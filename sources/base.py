from abc import ABC, abstractmethod
from models.job import Job

class JobSource(ABC):

    @abstractmethod
    def fetch_jobs(self):
        pass

    @abstractmethod
    def normalize_job(self, raw_job: dict) -> Job:
        pass

    def get_jobs(self) -> list[Job]:
        raw_jobs = self.fetch_jobs()

        return [
            self.normalize_job(raw_job)
            for raw_job in raw_jobs
        ]