import sqlite3
from fastapi import FastAPI
from fastapi.responses import JSONResponse

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL
    )
""")

conn.commit()
cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute(
        "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
        (1, "Learn FastAPI", 0)
    )
    cursor.execute(
        "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
        (2, "Build CRUD API", 0)
    )
    cursor.execute(
        "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
        (3, "Practice DSA", 1)
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
    return tasks


@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )


@app.post("/tasks", status_code=201)
def create_task(body: dict):
    title = body.get("title")

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )

    new_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "id": new_id,
        "title": title,
        "done": False
    }

    tasks.append(new_task)

    return new_task

@app.put("/tasks/{id}")
def update_task(id: int, body: dict):
    for task in tasks:
        if task["id"] == id:

            if not body:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Request body cannot be empty"}
                )

            if "title" in body:
                if not isinstance(body["title"], str) or not body["title"].strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"}
                    )
                task["title"] = body["title"]

            if "done" in body:
                if not isinstance(body["done"], bool):
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Done must be true or false"}
                    )
                task["done"] = body["done"]

            if "title" not in body and "done" not in body:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid request body"}
                )

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )