#!/usr/bin/env python3
"""
Serial-to-Backend Bridge for Power MCU Data
Reads power telemetry from STM32 via UART and updates the backend.
"""

import serial
import json
import time
import sys
import requests

class PowerSerialBridge:
    def __init__(self, serial_port: str, backend_url: str = "http://localhost:8000", baudrate: int = 115200):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.backend_url = backend_url
        self.ser = None

    def connect_serial(self):
        """Connect to serial port"""
        try:
            self.ser = serial.Serial(
                port=self.serial_port,
                baudrate=self.baudrate,
                timeout=1.0
            )
            print(f"✓ Connected to {self.serial_port} at {self.baudrate} baud")
            time.sleep(2)  # Wait for MCU to stabilize
            return True
        except serial.SerialException as e:
            print(f"✗ Failed to connect to {self.serial_port}: {e}")
            return False

    def read_and_parse(self):
        """Read one line from serial and parse JSON"""
        if not self.ser or not self.ser.is_open:
            return None

        try:
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                data = json.loads(line)
                return data
        except json.JSONDecodeError:
            # Silently ignore JSON errors (common on startup)
            return None
        except UnicodeDecodeError:
            # Silently ignore unicode errors (common on startup)
            return None
        except Exception as e:
            print(f"✗ Read error: {e}")
            return None

    def update_backend(self, power_data):
        """Send power data to backend via HTTP POST"""
        try:
            response = requests.post(
                f"{self.backend_url}/power/update",
                json=power_data,
                timeout=0.5
            )
            return response.status_code == 200
        except requests.RequestException:
            # Backend not available - continue silently
            return False

    def run(self):
        """Main loop - read serial and update backend"""
        if not self.connect_serial():
            return

        print(f"Reading power data and forwarding to {self.backend_url}")
        print("Press Ctrl+C to stop\n")

        update_count = 0
        error_count = 0

        try:
            while True:
                power_data = self.read_and_parse()
                if power_data:
                    update_count += 1

                    # Display formatted output
                    print(f"[{update_count}] Sensor1: {power_data['voltage']:.2f}V {power_data['current']:.3f}A {power_data['power']:.2f}W [H:{power_data['healthy']}] | "
                          f"Sensor2: {power_data['voltage2']:.2f}V {power_data['current2']:.3f}A {power_data['power2']:.2f}W [H:{power_data['healthy2']}]", end='')

                    # Update backend
                    if self.update_backend(power_data):
                        print(" → Backend ✓")
                    else:
                        error_count += 1
                        if error_count % 10 == 1:  # Only print occasionally to avoid spam
                            print(" → Backend ✗ (not running?)")
                        else:
                            print()

                time.sleep(0.01)

        except KeyboardInterrupt:
            print(f"\n\n✓ Stopped by user")
            print(f"Total updates: {update_count}")
        finally:
            if self.ser:
                self.ser.close()
                print("✓ Serial port closed")

def main():
    # Parse command line arguments
    port = sys.argv[1] if len(sys.argv) > 1 else '/dev/ttyUSB0'
    backend = sys.argv[2] if len(sys.argv) > 2 else 'http://localhost:8000'

    print(f"Power MCU Serial Bridge")
    print(f"Port: {port}")
    print(f"Backend: {backend}")
    print(f"Baud: 115200\n")

    bridge = PowerSerialBridge(serial_port=port, backend_url=backend, baudrate=115200)
    bridge.run()

if __name__ == '__main__':
    main()
