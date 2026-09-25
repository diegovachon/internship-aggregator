Distributed Internship Aggregation Platform

This project is a backend platform that collects job postings from external sources, converts them into a common format, stores them in PostgreSQL, and exposes them through a REST API.

I built it mainly to practice backend system design, data ingestion, API development, and working with multiple external data formats.


What the project does

The platform currently:

- Fetches real job postings from the Arbeitnow API
- Converts external job data into a common Job model
- Stores normalized jobs in PostgreSQL
- Avoids inserting the same job multiple times
- Tracks ingestion runs and their status
- Exposes stored jobs through FastAPI
- Can automatically run ingestion every few hours using APScheduler


How it works

The main ingestion flow looks like this:

Arbeitnow API
    ↓
Source adapter
    ↓
Raw job data
    ↓
Normalization
    ↓
Job model
    ↓
Ingestion service
    ↓
PostgreSQL

The API then reads the stored jobs from PostgreSQL:

Client
    ↓
FastAPI
    ↓
PostgreSQL
    ↓
JSON response


Why normalization is needed

Different job sources usually return similar information using different field names and structures.

For example, one source might return:

    job_title
    company_name
    city

while another might return:

    position
    employer
    location

Instead of letting those differences spread through the application, every source converts its data into the same internal Job model.

The rest of the backend can then work with:

    title
    company
    location
    description
    source
    source_url
    posted_at


Project structure

internship-aggregator/
|
|-- api/
|   |-- routes.py
|   |-- schemas.py
|
|-- database/
|   |-- connection.py
|   |-- models.py
|
|-- models/
|   |-- job.py
|
|-- repositories/
|   |-- job_repository.py
|   |-- ingestion_run_repository.py
|
|-- services/
|   |-- ingestion_service.py
|
|-- sources/
|   |-- base.py
|   |-- arbeitnow.py
|
|-- main.py
|-- run_ingestion.py
|-- scheduler.py
|-- requirements.txt


Main components

JobSource

Defines the common interface used by external job sources.

Each source is responsible for fetching its own data and converting it into the internal Job model.


Job

Represents a normalized job posting inside the application.


JobRepository

Handles job-related database operations such as saving jobs, retrieving them, and checking if a job already exists.


IngestionService

Coordinates a full ingestion run.

It:

1. Starts an ingestion run
2. Fetches jobs
3. Normalizes them
4. Skips jobs that already exist
5. Stores new jobs
6. Marks the run as successful or failed


IngestionRunRepository

Stores information about each ingestion execution, including:

- status
- start time
- end time
- jobs found
- jobs added
- jobs skipped
- error message


Tech stack

Python
FastAPI
PostgreSQL
SQLAlchemy
psycopg
Requests
APScheduler
Uvicorn


Setup

Create a virtual environment:

    python3 -m venv .venv

Activate it:

    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt


Database

Create the PostgreSQL database:

    createdb internship_aggregator

The application currently connects using:

    postgresql+psycopg://localhost/internship_aggregator


Run ingestion manually

    python run_ingestion.py

This fetches jobs from Arbeitnow and stores new ones in PostgreSQL.


Run the API

    python -m uvicorn main:app --reload

The API will run at:

    http://127.0.0.1:8000

Swagger documentation is available at:

    http://127.0.0.1:8000/docs


Main API endpoints

GET /jobs

Returns all stored jobs.


GET /jobs/{job_id}

Returns one job by ID.


POST /ingestion/run

Starts an ingestion run manually.


GET /ingestion/runs

Returns the history of ingestion runs.


Run automatic ingestion

Start the scheduler with:

    python scheduler.py

The scheduler runs the ingestion process automatically every six hours.

For testing, the interval can temporarily be changed to one minute.


Duplicate handling

The source URL is used as the current unique identifier for a job.

Before inserting a job, the application checks if the URL already exists.

The database also has a unique constraint on source_url, which gives an extra layer of protection against duplicate inserts.


Current limitations

This is still a relatively small version of the system.

Right now:

- Arbeitnow is the only real source
- Ingestion runs synchronously
- Duplicate detection is based mainly on the source URL
- There is no authentication
- Some job descriptions may still contain HTML
- The scheduler only runs while the scheduler process is active


Possible next steps

Some things I could add later:

- More job sources
- Internship-specific filtering
- Search and filters
- Better duplicate detection
- Background workers
- Docker
- Tests
- Authentication


Goal of the project

The main goal of this project was to understand how to build a backend system that collects data from external services and turns it into a consistent internal format.

The part I found most interesting was separating the system into clear layers so that the API, database, ingestion logic, and external sources do not depend too heavily on each other.
