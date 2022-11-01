from modules.abstract.scanner import Scanner
from modules.scanner.finding import Finding
from modules.scanner import ScannerManager
from modules.utils.helpers import plist_parse


@ScannerManager.add_filename_scanner('Info.plist')
class InfoPlistScanner(Scanner):
    async def perform_scan(self):
        dangerous_permissions = [
            'NFCReaderUsageDescription'
            'NSAppleMusicUsageDescription',
            'NSBluetoothPeripheralUsageDescription',
            'NSCalendarsUsageDescription',
            'NSCameraUsageDescription',
            'NSContactsUsageDescription',
            'NSHealthClinicalHealthRecordsShareUsageDescription',
            'NSHealthShareUsageDescription',
            'NSHealthUpdateUsageDescription',
            'NSHomeKitUsageDescription',
            'NSLocationAlwaysUsageDescription',
            'NSLocationUsageDescription',
            'NSLocationWhenInUseUsageDescription',
            'NSMicrophoneUsageDescription',
            'NSMotionUsageDescription',
            'NSPhotoLibraryUsageDescription',
            'NSRemindersUsageDescription',
            'NSSiriUsageDescription'
        ]
        plist = plist_parse(self.file_to_scan)

        if plist.get('NSAppTransportSecurity', {}).get('NSAllowsArbitraryLoads'):
            await self.report.add_finding(
                Finding(
                    title='NSAllowsArbitraryLoads set to true',
                    description=f'During checking {self.file_to_scan}, scanner found out that the '
                                f'NSAllowsArbitraryLoads flag were set to true. Thus allowing HTTP content to be '
                                'loaded in an insecure manner.',
                    likelihood=1,
                    impact=1,
                    risk=1,
                    recommendation='Set the <code>NSAllowsArbitraryLoads</code> to False to prevent loading insecure '
                                   'page.'
                )
            )

        dangerous_permissions_detected = []
        for dangerous_permission in dangerous_permissions:
            if dangerous_permission in plist:
                dangerous_permissions_detected.append(dangerous_permission)

        if len(dangerous_permissions_detected) != 0:
            dangerous_permissions_detected_str = '\n'.join(x for x in dangerous_permissions_detected)
            await self.report.add_finding(
                Finding(
                    title='Dangerous permission(s) detected',
                    description=f'During scanning {self.file_to_scan}, scanner found out that dangerous permissions '
                                f'are being used by the application. The permission(s) are:'
                                f'\n{dangerous_permissions_detected_str} '
                                '\nPlease check whether those permission(s) are actually needed by the application.',
                    likelihood=1,
                    impact=1,
                    risk=1,
                    recommendation='Please check whether those permission(s) are actually needed by the application.'
                )
            )
