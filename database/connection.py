from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = (
    "postgresql+psycopg://localhost/internship_aggregator"
)

# SQLAlchemy connection infrastructure to the db
# Python application -> Engine -> PostgreSQL
engine = create_engine(DATABASE_URL)


# Session represents a working conversation with database
SessionLocal = sessionmaker(
    bind=engine
)