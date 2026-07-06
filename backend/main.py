import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from datetime import datetime
from database.config import get_db
from backend.routes.auth import router as auth_router
from backend.routes.documents import router as documents_router
from backend.routes.conversations import router as conversations_router

# Initialize FastAPI app
app = FastAPI(
    title="DocMind",
    description="AI-powered document management and conversational assistant",
    version="1.0.0",
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(conversations_router, prefix="/api")

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# Lifespan context manager for startup/shutdown
@app.on_event("startup")
async def startup_event():
    from database.config import engine as _aakaar_engine
    from sqlalchemy import text as _sa_text
    with _aakaar_engine.begin() as _aakaar_conn:
        _aakaar_conn.execute(_sa_text("CREATE EXTENSION IF NOT EXISTS vector"))
    from database.models import Base as _AakaarBase
    _AakaarBase.metadata.create_all(bind=_aakaar_engine)
    db = get_db()
    try:
        # Initialize database connection or perform any startup tasks
        pass
    finally:
        db.close()

@app.on_event("shutdown")
async def shutdown_event():
    db = get_db()
    try:
        # Perform any cleanup tasks
        pass
    finally:
        db.close()

# Auto-mounted AI router — ai/routes.py exposes /api/ai/* (it carries its own prefix)
from ai.routes import router as ai_router
app.include_router(ai_router)
