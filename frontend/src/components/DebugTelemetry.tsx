import React from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

interface DebugTelemetryProps {
    url?: string;
}

export const DebugTelemetry: React.FC<DebugTelemetryProps> = ({ url = 'ws://localhost:8080/ws' }) => {
    const { telemetry, isConnected, error, connectionState } = useWebSocket(url);

    return (
        <div style={{ padding: '20px', border: '1px solid #ccc', margin: '20px', borderRadius: '8px', background: '#f9f9f9', color: '#333' }}>
            <h2>WebSocket Debug</h2>
            <div style={{ marginBottom: '10px' }}>
                <strong>Status:</strong> <span style={{
                    color: isConnected ? 'green' : connectionState === 'error' ? 'red' : 'orange',
                    fontWeight: 'bold'
                }}>{connectionState}</span>
            </div>

            {error && (
                <div style={{ color: 'red', marginBottom: '10px' }}>
                    <strong>Error:</strong> {error}
                </div>
            )}

            <div style={{ marginTop: '20px' }}>
                <h3>Telemetry Data:</h3>
                {telemetry ? (
                    <pre style={{ background: '#eee', padding: '10px', overflow: 'auto', maxHeight: '400px', fontSize: '12px' }}>
                        {JSON.stringify(telemetry, null, 2)}
                    </pre>
                ) : (
                    <div>No data received yet...</div>
                )}
            </div>
        </div>
    );
};
