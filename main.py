import os

from dotenv import load_dotenv
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from supabase_auth.errors import AuthApiError


# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PORT = int(os.getenv("PORT", "8000"))


# Create Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# Create FastAPI app
app = FastAPI(
    title="Task API - Auth",
    version="1.0"
)


# Home route
@app.get("/")
def home():
    return {
        "name": "Task API - Auth",
        "version": "1.0",
        "message": "Authentication API"
    }


# Health check
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Stage 1: Signup
@app.post("/auth/signup", status_code=201)
def signup(body: dict):
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Email and password are required"
            }
        )

    response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    return response.user


# Stage 1: Login
@app.post("/auth/login")
def login(body: dict):
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Email and password are required"
            }
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except AuthApiError:
        return JSONResponse(
            status_code=401,
            content={
                "error": "Invalid email or password"
            }
        )


# Stage 2: Public route
@app.get("/public/info")
def public_info():
    return {
        "message": "This is a public endpoint",
        "authenticated": False
    }


# Stage 2: Protected route
@app.get("/protected/profile")
def protected_profile(authorization: str | None = Header(default=None)):
    # Check Authorization header
    if not authorization:
        return JSONResponse(
            status_code=401,
            content={
                "error": "Authorization header required"
            }
        )

    # Check Bearer token format
    parts = authorization.split(" ", 1)

    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
        return JSONResponse(
            status_code=401,
            content={
                "error": "Invalid authorization header"
            }
        )

    token = parts[1]

    # Stage 2 only checks that a Bearer token is present.
    # Actual JWT verification is implemented in Stage 3.
    return {
        "message": "Bearer token received",
        "token_present": True
    }