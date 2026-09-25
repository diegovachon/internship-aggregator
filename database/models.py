# In models.py, we define the database representation of a job
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


# We define what the PostgreSQL table should look like
"""
Why define a new class JobRecord instead of reusing Job class already defined
in models/job.py? We ultimately want 
External API -> Job -> JobRecord -> PostgreSQL
Why? The core app is not tightly coupled to SQLAlchemy i.e. 
ArbeitnowSource e.g. does not need to know PostgreSQL exists
i.e. separation of concerns
"""
class JobRecord(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    company: Mapped[str] = mapped_column(
        String(255)
    )

    location: Mapped[str] = mapped_column(
        String(255)
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    source: Mapped[str] = mapped_column(
        String(100)
    )

    source_url: Mapped[str] = mapped_column(
        Text,
        unique=True
    )

    posted_at: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )


class IngestionRunRecord(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    source: Mapped[str] = mapped_column(
        String(100)
    )

    status: Mapped[str] = mapped_column(
        String(100)
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    jobs_found: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    jobs_added: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    jobs_skipped: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )