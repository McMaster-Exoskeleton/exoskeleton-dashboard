import logging

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.websocket import websocket_endpoint

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="Exoskeleton Telemetry API",
    description="WebSocket server for streaming exoskeleton telemetry data",
    version="0.1.0",
)

# Configure CORS for frontend development
# Using allow_origins=["*"] ensures WebSocket upgrades are not blocked by
# missing or mismatched Origin headers (e.g. wscat, Postman, etc.).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the server is running."""
    return {"status": "healthy", "service": "exoskeleton-telemetry"}


@app.websocket("/ws")
async def ws(websocket: WebSocket):
    """WebSocket endpoint for streaming telemetry data."""
    await websocket_endpoint(websocket)
