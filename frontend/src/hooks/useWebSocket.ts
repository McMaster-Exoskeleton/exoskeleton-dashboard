import { useState, useEffect, useRef } from 'react';
import { TelemetryData } from '../types/telemetry';

export type ConnectionState = 'connecting' | 'connected' | 'disconnected' | 'error';

interface UseWebSocketResult {
    telemetry: TelemetryData | null;
    isConnected: boolean;
    error: string | null;
    connectionState: ConnectionState;
}

export const useWebSocket = (url: string): UseWebSocketResult => {
    const [telemetry, setTelemetry] = useState<TelemetryData | null>(null);
    const [connectionState, setConnectionState] = useState<ConnectionState>('disconnected');
    const [error, setError] = useState<string | null>(null);

    const wsRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        setConnectionState('connecting');
        setError(null);

        const ws = new WebSocket(url);
        wsRef.current = ws;

        ws.onopen = () => {
            setConnectionState('connected');
            setError(null);
        };

        ws.onmessage = (event) => {
            try {
                const data: TelemetryData = JSON.parse(event.data);
                setTelemetry(data);
            } catch (err) {
                console.error('Failed to parse telemetry data:', err);
                // Optionally set error state here, but requirements say "Don't crash on malformed data"
                // strict requirement: "Catch and handle JSON parse errors"
            }
        };

        ws.onerror = (event) => {
            console.error('WebSocket error:', event);
            setConnectionState('error');
            setError('WebSocket connection error');
        };

        ws.onclose = () => {
            setConnectionState('disconnected');
            // If it closed unexpectedly, we might want to retain the error, but for now strict "disconnected" on close.
        };

        return () => {
            if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
                ws.close();
            }
        };
    }, [url]);

    return {
        telemetry,
        isConnected: connectionState === 'connected',
        error,
        connectionState,
    };
};
