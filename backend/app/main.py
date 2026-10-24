from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.infrastructure.database.supabase_client import get_supabase_client
from app.presentation.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup: verify Supabase client initialization
    get_supabase_client()
    yield
    # Application shutdown


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Asynchronous MemorizeMe API built with FastAPI, Supabase (PostgreSQL), and Supabase Auth following Clean Architecture.",
    lifespan=lifespan,
)

# CORS configuration to allow requests from web browsers and mobile WebViews
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 endpoints
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": "Supabase (PostgreSQL)",
        "auth": "Supabase Auth (JWT)",
    }
