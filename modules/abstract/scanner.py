from abc import ABC, abstractmethod
from asonic import Client
from modules.scanner.report import Report

import time


class Scanner(ABC):
    def __init__(self, *, database_client: Client, file_to_scan: str, report: Report):
        self.started_at = time.time_ns()
        self.database_client = database_client
        self.file_to_scan = file_to_scan
        self.report = report
        self.findings = []

    @abstractmethod
    async def perform_scan(self):
        pass

