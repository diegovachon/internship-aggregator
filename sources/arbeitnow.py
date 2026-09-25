import requests
from sources.base import JobSource
from models.job import Job

from datetime import datetime, timezone


class ArbeitnowSource(JobSource):

    API_URL = "https://www.arbeitnow.com/api/job-board-api"

    def fetch_jobs(self):
        response = requests.get(
            self.API_URL,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data["data"]

    def normalize_job(self, raw_job: dict) -> Job:

        posted_at = datetime.fromtimestamp(
        raw_job["created_at"],
        tz=timezone.utc
        ).date()

        return Job(
            title=raw_job["title"],
            company=raw_job["company_name"],
            location=raw_job["location"],
            description=raw_job["description"],
            source="Arbeitnow",
            source_url=raw_job["url"],
            posted_at=posted_at
        )