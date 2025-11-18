from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import orders
from app.config import settings

# Create FastAPI app [10, p.85]
app = FastAPI(
    title="K-Beauty Landing Page API",
    description="API for K-Beauty landing page order processing",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://kbeauty-landing-page.web.app",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders.router, prefix="/api", tags=["orders"])


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "K-Beauty API is running"}


@app.get("/health")
def health_check():
    """Health check endpoint for Cloud Run."""
    return {"status": "healthy"}


@app.get("/api/config")
def get_config():
    """
    Provide frontend configuration including API keys.

    This endpoint allows frontend to dynamically load configuration
    without hardcoding sensitive values in static files.
    """
    return {
        "google_places_api_key": settings.google_places_api_key,
        "paypal_client_id": settings.paypal_client_id
    }
