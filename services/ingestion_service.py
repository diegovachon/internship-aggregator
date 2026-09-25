from repositories.job_repository import JobRepository
from repositories.ingestion_run_repository import IngestionRunRepository


class IngestionService:

    def __init__(self, session):

        self.job_repository = JobRepository(session)

        self.run_repository = IngestionRunRepository(session)


    def run(self, source):

        run = self.run_repository.start(
            source=source.__class__.__name__
        )

        try:
            jobs = source.get_jobs()

            jobs_found = len(jobs)
            jobs_added = 0
            jobs_skipped = 0

            for job in jobs:

                if self.job_repository.exists_by_source_url(
                    job.source_url
                ):
                    jobs_skipped += 1
                    continue

                self.job_repository.save(job)

                jobs_added += 1

            self.run_repository.mark_success(
                run=run,
                jobs_found=jobs_found,
                jobs_added=jobs_added,
                jobs_skipped=jobs_skipped
            )

            return run

        except Exception as error:

            self.run_repository.mark_failed(
                run=run,
                error_message=str(error)
            )

            raise