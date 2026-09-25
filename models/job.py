from dataclasses import dataclass
from datetime import date


@dataclass
class Job:
    title: str
    company: str
    location: str
    description: str
    source: str
    source_url: str
    posted_at: date | None = None