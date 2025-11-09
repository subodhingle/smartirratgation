"""
Smart Irrigation System - Flask Web Dashboard
Provides web interface to monitor and control the irrigation system
Integrated with Arduino serial communication
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
from threading import Lock, Thread
import serial
import serial.tools.list_ports
import json
import time

app = Flask(__name__)
CORS(app)

_lock = Lock()

# Serial connection configuration
SERIAL_PORT = 'COM6'
BAUD_RATE = 9600
ser = None

def init_serial():
    """Initialize serial connection with retries"""
    global ser
    max_attempts = 3
    
    # First, make sure any existing connection is closed
    if ser is not None:
        try:
            ser.close()
        except:
            pass
        ser = None
        time.sleep(1)  # Wait for port to be released
    
    # Try to open the port with different parameters
    for attempt in range(max_attempts):
        try:
            # Try to open with exclusive access
            ser = serial.Serial(
                port=SERIAL_PORT,
                baudrate=BAUD_RATE,
                timeout=1,
                write_timeout=1,
                exclusive=True
            )
            print(f"Successfully connected to Arduino on {SERIAL_PORT}")
            time.sleep(2)  # Give Arduino time to reset
            return True
        except serial.SerialException as e:
            print(f"Attempt {attempt + 1}/{max_attempts}: Failed to connect to Arduino: {e}")
            if "PermissionError" in str(e):
                print("Permission denied. Please try:")
                print("1. Close Arduino IDE and any other programs using the port")
                print("2. Unplug and replug the Arduino")
                print("3. Run this program with administrator privileges")
            time.sleep(1)
            
            # Try to clean up
            if ser is not None:
                try:
                    ser.close()
                except:
                    pass
                ser = None
    return False

# Store system status
system_status = {
    'auto_mode': True,
    'manual_override': False,
    'manual_pump_status': False
}

# Current sensor data and system state
_sensor_data = {
    "moisture": None,
    "raw_value": None,
    "pump_status": False,
    "threshold_low": 30,
    "threshold_high": 60
}
_system_status = {"auto_mode": True}
_history = []  # list of {"timestamp": iso_str, "moisture": value}
_MAX_HISTORY = 500

def read_arduino_data():
    """
    Background thread function to continuously read data from Arduino
    """
    global ser
    
    while True:
        try:
            # Try to initialize serial if not connected
            if ser is None or not ser.is_open:
                if not init_serial():
                    print("Failed to connect to Arduino, retrying in 5 seconds...")
                    time.sleep(5)
                    continue

            if ser.in_waiting > 0:
                try:
                    # Read line from Arduino
                    data = ser.readline().decode('utf-8', errors='replace').strip()
                    print(f"Received from Arduino: {data}")
                    
                    # Try to parse as JSON
                    try:
                        payload = json.loads(data)
                        
                        # Update sensor data with lock
                        with _lock:
                            # Update sensor data fields that exist in payload
                            for k in ("moisture", "raw_value", "pump_status", "threshold_low", "threshold_high"):
                                if k in payload:
                                    _sensor_data[k] = payload[k]
                            
                            # Append to history
                            if _sensor_data.get("moisture") is not None:
                                _history.append({
                                    "timestamp": datetime.utcnow().isoformat() + "Z",
                                    "moisture": _sensor_data.get("moisture")
                                })
                                
                                # Truncate history if needed
                                if len(_history) > _MAX_HISTORY:
                                    del _history[0: len(_history) - _MAX_HISTORY]
                        
                        print(f"Updated sensor data: moisture={_sensor_data.get('moisture')}%, pump={_sensor_data.get('pump_status')}")
                        
                    except json.JSONDecodeError:
                        # If not JSON, just log it as raw data
                        print(f"Non-JSON data: {data}")
                        
                except Exception as e:
                    print(f"Error reading/parsing data: {e}")
            
            time.sleep(0.1)  # Small delay to prevent CPU spinning
            
        except serial.SerialException as e:
            print(f"Serial connection error: {e}")
            if ser:
                try:
                    ser.close()
                except:
                    pass
                ser = None
            time.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)  # Wait before retrying

def send_command_to_arduino(command):
    """Send a command to Arduino"""
    global ser
    
    try:
        if ser and ser.is_open:
            command_str = json.dumps(command) + "\n"
            ser.write(command_str.encode())
            print(f"Sent to Arduino: {command_str.strip()}")
            return True
    except Exception as e:
        print(f"Error sending command: {e}")
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """Main API endpoint to get current sensor data and system status"""
    with _lock:
        return jsonify({
            "sensor_data": _sensor_data,
            "system_status": _system_status,
            "history": _history[-20:]  # Return last 20 readings
        })

@app.route('/api/control', methods=['POST'])
def control():
    """API endpoint to control the system"""
    global _system_status
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    with _lock:
        # Handle auto mode toggle
        if 'auto_mode' in data:
            auto_mode = bool(data['auto_mode'])
            _system_status['auto_mode'] = auto_mode
            
            # Send command to Arduino
            send_command_to_arduino({"auto_mode": auto_mode})

        # Handle manual pump control
        if 'manual_pump' in data and not _system_status.get('auto_mode', True):
            manual_pump = bool(data['manual_pump'])
            system_status['auto_mode'] = False
            
            # Send command to Arduino
            send_command_to_arduino({"manual_pump": manual_pump, "auto_mode": False})

    return jsonify({"ok": True, "system_status": _system_status, "sensor_data": _sensor_data})

@app.route('/api/history')
def get_history():
    """API endpoint to get full data history"""
    with _lock:
        return jsonify(list(_history))

@app.route('/api/status')
def get_status():
    """Check if Arduino connection is active"""
    global ser
    is_connected = ser is not None and ser.is_open
    return jsonify({
        "arduino_connected": is_connected,
        "port": SERIAL_PORT,
        "baud_rate": BAUD_RATE
    })

def list_com_ports():
    """List available COM ports"""
    ports = list(serial.tools.list_ports.comports())
    print("\nAvailable COM ports:")
    for port in ports:
        print(f"  - {port.device}: {port.description}")

if __name__ == '__main__':
    print("="*60)
    print("Smart Irrigation System - Starting...")
    print("="*60)
    
    # List available COM ports
    list_com_ports()
    
    # Start Arduino reader thread
    arduino_thread = Thread(target=read_arduino_data, daemon=True)
    arduino_thread.start()
    print(f"Arduino reader thread started")
    
    # Give the serial connection a moment to establish
    time.sleep(2)
    
    print("\n" + "="*60)
    print("Flask Dashboard starting...")
    print("Dashboard available at: http://127.0.0.1:5000")
    print("="*60)
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        if ser and ser.is_open:
            ser.close()
        print("Server stopped.")