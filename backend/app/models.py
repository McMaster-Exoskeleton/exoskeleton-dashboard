from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class MotorStatus(str, Enum):
    """Motor health status."""

    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    OFFLINE = "offline"


class SystemHealthStatus(str, Enum):
    """Overall system health status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"


class AlertSeverity(str, Enum):
    """Alert severity levels."""

    WARNING = "warning"
    CRITICAL = "critical"


class JointData(BaseModel):
    """Telemetry data for a single joint."""

    position: float = Field(..., description="Joint angle in radians (-π to π)")
    velocity: float = Field(..., description="Angular velocity in rad/s")
    torque: float = Field(..., description="Applied torque in Nm")


class JointsData(BaseModel):
    """Telemetry data for all joints."""

    left_hip: JointData
    left_knee: JointData
    right_hip: JointData
    right_knee: JointData


class MotorData(BaseModel):
    """Telemetry data for a single motor."""

    current: float = Field(..., description="Current draw in Amperes")
    temperature: float = Field(..., description="Motor temperature in Celsius")
    status: MotorStatus = Field(..., description="Motor health status")


class MotorsData(BaseModel):
    """Telemetry data for all motors."""

    left_hip: MotorData
    left_knee: MotorData
    right_hip: MotorData
    right_knee: MotorData


class MotorAlertData(BaseModel):
    """Alert state for a motor's metrics."""

    temperature: Optional[AlertSeverity] = Field(
        default=None, description="Alert severity for motor temperature"
    )
    current: Optional[AlertSeverity] = Field(
        default=None, description="Alert severity for motor current"
    )


class MotorsAlertsData(BaseModel):
    """Alert states for all motors."""

    left_hip: MotorAlertData
    left_knee: MotorAlertData
    right_hip: MotorAlertData
    right_knee: MotorAlertData


class IMUData(BaseModel):
    """Telemetry data for a single IMU sensor."""

    acceleration: List[float] = Field(
        ..., min_length=3, max_length=3, description="Acceleration [x, y, z] in m/s²"
    )
    gyroscope: List[float] = Field(
        ..., min_length=3, max_length=3, description="Angular velocity [x, y, z] in rad/s"
    )


class SensorsData(BaseModel):
    """Telemetry data for all IMU sensors."""

    left_hip: IMUData
    left_knee: IMUData
    right_hip: IMUData
    right_knee: IMUData


class SensorReading(BaseModel):
    """Reading from a single INA228 power sensor."""

    voltage: float = Field(..., ge=0, description="Voltage in Volts")
    current: float = Field(..., description="Current in Amperes")
    power: float = Field(..., ge=0, description="Power in Watts")
    healthy: bool = Field(..., description="Sensor health flag")
class Ina228Data(BaseModel):
    """Telemetry data for a single INA228 sensor."""

    voltage: float = Field(..., description="Bus voltage in Volts")
    current: float = Field(..., description="Current in Amperes")


class Ina228SensorsData(BaseModel):
    """Telemetry data for all INA228 sensors."""

    left_hip: Ina228Data
    left_knee: Ina228Data
    right_hip: Ina228Data
    right_knee: Ina228Data


class Ina228AlertData(BaseModel):
    """Alert state for a single INA228 sensor."""

    voltage: Optional[AlertSeverity] = Field(
        default=None, description="Alert severity for sensor voltage"
    )
    current: Optional[AlertSeverity] = Field(
        default=None, description="Alert severity for sensor current"
    )


class Ina228AlertsData(BaseModel):
    """Alert states for all INA228 sensors."""

    left_hip: Ina228AlertData
    left_knee: Ina228AlertData
    right_hip: Ina228AlertData
    right_knee: Ina228AlertData


class PowerData(BaseModel):
    """Power system telemetry data."""

    battery_percentage: float = Field(
        ..., ge=0, le=100, description="Battery charge level (0-100%)"
    )
    battery_voltage: float = Field(..., description="Battery voltage in Volts")
    current_draw: float = Field(..., description="Total current draw in Amperes")
    sensors: List[SensorReading] = Field(
        default_factory=list, description="Raw readings from INA228 sensors (empty if using mock data)"
    )
    is_stale: bool = Field(default=False, description="True if sensor data is stale")
    relay1: bool = Field(default=False, description="Relay 1 state")
    relay2: bool = Field(default=False, description="Relay 2 state")
    relay3: bool = Field(default=False, description="Relay 3 state")
    relay4: bool = Field(default=False, description="Relay 4 state")
    relay5: bool = Field(default=False, description="Relay 5 state")
    relay6: bool = Field(default=False, description="Relay 6 state")
    relay7: bool = Field(default=False, description="Relay 7 state")


class PowerUpdate(BaseModel):
    """Power data received from MCU via serial bridge (5 INA228 sensors)."""

    sensors: List[SensorReading] = Field(
        ...,
        min_length=5,
        max_length=5,
        description="Readings from 5 INA228 power sensors"
    )
    relay1: bool = Field(default=False, description="Relay 1 state")
    relay2: bool = Field(default=False, description="Relay 2 state")
    relay3: bool = Field(default=False, description="Relay 3 state")
    relay4: bool = Field(default=False, description="Relay 4 state")
    relay5: bool = Field(default=False, description="Relay 5 state")
    relay6: bool = Field(default=False, description="Relay 6 state")
    relay7: bool = Field(default=False, description="Relay 7 state")


class SystemData(BaseModel):
    """System health and status data."""

    health_status: SystemHealthStatus = Field(..., description="Overall system health")
    emergency_stop: bool = Field(..., description="Emergency stop activated")
    error_messages: List[str] = Field(
        default_factory=list, description="Active error messages"
    )
    uptime_seconds: float = Field(..., description="System uptime in seconds")


class AlertsData(BaseModel):
    """Alert state payload for telemetry."""

    motors: MotorsAlertsData
    ina228: Ina228AlertsData


class TelemetryData(BaseModel):
    """Complete telemetry data packet sent over WebSocket."""

    timestamp: datetime = Field(..., description="ISO 8601 timestamp")
    sequence: int = Field(..., description="Packet sequence number")
    joints: JointsData
    motors: MotorsData
    sensors: SensorsData
    ina228: Ina228SensorsData
    power: PowerData
    system: SystemData
    alerts: AlertsData

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
