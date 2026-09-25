from apscheduler.schedulers.blocking import BlockingScheduler

from database.connection import SessionLocal, engine
from database.models import Base
from services.ingestion_service import IngestionService
from sources.arbeitnow import ArbeitnowSource


Base.metadata.create_all(engine)


def run_ingestion():
    session = SessionLocal()

    try:
        service = IngestionService(session)

        service.run(
            ArbeitnowSource()
        )

        print("Ingestion completed successfully.")

    except Exception as error:
        print(f"Ingestion failed: {error}")

    finally:
        session.close()


scheduler = BlockingScheduler()

scheduler.add_job(
    run_ingestion,
    trigger="interval",
    hours=24,
    id="arbeitnow_ingestion",
    max_instances=1
)


print("Scheduler started.")

scheduler.start()