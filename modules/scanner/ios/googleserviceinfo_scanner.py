from modules.abstract.scanner import Scanner
from modules.logger import logger
from modules.scanner.finding import Finding
from modules.scanner import ScannerManager
from modules.utils.helpers import plist_parse, GOOGLE_API_URL
import requests


@ScannerManager.add_filename_scanner('GoogleServiceInfo.plist')
class GoogleServiceInfoScanner(Scanner):
    async def perform_scan(self):
        plist = plist_parse(self.file_to_scan)
        if plist.get('API_KEY'):
            api_key = plist['API_KEY']
            vulnerable_api_keys = []
            for api, url in GOOGLE_API_URL:
                try:
                    response = requests.get(url + api_key)
                    if response.status_code == 200 and "REQUEST_DENIED" not in response.text:
                        vulnerable_api_keys.append(api)
                except Exception as e:
                    logger.error(f'[-] Uncaught exception at GoogleServiceInfoScanner.perform_scan: {e}')

            vulnerable_api_keys_str = '\n'.join(x for x in vulnerable_api_keys)
            if len(vulnerable_api_keys):
                await self.report.add_finding(
                    Finding(
                        title='Vulnerable Google MAP API Key Leaked',
                        description=f'During scanning {self.file_to_scan} file, scanner detect one or more '
                                    f'occurrences of a vulnerable Google Map API key with these contents:'
                                    f'\n {vulnerable_api_keys_str} ',
                        likelihood=2,
                        impact=2,
                        risk=2,
                        recommendation='Please configure the Google Map API key so malicious actor can\'t use the key '
                                       'arbitrarily. '
                    )
                )