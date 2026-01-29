import math
import random
import time
from datetime import datetime
from typing import Dict, List

from app.models import (
    IMUData,
    JointData,
    JointsData,
    MotorData,
    MotorsData,
    MotorStatus,
    PowerData,
    SensorsData,
    SystemData,
    SystemHealthStatus,
    TelemetryData,
)


class DataCollector:

    def __init__(self, mode: str = "gait", update_rate_hz: float = 10.0):

        if mode not in ("gait", "random"):
            raise ValueError(f"Invalid mode '{mode}'. Must be 'gait' or 'random'")

        self.mode = mode
        self.update_rate_hz = update_rate_hz

        # Internal state tracking
        self._sequence = 0
        self._start_time = time.time()
        self._last_update_time = self._start_time

        # Motor status tracking
        self._motor_statuses: Dict[str, MotorStatus] = {
            "left_hip": MotorStatus.OK,
            "left_knee": MotorStatus.OK,
            "right_hip": MotorStatus.OK,
            "right_knee": MotorStatus.OK,
        }

        # System state
        self._emergency_stop = False
        self._error_messages: List[str] = []

        # Motor temperature tracking 
        self._motor_temperatures = {
            "left_hip": 25.0,
            "left_knee": 25.0,
            "right_hip": 25.0,
            "right_knee": 25.0,
        }

        # Battery tracking
        self._battery_percentage = 100.0

        # Random mode state (smooth random walk)
        self._random_positions = {
            "left_hip": 0.0,
            "left_knee": 0.0,
            "right_hip": 0.0,
            "right_knee": 0.0,
        }
        self._random_velocities = {
            "left_hip": 0.0,
            "left_knee": 0.0,
            "right_hip": 0.0,
            "right_knee": 0.0,
        }

    def get_telemetry(self) -> TelemetryData:
        # Enforce update rate by sleeping if called too quickly
        current_time = time.time()
        time_since_last_call = current_time - self._last_update_time
        expected_interval = 1.0 / self.update_rate_hz
        
        if time_since_last_call < expected_interval:
            sleep_duration = expected_interval - time_since_last_call
            time.sleep(sleep_duration)
            current_time = time.time()
            time_since_last_call = current_time - self._last_update_time
        
        self._last_update_time = current_time

        # Generate joint data based on mode
        joints = self._generate_joints(time_since_last_call)

        # Generate motor data (correlated with joint torque)
        motors = self._generate_motors(joints)

        # Generate sensor data (correlated with joint movement)
        sensors = self._generate_sensors(joints)

        # Generate power data
        power = self._generate_power(current_time, motors)

        # Generate system data
        system = self._generate_system(current_time, motors)

        # Create telemetry packet
        telemetry = TelemetryData(
            timestamp=datetime.now(),
            sequence=self._sequence,
            joints=joints,
            motors=motors,
            sensors=sensors,
            power=power,
            system=system,
        )

        self._sequence += 1
        return telemetry

    def set_motor_status(self, joint: str, status: MotorStatus) -> None:
        """
        Manually set motor status for testing warnings/errors.

        Args:
            joint: Joint name ("left_hip", "left_knee", "right_hip", "right_knee")
            status: MotorStatus value
        """
        if joint not in self._motor_statuses:
            raise ValueError(f"Invalid joint '{joint}'")
        self._motor_statuses[joint] = status

    def set_emergency_stop(self, active: bool) -> None:
   
        self._emergency_stop = active


    def add_error_message(self, message: str) -> None:

         self._error_messages.append(message)


    def clear_error_messages(self) -> None:
        self._error_messages.clear()

    def reset(self) -> None:

        self._sequence = 0
        self._start_time = time.time()
        self._last_update_time = self._start_time
        self._motor_statuses = {
            "left_hip": MotorStatus.OK,
            "left_knee": MotorStatus.OK,
            "right_hip": MotorStatus.OK,
            "right_knee": MotorStatus.OK,
        }

        self._emergency_stop = False
        self._error_messages.clear()
        self._motor_temperatures = {
            "left_hip": 25.0,
            "left_knee": 25.0,
            "right_hip": 25.0,
            "right_knee": 25.0,
        }
        self._battery_percentage = 100.0
        self._random_positions = {
            "left_hip": 0.0,
            "left_knee": 0.0,
            "right_hip": 0.0,
            "right_knee": 0.0,
        }
        self._random_velocities = {
            "left_hip": 0.0,
            "left_knee": 0.0,
            "right_hip": 0.0,
            "right_knee": 0.0,
        }

                                            # Private methods for data generation

    def _generate_joints(self, dt: float) -> JointsData:
        """Generate joint data based on current mode."""
        if self.mode == "gait":
            return self._generate_gait_joints()
        else:
            return self._generate_random_joints(dt)

    def _generate_gait_joints(self) -> JointsData:
        """Generate realistic walking gait joint patterns."""
        # Time since start 
        elapsed_total = time.time() - self._start_time

        # Gait frequency: ~1 Hz 
        gait_freq = 1.0
        phase = 2 * math.pi * gait_freq * elapsed_total

        # Hip joints: primary oscillation
        hip_amplitude = 0.5  # radians
        left_hip_pos = hip_amplitude * math.sin(phase)
        right_hip_pos = hip_amplitude * math.sin(phase + math.pi)  # 180° out of phase

        # Knee joints: phase-offset from hips, slightly larger amplitude
        knee_amplitude = 0.6
        knee_phase_offset = math.pi / 4  # 45° offset
        left_knee_pos = knee_amplitude * math.sin(phase + knee_phase_offset)
        right_knee_pos = knee_amplitude * math.sin(phase + math.pi + knee_phase_offset)

        # Velocities: derivative of position + small noise
        vel_factor = hip_amplitude * 2 * math.pi * gait_freq
        left_hip_vel = vel_factor * math.cos(phase) + self._noise(0.1)
        right_hip_vel = vel_factor * math.cos(phase + math.pi) + self._noise(0.1)

        vel_factor_knee = knee_amplitude * 2 * math.pi * gait_freq
        left_knee_vel = vel_factor_knee * math.cos(phase + knee_phase_offset) + self._noise(0.1)
        right_knee_vel = (
            vel_factor_knee * math.cos(phase + math.pi + knee_phase_offset) + self._noise(0.1)
        )

        # Torques: correlated with velocity, clamped to range
        left_hip_torque = self._clamp(left_hip_vel * 15.0 + self._noise(1.0), -30.0, 30.0)
        right_hip_torque = self._clamp(right_hip_vel * 15.0 + self._noise(1.0), -30.0, 30.0)
        left_knee_torque = self._clamp(left_knee_vel * 15.0 + self._noise(1.0), -30.0, 30.0)
        right_knee_torque = self._clamp(right_knee_vel * 15.0 + self._noise(1.0), -30.0, 30.0)

        return JointsData(
            left_hip=JointData(
                position=self._clamp(left_hip_pos, -math.pi, math.pi),
                velocity=self._clamp(left_hip_vel, -2.0, 2.0),
                torque=left_hip_torque,
            ),
            right_hip=JointData(
                position=self._clamp(right_hip_pos, -math.pi, math.pi),
                velocity=self._clamp(right_hip_vel, -2.0, 2.0),
                torque=right_hip_torque,
            ),
            left_knee=JointData(
                position=self._clamp(left_knee_pos, -math.pi, math.pi),
                velocity=self._clamp(left_knee_vel, -2.0, 2.0),
                torque=left_knee_torque,
            ),
            right_knee=JointData(
                position=self._clamp(right_knee_pos, -math.pi, math.pi),
                velocity=self._clamp(right_knee_vel, -2.0, 2.0),
                torque=right_knee_torque,
            ),
        )

    def _generate_random_joints(self, dt: float) -> JointsData:
        """Generate smooth random joint variations using random walk."""
        joints_list = ["left_hip", "left_knee", "right_hip", "right_knee"]

        for joint in joints_list:
            # Random walk with smoothing
            random_accel = self._noise(0.5)
            self._random_velocities[joint] += random_accel * dt
            self._random_velocities[joint] = self._clamp(self._random_velocities[joint], -2.0, 2.0)

            # Update position
            self._random_positions[joint] += self._random_velocities[joint] * dt
            self._random_positions[joint] = self._clamp(
                self._random_positions[joint], -math.pi, math.pi
            )

        # Generate torques correlated with velocities
        left_hip_torque = self._clamp(self._random_velocities["left_hip"] * 15.0 + self._noise(1.0), -30.0, 30.0)
        right_hip_torque = self._clamp(self._random_velocities["right_hip"] * 15.0 + self._noise(1.0), -30.0, 30.0)
        left_knee_torque = self._clamp(self._random_velocities["left_knee"] * 15.0 + self._noise(1.0), -30.0, 30.0)
        right_knee_torque = self._clamp(self._random_velocities["right_knee"] * 15.0 + self._noise(1.0), -30.0, 30.0)

        return JointsData(
            left_hip=JointData(
                position=self._random_positions["left_hip"],
                velocity=self._random_velocities["left_hip"],
                torque=left_hip_torque,
            ),
            right_hip=JointData(
                position=self._random_positions["right_hip"],
                velocity=self._random_velocities["right_hip"],
                torque=right_hip_torque,
            ),
            left_knee=JointData(
                position=self._random_positions["left_knee"],
                velocity=self._random_velocities["left_knee"],
                torque=left_knee_torque,
            ),
            right_knee=JointData(
                position=self._random_positions["right_knee"],
                velocity=self._random_velocities["right_knee"],
                torque=right_knee_torque,
            ),
        )

    def _generate_motors(self, joints: JointsData) -> MotorsData:
        """Generate motor data correlated with joint torques."""
        motor_joints = {
            "left_hip": joints.left_hip,
            "right_hip": joints.right_hip,
            "left_knee": joints.left_knee,
            "right_knee": joints.right_knee,
        }

        motors_dict = {}
        for joint_name, joint_data in motor_joints.items():
            # Current correlated with torque magnitude
            current = self._clamp(
                abs(joint_data.torque) * 0.3 + 2.0 + self._noise(0.5), 0.5, 15.0
            )

            # Temperature thermal model: slowly approaches target based on current draw
            target_temp = 45.0 + abs(current) * 0.5  # Baseline 45°C + variation with load
            temp_diff = target_temp - self._motor_temperatures[joint_name]
            self._motor_temperatures[joint_name] += temp_diff * 0.05  # Slow thermal response

            motors_dict[joint_name] = MotorData(
                current=current,
                temperature=self._clamp(self._motor_temperatures[joint_name], 25.0, 65.0),
                status=self._motor_statuses[joint_name],
            )

        return MotorsData(
            left_hip=motors_dict["left_hip"],
            right_hip=motors_dict["right_hip"],
            left_knee=motors_dict["left_knee"],
            right_knee=motors_dict["right_knee"],
        )

    def _generate_sensors(self, joints: JointsData) -> SensorsData:
        """Generate IMU sensor data correlated with joint movement."""
        # Gyroscope correlated with joint velocities
        # Acceleration includes gravity (~-9.8 m/s² on y-axis)
        sensors_dict = {}

        joint_vels = {
            "left_hip": joints.left_hip.velocity,
            "right_hip": joints.right_hip.velocity,
            "left_knee": joints.left_knee.velocity,
            "right_knee": joints.right_knee.velocity,
        }

        for joint_name, vel in joint_vels.items():
            # Gyroscope: correlated with joint velocity
            gyr_x = self._clamp(vel * 0.3 + self._noise(0.1), -1.0, 1.0)
            gyr_y = self._clamp(vel * 0.2 + self._noise(0.1), -1.0, 1.0)
            gyr_z = self._clamp(vel * 0.25 + self._noise(0.1), -1.0, 1.0)

            # Acceleration: includes gravity on y-axis
            acc_x = self._clamp(self._noise(0.5), -2.0, 2.0)
            acc_y = self._clamp(-9.8 + self._noise(0.3), -11.0, -8.0)
            acc_z = self._clamp(self._noise(0.5), -2.0, 2.0)

            sensors_dict[joint_name] = IMUData(
                acceleration=[acc_x, acc_y, acc_z],
                gyroscope=[gyr_x, gyr_y, gyr_z],
            )

        return SensorsData(
            left_hip=sensors_dict["left_hip"],
            right_hip=sensors_dict["right_hip"],
            left_knee=sensors_dict["left_knee"],
            right_knee=sensors_dict["right_knee"],
        )

    def _generate_power(self, current_time: float, motors: MotorsData) -> PowerData:
        """Generate power system data."""
        # Battery depletes over time (~0.01%/sec), wraps to 100 at 20%
        elapsed = current_time - self._start_time
        depletion = elapsed * 0.01  
        self._battery_percentage = 100.0 - depletion

        if self._battery_percentage <= 20.0:
            self._battery_percentage = 100.0

        # Battery voltage correlated with percentage
        battery_voltage = 22.0 + (self._battery_percentage / 100.0) * 4.0

        # Current draw is sum of motor currents plus baseline
        baseline_current = 5.0
        total_motor_current = (
            motors.left_hip.current +
            motors.right_hip.current +
            motors.left_knee.current +
            motors.right_knee.current
        )
        current_draw = self._clamp(baseline_current + total_motor_current, 5.0, 35.0)

        return PowerData(
            battery_percentage=self._battery_percentage,
            battery_voltage=battery_voltage,
            current_draw=current_draw,
        )

    def _generate_system(self, current_time: float, motors: MotorsData) -> SystemData:
        """Generate system health and status data."""
        # Determine health status
        health_status = SystemHealthStatus.HEALTHY

        if self._emergency_stop:
            health_status = SystemHealthStatus.CRITICAL
        else:
            # Check motor statuses
            motor_statuses = [
                motors.left_hip.status,
                motors.right_hip.status,
                motors.left_knee.status,
                motors.right_knee.status,
            ]

            if any(status == MotorStatus.ERROR for status in motor_statuses):
                health_status = SystemHealthStatus.CRITICAL
            elif any(status == MotorStatus.WARNING for status in motor_statuses):
                health_status = SystemHealthStatus.DEGRADED

        uptime = current_time - self._start_time

        return SystemData(
            health_status=health_status,
            emergency_stop=self._emergency_stop,
            error_messages=self._error_messages.copy(),
            uptime_seconds=uptime,
        )



    @staticmethod
    def _noise(amplitude: float) -> float:
        """Generate small random noise with given amplitude."""
        return random.uniform(-amplitude, amplitude)

    @staticmethod
    def _clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp a value between min and max."""
        return max(min_val, min(max_val, value))
