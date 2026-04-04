"""Async-safe shared state for power data from MCU."""

import asyncio
import logging
import os
import time
from typing import Optional

from app.models import PowerUpdate

logger = logging.getLogger(__name__)

# Configuration (env vars)
STALE_THRESHOLD_SECONDS = float(os.getenv("POWER_STALE_THRESHOLD", "5.0"))
VOLTAGE_MIN = float(os.getenv("VOLTAGE_VALID_MIN", "0.0"))
VOLTAGE_MAX = float(os.getenv("VOLTAGE_VALID_MAX", "60.0"))


class PowerState:
    """Async-safe container for power sensor data with staleness detection."""

    def __init__(self, stale_threshold_seconds: float = 5.0):
        self._data: Optional[PowerUpdate] = None
        self._last_update: float = 0.0
        self._lock = asyncio.Lock()
        self._stale_threshold = stale_threshold_seconds

    async def update(self, data: PowerUpdate) -> None:
        """Store new power data with validation."""
        for i, sensor in enumerate(data.sensors):
            if not sensor.healthy:
                logger.warning(f"Sensor {i+1} reports unhealthy")
            if not (VOLTAGE_MIN <= sensor.voltage <= VOLTAGE_MAX):
                logger.warning(f"Sensor {i+1} voltage {sensor.voltage}V out of range")
        
        async with self._lock:
            self._data = data
            self._last_update = time.time()

    async def get(self) -> Optional[PowerUpdate]:
        """Get current data if not stale (async)."""
        async with self._lock:
            if self._data is None or self.is_stale():
                return None
            return self._data

    def get_sync(self) -> Optional[PowerUpdate]:
        """Get current data if not stale (sync, for thread pools)."""
        if self._data is None or self.is_stale():
            return None
        return self._data

    def is_stale(self) -> bool:
        """Check if data is stale."""
        if self._data is None:
            return True
        return (time.time() - self._last_update) > self._stale_threshold

    @property
    def last_update_time(self) -> float:
        return self._last_update


# Singleton instance
power_state = PowerState(stale_threshold_seconds=STALE_THRESHOLD_SECONDS)
