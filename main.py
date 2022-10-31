from modules.scanner import ScannerManager
from modules.utils.constant import PLATFORM_EXTENSION
import asyncio
import uuid
import sys


async def main():
    if len(sys.argv) != 2:
        print(f'Run: {sys.argv[0]} YOUR_MOBILE_APP.[ipa/apk]')
        exit()

    platform = PLATFORM_EXTENSION.get(sys.argv[1].split('.')[1])
    scan_id = uuid.uuid4()
    scanner_manager = await ScannerManager.init(
        platform=platform,
        application=sys.argv[1],
        scan_id=scan_id
    )
    await scanner_manager.start_scanner()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
