import asyncio
import json
import logging
import os
from typing import List

from fastapi import WebSocket, WebSocketDisconnect

from app.data_collector import DataCollector

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration (environment variables with fallback defaults)
# ---------------------------------------------------------------------------
UPDATE_RATE_HZ: float = float(os.getenv("UPDATE_RATE_HZ", "10.0"))
DATA_MODE: str = os.getenv("DATA_MODE", "gait")


# ---------------------------------------------------------------------------
# ConnectionManager – keeps track of every active WebSocket client
# ---------------------------------------------------------------------------
class ConnectionManager:
    """Manages active WebSocket connections and broadcasts data to all clients."""

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """Accept and store a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove a connection from the active list."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        """Send a message to every connected client."""
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                # If sending fails the client is probably gone – remove it
                self.disconnect(connection)

    def get_connection_count(self) -> int:
        """Return the number of active connections."""
        return len(self.active_connections)


# Singleton instances shared across the application
manager = ConnectionManager()
collector = DataCollector(mode=DATA_MODE, update_rate_hz=UPDATE_RATE_HZ)


# ---------------------------------------------------------------------------
# WebSocket endpoint handler
# ---------------------------------------------------------------------------
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    /ws endpoint handler.

    Accepts a WebSocket connection, streams telemetry JSON at the configured
    rate, and gracefully handles disconnections.
    """
    client_id = f"{websocket.client.host}:{websocket.client.port}" if websocket.client else "unknown"

    # --- accept & register ---------------------------------------------------
    try:
        await manager.connect(websocket)
    except Exception as exc:
        logger.error("Failed to accept WebSocket connection from %s: %s", client_id, exc)
        return

    logger.info(
        "Client connected: %s, total connections: %d",
        client_id,
        manager.get_connection_count(),
    )

    # --- streaming loop ------------------------------------------------------
    interval = 1.0 / UPDATE_RATE_HZ
    loop = asyncio.get_event_loop()
    try:
        while True:
            # Generate telemetry in a thread so the blocking sleep inside
            # DataCollector.get_telemetry() doesn't freeze the event loop.
            telemetry = await loop.run_in_executor(None, collector.get_telemetry)

            # Serialize to JSON
            try:
                payload = telemetry.model_dump_json()
            except Exception as ser_err:
                logger.error("Serialization error: %s", ser_err)
                continue

            # Send to this specific client
            await websocket.send_text(payload)

            # Yield control and wait for next tick
            await asyncio.sleep(interval)

    except WebSocketDisconnect:
        pass  # client closed the connection normally
    except Exception as exc:
        logger.error("WebSocket error for %s: %s", client_id, exc)
    finally:
        manager.disconnect(websocket)
        logger.info(
            "Client disconnected: %s, total connections: %d",
            client_id,
            manager.get_connection_count(),
        )
