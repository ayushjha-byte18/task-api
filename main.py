import os

from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client, Client


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PORT = int(os.getenv("PORT", "8000"))

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


app = FastAPI(
    title="Task API - Auth",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "name": "Task API - Auth",
        "version": "1.0",
        "message": "Authentication API"
    }


@app.get("/health")
def health():
    return {"status": "ok"}