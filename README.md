FLIE-structure


| Component | Technology Used |
|------------|-----------------|
| **Backend** | Python (Flask) |
| **Frontend** | HTML, CSS, JavaScript, Bootstrap |
| **Visualization** | Chart.js |
| **Hardware** | Arduino UNO, Soil Moisture Sensor, Relay Module, Water Pump |
| **Communication** | Serial (PySerial) |

# 🌿 Smart Irrigation System (Arduino + Python + Flask Dashboard)

A **Smart Irrigation System** that automatically controls a water pump based on **soil moisture level** and displays real-time data on a **Flask-based web dashboard**.

The system integrates **Arduino**, **Python (Flask)**, and **Chart.js** to provide efficient, data-driven irrigation — ensuring optimal water usage for sustainable agriculture.

---

## 📘 Theory / Background

Agriculture consumes over 70% of the world’s freshwater resources, making **efficient irrigation** crucial for sustainable farming.  
Traditional irrigation systems often depend on manual monitoring or fixed-timer methods, leading to **over-irrigation** (wastage) or **under-irrigation** (crop stress).

The **Smart Irrigation System** aims to solve this problem by using **soil moisture sensors** and **microcontroller automation**.  
It continuously monitors the water content in soil and activates a **relay-controlled water pump** when the soil becomes dry. Once the desired moisture level is restored, the pump is automatically turned off.

This closed-loop system ensures:
- Optimal soil moisture maintenance  
- Water conservation (up to 30–40%)  
- Reduced manual intervention  
- Improved crop health and yield  

The data collected by the Arduino is sent to a **Python Flask server** via serial communication.  
The server visualizes real-time moisture levels using **Chart.js** on a web dashboard, allowing farmers or users to monitor irrigation performance from their computers or local network.

---

## 🧰 Components Required

| Component | Quantity | Description |
|------------|-----------|-------------|
| Arduino Uno / Nano | 1 | Microcontroller board |
| Soil Moisture Sensor (YL-69 or similar) | 1 | Measures soil moisture |
| Relay Module (5V) | 1 | Controls water pump |
| Water Pump (3–12V DC) | 1 | Used for irrigation |
| Jumper Wires | — | For connections |
| Breadboard | 1 | For prototyping |

---

## ⚙️ Wiring Diagram

### 🪴 Soil Moisture Sensor
| Pin | Connects To |
|-----|--------------|
| VCC | 5V |
| GND | GND |
| A0  | Arduino A0 |

### ⚡ Relay Module
| Pin | Connects To |
|-----|--------------|
| VCC | 5V |
| GND | GND |
| IN  | Digital Pin 7 |

### 💧 Water Pump
| Pin | Connects To |
|-----|--------------|
| Positive | Relay NO (Normally Open) |
| Negative | GND |
| Power Source | External 5–12V DC *(⚠️ Do not power pump directly from Arduino)* |

---
