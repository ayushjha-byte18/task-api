# Task API

A REST API built with Python, FastAPI, and PostgreSQL, containerized with Docker Compose.

## What it does

The API supports full CRUD operations for tasks:

- Create a task
- Read all tasks
- Read a single task
- Update a task
- Delete a task

Tasks are stored in PostgreSQL, so data persists across API/container restarts.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- psycopg
- Docker
- Docker Compose

## Project Structure

```text
task-api-a3/
|-- main.py
|-- Dockerfile
|-- compose.yaml
|-- .dockerignore
|-- .env.example
|-- .gitignore
`-- README.md

## Environment Setup

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks

## Run with Docker Compose

Start the API and PostgreSQL database with:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

To stop the containers:

```bash
docker compose down
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get one task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

All task data is stored in PostgreSQL.

## Example Requests

### Get all tasks

```bash
curl -i http://localhost:8000/tasks
```

### Create a task

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Learn Docker\"}"
```

### Update a task

```bash
curl -i -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"done\":true}"
```

### Delete a task

```bash
curl -i -X DELETE http://localhost:8000/tasks/1
```

## Docker Architecture

The application runs as two Docker Compose services:

- **API** — FastAPI application running on port `8000`
- **Database** — PostgreSQL database running on port `5432`

The API connects to PostgreSQL using the Docker service name `db`.

A Docker volume is used so database data persists even when the containers are stopped and restarted.

## Database Persistence

PostgreSQL data is stored using a Docker volume named `taskdata`.

This means tasks remain available after stopping and restarting the Docker Compose services.

For example, a task created before restarting the containers will still be present after:

```bash
docker compose down
docker compose up -d
```

## PostgreSQL Database

The tasks are stored in PostgreSQL:

![PostgreSQL database](postgres-db.png)

## Repository

This project is part of my Backend Assignment A3.

GitHub repository:

https://github.com/ayushjha-byte18/task-api