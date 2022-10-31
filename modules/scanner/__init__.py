from asonic import Client
from asonic.enums import Channel
from modules.abstract.scanner import Scanner
from modules.scanner.report import Report
from modules.utils.preprocessor import PREPROCESSOR
from modules.logger import logger
from modules.utils.constant import (
    DB_HOST,
    DB_PASS,
    DB_PORT,
    DB_MAX_CONNECTION,
    MAX_WORKER
)
import asyncio
import importlib
import magic
import os


class ScannerManager:
    scanner_by_filename = {}
    scanner_by_mimetype = {}

    @classmethod
    async def init(cls, *, platform: str, application: str, scan_id: str):
        self = ScannerManager()
        self.platform = platform
        assert self.platform in {'ios', 'android'}
        self.application = application
        self.scan_id = scan_id
        await self._bootstrap()
        return self

    async def _bootstrap(self):
        self._load_scanner_modules()
        assert await self._connect_to_database()
        preprocessor_method = PREPROCESSOR.get(self.platform)
        assert preprocessor_method
        self.scan_path = preprocessor_method(filename=self.application, scan_id=self.scan_id)

    @classmethod
    def add_filename_scanner(cls, filename: str):
        def decorator(scanner):
            if not issubclass(scanner, Scanner):
                logger.error('Scanner must be a subclass of modules.abstract.Scanner')
                return
            logger.info(f'[+] Registering {scanner.__name__} as a scanner for file {filename}')
            if filename not in cls.scanner_by_filename.keys():
                cls.scanner_by_filename[filename] = []
            cls.scanner_by_filename[filename].append(scanner)

        return decorator

    @classmethod
    def add_mimetype_scanner(cls, mimetype: str):
        def decorator(scanner):
            if not issubclass(scanner, Scanner):
                logger.error('Scanner must be a subclass of modules.abstract.Scanner')
                return
            logger.info(f'[+] Registering {scanner.__name__} as a scanner for type {mimetype}')
            if mimetype not in cls.scanner_by_mimetype.keys():
                cls.scanner_by_mimetype[mimetype] = []
            cls.scanner_by_mimetype[mimetype].append(scanner)

        return decorator

    def _load_scanner_modules(self):
        try:
            scanner_modules_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.platform)
            module_files = [
                f.split('.py')[0] for f in os.listdir(scanner_modules_path) if
                os.path.isfile(os.path.join(scanner_modules_path, f)) and f.endswith('scanner.py')
            ]
            for module_file in module_files:
                scanner_module = f'modules.scanner.{self.platform}.{module_file}'
                importlib.import_module(scanner_module)

        except Exception as e:
            logger.exception(e)

    async def _connect_to_database(self):
        return_value = True
        try:
            self.db_client = Client(
                host=DB_HOST,
                port=DB_PORT,
                password=DB_PASS,
                max_connections=DB_MAX_CONNECTION
            )
            await self.db_client.ping()
            await self.db_client.channel(Channel.INGEST)
        except ConnectionRefusedError as e:
            logger.error('ConnectionRefusedError at _connect_to_database: {e}')
            return_value = False
        finally:
            return return_value

    async def start_scanner(self):
        async def producer(scanner_queue):
            filenames = set(self.scanner_by_filename.keys())
            mimetypes = set(self.scanner_by_mimetype.keys())
            mime = magic.Magic(mime=True)
            for subdir, dirs, files in os.walk(self.scan_path):
                for file in files:
                    file_to_scan = os.path.join(subdir, file)
                    if file in filenames:
                        scanner_queue.put_nowait(
                            (file_to_scan, self.scanner_by_filename.get(file))
                        )
                    mimetype = mime.from_file(file_to_scan)
                    if mimetype in mimetypes:
                        scanner_queue.put_nowait(
                            (file_to_scan, self.scanner_by_mimetype.get(mimetype))
                        )

        async def consumer(scanner_queue, report):
            while True:
                try:
                    file_to_scan, scanner_classes = scanner_queue.get_nowait()
                    for scanner_class in scanner_classes:
                        scanner = scanner_class(
                            database_client=self.db_client,
                            file_to_scan=file_to_scan,
                            report=report
                        )
                        await scanner.perform_scan()
                except asyncio.queues.QueueEmpty:
                    break
                except Exception as e:
                    logger.error(f'[-] Uncaught exception at modules.scanner.ScannerManager.start_scanner.consumer: {e}')

        queue = asyncio.Queue()
        tasks = [
            asyncio.create_task(producer(queue))
        ]
        await asyncio.sleep(1)
        scanner_report = Report(
            scan_id=self.scan_id
        )
        for _ in range(MAX_WORKER):
            tasks.append(
                asyncio.create_task(consumer(queue, scanner_report))
            )

        await asyncio.wait(tasks)
        scanner_report.save_to_file()

