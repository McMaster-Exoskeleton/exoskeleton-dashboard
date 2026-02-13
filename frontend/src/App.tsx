import { useEffect } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import { JointName, JOINT_NAMES } from './types/telemetry';

function App() {
  // Get WebSocket URL from environment variable or use default
  const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
  const { telemetry, isConnected, error, connectionState } = useWebSocket(wsUrl);

  // Log telemetry data to console for debugging
  useEffect(() => {
    if (telemetry) {
      console.log('Telemetry Update:', telemetry);
    }
  }, [telemetry]);

  // Format uptime as HH:MM:SS
  const formatUptime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Get color class based on connection state
  const getConnectionColor = () => {
    switch (connectionState) {
      case 'connected':
        return 'text-green-400';
      case 'connecting':
        return 'text-yellow-400';
      case 'error':
        return 'text-red-400';
      case 'disconnected':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  // Get color class based on system health status
  const getHealthColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-400';
      case 'degraded':
        return 'text-yellow-400';
      case 'critical':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  // Get color class based on motor status
  const getMotorStatusColor = (status: string) => {
    switch (status) {
      case 'ok':
        return 'text-green-400';
      case 'warning':
        return 'text-yellow-400';
      case 'error':
        return 'text-red-400';
      case 'offline':
        return 'text-gray-400';
      default:
        return 'text-gray-400';
    }
  };

  // Get battery level color based on percentage
  const getBatteryColor = (percentage: number) => {
    if (percentage > 50) return 'text-green-400';
    if (percentage > 20) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Exoskeleton Telemetry Dashboard</h1>

        {/* Connection Status */}
        <div className="flex items-center gap-2">
          <span className="text-gray-400">Status:</span>
          <span className={`font-semibold ${getConnectionColor()}`}>
            {connectionState.toUpperCase()}
            {connectionState === 'connecting' && (
              <span className="ml-2 inline-block animate-pulse">●</span>
            )}
          </span>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-2 p-3 bg-red-900/30 border border-red-500 rounded text-red-300">
            <strong>Error:</strong> {error}
          </div>
        )}
      </div>

      {/* Telemetry Data Display */}
      {!isConnected && !telemetry && (
        <div className="text-center text-gray-400 py-12">
          {connectionState === 'connecting' && (
            <div>
              <div className="text-4xl mb-4">⟳</div>
              <p>Connecting to WebSocket server...</p>
            </div>
          )}
          {connectionState === 'disconnected' && (
            <div>
              <div className="text-4xl mb-4">✕</div>
              <p>Disconnected from server</p>
            </div>
          )}
          {connectionState === 'error' && (
            <div>
              <div className="text-4xl mb-4">⚠</div>
              <p>Connection error - please check backend server</p>
            </div>
          )}
        </div>
      )}

      {telemetry && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* System Status Section */}
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h2 className="text-xl font-bold mb-4 text-blue-400">System Status</h2>

            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-400">Health:</span>
                <span className={`font-semibold ${getHealthColor(telemetry.system.health_status)}`}>
                  {telemetry.system.health_status.toUpperCase()}
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-gray-400">Emergency Stop:</span>
                <span className={`font-semibold ${telemetry.system.emergency_stop ? 'text-red-400 animate-pulse' : 'text-green-400'}`}>
                  {telemetry.system.emergency_stop ? '🚨 ACTIVE' : 'Inactive'}
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-gray-400">Uptime:</span>
                <span className="font-mono">{formatUptime(telemetry.system.uptime_seconds)}</span>
              </div>

              <div className="flex justify-between">
                <span className="text-gray-400">Sequence:</span>
                <span className="font-mono">#{telemetry.sequence}</span>
              </div>

              {telemetry.system.error_messages.length > 0 && (
                <div className="mt-4 p-3 bg-red-900/30 border border-red-500 rounded">
                  <div className="text-red-300 font-semibold mb-2">Active Errors:</div>
                  <ul className="list-disc list-inside text-red-300 text-sm">
                    {telemetry.system.error_messages.map((msg, idx) => (
                      <li key={idx}>{msg}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Power Section */}
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h2 className="text-xl font-bold mb-4 text-blue-400">Power System</h2>

            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-400">Battery:</span>
                <span className={`font-semibold ${getBatteryColor(telemetry.power.battery_percentage)}`}>
                  {telemetry.power.battery_percentage.toFixed(1)}%
                </span>
              </div>

              {/* Battery Visual Indicator */}
              <div className="w-full bg-gray-700 rounded-full h-4 overflow-hidden">
                <div
                  className={`h-full transition-all duration-300 ${
                    telemetry.power.battery_percentage > 50
                      ? 'bg-green-500'
                      : telemetry.power.battery_percentage > 20
                      ? 'bg-yellow-500'
                      : 'bg-red-500'
                  }`}
                  style={{ width: `${telemetry.power.battery_percentage}%` }}
                />
              </div>

              <div className="flex justify-between">
                <span className="text-gray-400">Voltage:</span>
                <span className="font-mono">{telemetry.power.battery_voltage.toFixed(2)} V</span>
              </div>

              <div className="flex justify-between">
                <span className="text-gray-400">Current Draw:</span>
                <span className="font-mono">{telemetry.power.current_draw.toFixed(2)} A</span>
              </div>
            </div>
          </div>

          {/* Joints Section */}
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 lg:col-span-2">
            <h2 className="text-xl font-bold mb-4 text-blue-400">Joint Telemetry</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
              {JOINT_NAMES.map((jointName: JointName) => {
                const joint = telemetry.joints[jointName];
                return (
                  <div key={jointName} className="bg-gray-700/50 p-4 rounded border border-gray-600">
                    <h3 className="font-semibold text-cyan-400 mb-3 capitalize">
                      {jointName.replace('_', ' ')}
                    </h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Position:</span>
                        <span className="font-mono">{joint.position.toFixed(3)} rad</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Velocity:</span>
                        <span className="font-mono">{joint.velocity.toFixed(3)} rad/s</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Torque:</span>
                        <span className="font-mono">{joint.torque.toFixed(2)} Nm</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Motors Section */}
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 lg:col-span-2">
            <h2 className="text-xl font-bold mb-4 text-blue-400">Motor Status</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
              {JOINT_NAMES.map((jointName: JointName) => {
                const motor = telemetry.motors[jointName];
                return (
                  <div key={jointName} className="bg-gray-700/50 p-4 rounded border border-gray-600">
                    <h3 className="font-semibold text-purple-400 mb-3 capitalize">
                      {jointName.replace('_', ' ')}
                    </h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Status:</span>
                        <span className={`font-semibold ${getMotorStatusColor(motor.status)}`}>
                          {motor.status.toUpperCase()}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Temperature:</span>
                        <span className={`font-mono ${motor.temperature > 60 ? 'text-red-400' : motor.temperature > 50 ? 'text-yellow-400' : ''}`}>
                          {motor.temperature.toFixed(1)} °C
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Current:</span>
                        <span className="font-mono">{motor.current.toFixed(2)} A</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Footer Info */}
      <div className="mt-8 text-center text-gray-500 text-sm">
        <p>Connected to: {wsUrl}</p>
        {telemetry && (
          <p className="mt-1">
            Last update: {new Date(telemetry.timestamp).toLocaleTimeString()}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
