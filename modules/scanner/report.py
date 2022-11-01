from modules.logger import logger
import asyncio
import json
import time


class Report:
    def __init__(self, *, scan_id: str):
        self.scan_id = scan_id
        self.findings = []
        self.lock = asyncio.Lock()

    async def add_finding(self, finding):
        async with self.lock:
            self.findings.append(finding)

    def save_to_file(self):
        output = f'/tmp/{self.scan_id}.json'
        with open(output, 'w+') as fp:
            json_report = {
                'scan_id': str(self.scan_id),
                'report_generated_at': time.time(),
                'findings': []
            }
            for finding in self.findings:
                json_report['findings'].append(finding.__dict__)

            json.dump(json_report, fp)
            logger.info(f'[+] Report saved at {output}')
