from datetime import datetime

from database.models import IngestionRunRecord

from sqlalchemy import select

class IngestionRunRepository:

    def __init__(self, session):
        self.session = session

    def start(self, source: str) -> IngestionRunRecord:

        run = IngestionRunRecord(
            source=source,
            status="RUNNING",
            started_at=datetime.now(),
            jobs_found=0,
            jobs_added=0,
            jobs_skipped=0
        )

        self.session.add(run)
        self.session.commit()
        self.session.refresh(run)

        return run


    def mark_success(
            self,
            run: IngestionRunRecord,
            jobs_found: int,
            jobs_added: int,
            jobs_skipped: int
    ):

        run.status = "SUCCESS"
        run.finished_at = datetime.now()
        run.jobs_found = jobs_found
        run.jobs_added = jobs_added
        run.jobs_skipped = jobs_skipped

        self.session.commit()

    def mark_failed(
        self,
        run: IngestionRunRecord,
        error_message: str
    ):

        run.status = "FAILED"
        run.finished_at = datetime.now()
        run.error_message = error_message

        self.session.commit()


    def get_all(self) -> list[IngestionRunRecord]:

        statement = (
            select(IngestionRunRecord)
            .order_by(
                IngestionRunRecord.started_at.desc()
            )
        )

        result = self.session.execute(statement)

        return list(result.scalars().all())