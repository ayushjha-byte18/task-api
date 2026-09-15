import os
import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL
    )
""")

conn.commit()

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute(
        "INSERT INTO tasks (id, title, done) VALUES (%s, %s, %s)",
        (1, "Learn FastAPI", False)
    )

    cursor.execute(
        "INSERT INTO tasks (id, title, done) VALUES (%s, %s, %s)",
        (2, "Build CRUD API", False)
    )

    cursor.execute(
        "INSERT INTO tasks (id, title, done) VALUES (%s, %s, %s)",
        (3, "Practice DSA", True)
    )

    conn.commit()


app = FastAPI(
    title="Task API",
    version="1.0"
)

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Practice DSA", "done": True}
]


@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        }
        for row in rows
    ]


@app.get("/tasks/{id}")
def get_task(id: int):
    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }


@app.post("/tasks", status_code=201)
def create_task(body: dict):
    title = body.get("title")

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
        (title, False)
    )

    conn.commit()

    new_id = cursor.fetchone()[0]

    return {
        "id": new_id,
        "title": title,
        "done": False
    }


@app.put("/tasks/{id}")
def update_task(id: int, body: dict):
    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    if not body:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    title = row[1]
    done = bool(row[2])

    if "title" in body:
        if not isinstance(body["title"], str) or not body["title"].strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

        title = body["title"]

    if "done" in body:
        if not isinstance(body["done"], bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be true or false"}
            )

        done = body["done"]

    if "title" not in body and "done" not in body:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid request body"}
        )

    cursor.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s",
        (title, done, id)
    )

    conn.commit()

    return {
        "id": id,
        "title": title,
        "done": done
    }


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (id,)
    )

    if cursor.rowcount == 0:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    conn.commit()

    return