from abc import ABC, abstractmethod
from asonic import Client

import time


class Scanner(ABC):
    def __init__(self, *, database_client: Client, application_path: str):
        self.started_at = time.time_ns()
        self.database_client = database_client
        self.application_path = application_path

    @abstractmethod
    async def perform_scan(self):
        pass

    async def save_result(self):
        pass
