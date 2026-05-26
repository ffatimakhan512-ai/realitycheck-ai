import sys
import os

# Add the project root to sys.path to allow running this script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routes.analyze import router as analyze_router

app = FastAPI(
    title="RealityCheck AI Engine",
    description="Intelligent Rule-Based Fake News, Sensationalism & Punctuation Sentiment Analysis Platform.",
    version="1.0.0"
)

# Configure Cross-Origin Resource Sharing (CORS)
# Allows the local frontend file system or custom hosts to reach the FastAPI REST service
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits all origins for simplified local hosting environments
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(analyze_router)

@app.get("/health")
def read_root():
    """
    Health check and metadata route.
    """
    return {
        "status": "online",
        "service": "RealityCheck AI – Fake News & Misinformation Analyzer",
        "version": "1.0.0",
        "docs_url": "/docs",
        "capabilities": [
            "Credibility scoring (0-100)",
            "Sensationalism & clickbait word extraction",
            "Punctuation sentiment metrics",
            "Domain reputational audit",
            "Inline highlight offsets mapping"
        ]
    }

frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
if __name__ == "__main__":
    # Boot server locally on port 8000
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
