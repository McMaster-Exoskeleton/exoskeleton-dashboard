// A bunch of types for telemetry data
// Exporting them all at once to make it easier to import
export enum MotorStatus {
    Ok = 'ok',
    Warning = 'warning',
    Error = 'error',
    Offline = 'offline',
}

export enum SystemHealthStatus {
    Healthy = 'healthy',
    Degraded = 'degraded',
    Critical = 'critical',
}

export interface JointData {
    position: number;
    velocity: number;
    torque: number;
}

export interface JointsData {
    left_hip: JointData;
    left_knee: JointData;
    right_hip: JointData;
    right_knee: JointData;
}

export interface MotorData {
    current: number;
    temperature: number;
    status: MotorStatus;
}

export interface MotorsData {
    left_hip: MotorData;
    left_knee: MotorData;
    right_hip: MotorData;
    right_knee: MotorData;
}

export interface IMUData {
    acceleration: [number, number, number];
    gyroscope: [number, number, number];
}

export interface SensorsData {
    left_hip: IMUData;
    left_knee: IMUData;
    right_hip: IMUData;
    right_knee: IMUData;
}

export interface PowerData {
    battery_percentage: number;
    battery_voltage: number;
    current_draw: number;
}

export interface SystemData {
    health_status: SystemHealthStatus;
    emergency_stop: boolean;
    error_messages: string[];
    uptime_seconds: number;
}

export interface TelemetryData {
    timestamp: string;
    sequence: number;
    joints: JointsData;
    motors: MotorsData;
    sensors: SensorsData;
    power: PowerData;
    system: SystemData;
}

export type JointName = 'left_hip' | 'left_knee' | 'right_hip' | 'right_knee';

export const JOINT_NAMES: JointName[] = [
    'left_hip',
    'left_knee',
    'right_hip',
    'right_knee',
];
