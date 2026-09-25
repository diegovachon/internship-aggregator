from datetime import date, datetime

# Pydantic for data validation and serialization
from pydantic import BaseModel, ConfigDict


class JobResponse(BaseModel):

    id: int
    title: str
    company: str
    location: str
    description: str
    source: str
    source_url: str
    posted_at: date | None

    model_config = ConfigDict(
        from_attributes=True
    )


class IngestionRunResponse(BaseModel):

    id: int
    source: str
    status: str

    started_at: datetime
    finished_at: datetime | None

    jobs_found: int
    jobs_added: int
    jobs_skipped: int

    error_message: str | None

    model_config = ConfigDict(
        from_attributes=True
    )