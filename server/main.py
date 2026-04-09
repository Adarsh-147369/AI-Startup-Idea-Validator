from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware
import os

from database import create_all
from routes import ideas, export


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    create_all()
    yield


app = FastAPI(
    title="AI Startup Idea Validator API",
    description="Backend API for validating startup ideas using AI",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(ideas.router)
app.include_router(export.router)


@app.get("/api")
def api_root():
    """API root endpoint to check API health."""
    return {
        "message": "AI Startup Idea Validator API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Serve React static files
static_dir = os.path.join(os.path.dirname(__file__), "..", "client", "dist")

if os.path.exists(static_dir):
    # Mount assets directory with cache-busting headers
    assets_dir = os.path.join(static_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir, html=False), name="assets")


# Middleware to serve React app for non-API GET requests
class SPAMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Let API routes and assets pass through
        if request.url.path.startswith("/api") or request.url.path.startswith("/assets"):
            return await call_next(request)
        
        # Try to process the request normally
        response = await call_next(request)
        
        # If it's a 404 and a GET request, serve the React app
        if response.status_code == 404 and request.method == "GET":
            index_path = os.path.join(static_dir, "index.html")
            if os.path.exists(index_path):
                # Add cache-busting headers
                response = FileResponse(index_path)
                response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response.headers["Pragma"] = "no-cache"
                response.headers["Expires"] = "0"
                return response
        
        return response


# Add SPA middleware
if os.path.exists(static_dir):
    app.add_middleware(SPAMiddleware)
