import serial
import serial.tools.list_ports
import psutil
import os

def check_port_usage(port):
    print(f"\nChecking port {port}...")
    
    # List all ports
    ports = list(serial.tools.list_ports.comports())
    target_port = None
    
    # Find our port
    for p in ports:
        if p.device == port:
            target_port = p
            print(f"Found port: {p.device}")
            print(f"Description: {p.description}")
            print(f"Hardware ID: {p.hwid}")
            break
    
    if not target_port:
        print(f"Port {port} not found!")
        return
    
    # Try to open the port
    try:
        ser = serial.Serial(port, timeout=1)
        print("Successfully opened port!")
        ser.close()
        print("Port closed successfully")
    except Exception as e:
        print(f"Failed to open port: {e}")

if __name__ == "__main__":
    check_port_usage("COM6")