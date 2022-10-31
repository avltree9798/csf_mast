from modules.abstract.scanner import Scanner
from modules.scanner import ScannerManager


@ScannerManager.add_filename_scanner('Info.plist')
class InfoPlistScanner(Scanner):
    async def perform_scan(self):
        print("Info.plist Scanner")