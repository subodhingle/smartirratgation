 Hardware Connection Instructions
Components Needed:
Arduino Uno/Nano

Soil Moisture Sensor (YL-69 or similar)

Relay Module (5V)

Water Pump (3-12V DC)

Jumper Wires

Breadboard

Wiring Diagram:
Soil Moisture Sensor:

VCC → 5V

GND → GND

A0 → Arduino A0

Relay Module:

VCC → 5V

GND → GND

IN → Digital Pin 7

Water Pump:

Positive → Relay NO (Normally Open)

Negative → GND

Power Source → External 5-12V supply (don't power pump from Arduino)

🚀 Installation & Setup
Step 1: Install Python Dependencies
bash
pip install flask pyserial requests
Step 2: Upload Arduino Code
Open Arduino IDE

Connect Arduino via USB

Upload smart_irrigation.ino sketch

Note the COM port (Windows) or /dev/tty* (Linux/Mac)

Step 3: Configure Serial Port
In arduino_reader.py, change the port:

python
# For Windows:
arduino_reader = ArduinoReader(port='COM3')

# For Linux/Mac:
arduino_reader = ArduinoReader(port='/dev/ttyUSB0')
Step 4: Run the System
bash
python app.py
Step 5: Access Dashboard
Open your browser and go to: http://127.0.0.1:5000

🎯 How It Works
Arduino continuously reads soil moisture and controls the pump based on thresholds

Python reads Arduino data via serial and stores it in memory

Flask serves a web dashboard that displays real-time data

Frontend uses AJAX to auto-refresh data every 2 seconds

Chart.js displays historical moisture trends

Automatic Control: Pump turns ON when moisture < 30%, OFF when > 60%

⚙️ Calibration Tips
Test your soil moisture sensor in dry air (0%) and water (100%) to find actual range

Adjust the mapping values in Arduino code:

cpp
soilMoisturePercent = map(soilMoistureValue, YOUR_DRY_VALUE, YOUR_WET_VALUE, 0, 100);
Modify thresholds based on your plants' needs:

cpp
const int DRY_THRESHOLD = 30;  // Adjust as needed
const int WET_THRESHOLD = 60; // Adjust as needed
The system is now ready to run! You'll see real-time moisture readings, pump status, and a beautiful chart showing moisture trends over time.
