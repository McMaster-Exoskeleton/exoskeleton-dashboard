import json
import logging
import os
from typing import Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MetricThresholds(BaseModel):
    """Warning/critical threshold values for a metric."""

    warning: float = Field(..., description="Warning threshold")
    critical: float = Field(..., description="Critical threshold")


class MotorThresholds(BaseModel):
    """Thresholds for motor telemetry metrics."""

    temperature: MetricThresholds = Field(
        default_factory=lambda: MetricThresholds(warning=50.0, critical=60.0)
    )
    current: MetricThresholds = Field(
        default_factory=lambda: MetricThresholds(warning=10.0, critical=13.0)
    )


class Ina228Thresholds(BaseModel):
    """Thresholds for INA228 telemetry metrics."""

    voltage: MetricThresholds = Field(
        default_factory=lambda: MetricThresholds(warning=27.0, critical=29.0)
    )
    current: MetricThresholds = Field(
        default_factory=lambda: MetricThresholds(warning=8.0, critical=12.0)
    )


class ThresholdsConfig(BaseModel):
    """Top-level threshold configuration."""

    motors: MotorThresholds = Field(default_factory=MotorThresholds)
    ina228: Ina228Thresholds = Field(default_factory=Ina228Thresholds)


DEFAULT_THRESHOLDS = ThresholdsConfig()


def _load_thresholds_data() -> Optional[dict]:
    raw = os.getenv("THRESHOLDS_JSON")
    path = os.getenv("THRESHOLDS_PATH")

    if path:
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except Exception as exc:
            logger.warning("Failed to read THRESHOLDS_PATH '%s': %s", path, exc)
            return None

    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.warning("Failed to parse THRESHOLDS_JSON: %s", exc)

    return None


def load_thresholds() -> ThresholdsConfig:
    """Load thresholds from environment overrides or defaults."""

    data = _load_thresholds_data()
    if data is None:
        return DEFAULT_THRESHOLDS

    try:
        return ThresholdsConfig.model_validate(data)
    except Exception as exc:
        logger.warning("Invalid thresholds config; using defaults: %s", exc)
        return DEFAULT_THRESHOLDS
