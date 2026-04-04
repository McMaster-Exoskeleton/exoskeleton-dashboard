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

export enum AlertSeverity {
    Warning = 'warning',
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

export interface SensorReading {
    voltage: number;
    current: number;
    power: number;
    healthy: boolean;
export interface Ina228Data {
    voltage: number;
    current: number;
}

export interface Ina228SensorsData {
    left_hip: Ina228Data;
    left_knee: Ina228Data;
    right_hip: Ina228Data;
    right_knee: Ina228Data;
}

export interface MotorAlertData {
    temperature?: AlertSeverity;
    current?: AlertSeverity;
}

export interface MotorsAlertsData {
    left_hip: MotorAlertData;
    left_knee: MotorAlertData;
    right_hip: MotorAlertData;
    right_knee: MotorAlertData;
}

export interface Ina228AlertData {
    voltage?: AlertSeverity;
    current?: AlertSeverity;
}

export interface Ina228AlertsData {
    left_hip: Ina228AlertData;
    left_knee: Ina228AlertData;
    right_hip: Ina228AlertData;
    right_knee: Ina228AlertData;
}

export interface AlertsData {
    motors: MotorsAlertsData;
    ina228: Ina228AlertsData;
}

export interface PowerData {
    battery_percentage: number;
    battery_voltage: number;
    current_draw: number;
    sensors: SensorReading[];
    is_stale: boolean;
    relay1: boolean;
    relay2: boolean;
    relay3: boolean;
    relay4: boolean;
    relay5: boolean;
    relay6: boolean;
    relay7: boolean;
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
    ina228: Ina228SensorsData;
    power: PowerData;
    system: SystemData;
    alerts: AlertsData;
}

export type JointName = 'left_hip' | 'left_knee' | 'right_hip' | 'right_knee';

export const JOINT_NAMES: JointName[] = [
    'left_hip',
    'left_knee',
    'right_hip',
    'right_knee',
];
