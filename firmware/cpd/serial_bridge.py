"""
Reads JSON batches from the CPD via Serial and forwards them to the TerraSafe API.

Usage:
    python serial_bridge.py              # uses defaults below
    python serial_bridge.py COM9 115200  # override port and baud

Dependencies:
    pip install pyserial requests
"""

import json
import sys
import time
import serial
import requests

PORT    = "COM8"
BAUD    = 9600
API_URL = "http://127.0.0.1:8000/api/v1/cpd/batch"

RECONNECT_DELAY = 3  # seconds between reconnect attempts


def run_loop(port: str, baud: int):
    while True:
        try:
            print(f"Connecting to {port} at {baud} baud...")
            with serial.Serial(port, baud, timeout=1) as ser:
                print(f"Listening. Forwarding to {API_URL}\n")
                while True:
                    try:
                        line = ser.readline().decode("utf-8", errors="ignore").strip()
                    except serial.SerialException as e:
                        print(f"[serial error] {e}")
                        break

                    if not line:
                        continue

                    if not line.startswith("{"):
                        print(f"[cpd] {line}")
                        continue

                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError as e:
                        print(f"[json error] {e} | raw: {line}")
                        continue

                    try:
                        r = requests.post(API_URL, json=payload, timeout=5)
                        print(f"[POST {r.status_code}] {r.text.strip()}")
                    except requests.RequestException as e:
                        print(f"[http error] {e}")

        except serial.SerialException as e:
            print(f"[serial error] {e}")

        print(f"[reconnect] retrying in {RECONNECT_DELAY}s...")
        time.sleep(RECONNECT_DELAY)


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else PORT
    baud = int(sys.argv[2]) if len(sys.argv) > 2 else BAUD

    try:
        run_loop(port, baud)
    except KeyboardInterrupt:
        print("\n[exit] stopped by user")


if __name__ == "__main__":
    main()
