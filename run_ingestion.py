from database.connection import engine, SessionLocal
from database.models import Base
from services.ingestion_service import IngestionService
from sources.arbeitnow import ArbeitnowSource


Base.metadata.create_all(engine)


session = SessionLocal()

try:
    service = IngestionService(session)

    service.run(
        ArbeitnowSource()
    )

finally:
    session.close()