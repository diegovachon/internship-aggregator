"""
A repository is an abstraction around persistance
Instead of the app saying: session.add(...) and session.commit(...)
it says: repository.save(job).

Conceptually,
Application -save(job)-> JobRepository -SQLAlc-> PostgreSQL
We don't want to sources to save directly i.e. session.add(...)
since the class will then have two responsabilities (understands
Arbeitnow and PostgreSQL)
"""
from sqlalchemy import select

from models.job import Job
from database.models import JobRecord

class JobRepository:

    def __init__(self, session):
        self.session = session

    def save(self, job: Job) -> JobRecord:

        record = JobRecord(
            title=job.title,
            company=job.company,
            location=job.location,
            description=job.description,
            source=job.source,
            source_url=job.source_url,
            posted_at=job.posted_at
        )

        self.session.add(record)
        self.session.commit()

        return record

    def get_all(self) -> list[JobRecord]:

        statement = select(JobRecord)

        result = self.session.execute(statement)

        return list(result.scalars().all())

    def get_by_id(self, job_id: int) -> JobRecord | None:
        return self.session.get(JobRecord, job_id)


    def exists_by_source_url(self, source_url: str) -> bool:

        statement = select(JobRecord).where(
        JobRecord.source_url == source_url
    )

        result = self.session.execute(statement)

        return result.scalar_one_or_none() is not None