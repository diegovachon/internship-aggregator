from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas import JobResponse
from database.connection import SessionLocal
from repositories.job_repository import JobRepository

from services.ingestion_service import IngestionService
from sources.arbeitnow import ArbeitnowSource

from api.schemas import (
    JobResponse,
    IngestionRunResponse
)

from repositories.ingestion_run_repository import (
    IngestionRunRepository
)

# The router contains our job endpoint

router = APIRouter()


"""
Basically, every HTTP request needs a database session:
HTTP request -> open DB session -> run query -> return response -> close session
We don't want the db sessions open forever
"""
def get_db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()

"""
When an HTTP GET request arrives at /jobs, execute this function
"""
@router.get(
    "/jobs",
    response_model=list[JobResponse]
)
def get_jobs(
    session: Session = Depends(get_db)
):
    repository = JobRepository(session)

    jobs = repository.get_all()

    return jobs

@router.get(
    "/jobs/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: int,
    session: Session = Depends(get_db)
):
    repository = JobRepository(session)

    job = repository.get_by_id(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


@router.post("/ingestion/run")
def run_ingestion(
    session: Session = Depends(get_db)
):

    service = IngestionService(session)

    run = service.run(
        ArbeitnowSource()
    )

    return {
        "run_id": run.id,
        "status": run.status
    }


@router.get(
    "/ingestion/runs",
    response_model=list[IngestionRunResponse]
)
def get_ingestion_runs(
    session: Session = Depends(get_db)
):

    repository = IngestionRunRepository(session)

    return repository.get_all()