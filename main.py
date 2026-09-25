from fastapi import FastAPI
from api.routes import router
from database.connection import engine
from database.models import Base

# Take the Python db models and create their tables
Base.metadata.create_all(engine)

app = FastAPI(
    title="Internship Aggregation Platform"
)

app.include_router(router)