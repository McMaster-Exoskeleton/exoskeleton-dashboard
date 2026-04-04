"""Async-safe shared state for IMU data from MCUs."""

import asyncio
import logging
import os
import time
from typing import Dict, Optional

from app.models import IMUData, IMUUpdate

logger = logging.getLogger(__name__)

STALE_THRESHOLD_SECONDS = float(os.getenv("IMU_STALE_THRESHOLD", "5.0"))
VALID_JOINTS = {"left_hip", "left_knee", "right_hip", "right_knee"}


class IMUState:
    """Async-safe container for IMU sensor data with staleness detection."""

    def __init__(self, stale_threshold_seconds: float = 5.0):
        self._data: Dict[str, IMUData] = {}
        self._last_updates: Dict[str, float] = {}
        self._lock = asyncio.Lock()
        self._stale_threshold = stale_threshold_seconds

    async def update(self, data: IMUUpdate) -> None:
        """Store new IMU data for a joint."""
        if data.joint not in VALID_JOINTS:
            logger.warning(f"Unknown joint '{data.joint}' in IMU update, ignoring")
            return

        imu = IMUData(
            acceleration=data.acceleration,
            gyroscope=data.gyroscope,
        )

        async with self._lock:
            self._data[data.joint] = imu
            self._last_updates[data.joint] = time.time()

    def get_sync(self, joint: str) -> Optional[IMUData]:
        """Get current IMU data for a joint if not stale (sync)."""
        if joint not in self._data:
            return None
        if (time.time() - self._last_updates.get(joint, 0)) > self._stale_threshold:
            return None
        return self._data[joint]

    def is_stale(self, joint: str) -> bool:
        """Check if data for a joint is stale."""
        if joint not in self._last_updates:
            return True
        return (time.time() - self._last_updates[joint]) > self._stale_threshold


# Singleton instance
imu_state = IMUState(stale_threshold_seconds=STALE_THRESHOLD_SECONDS)
