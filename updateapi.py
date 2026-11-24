import urequests
import ujson
import time
from machine import Pin, ADC
import network

# WiFi credentials
SSID     = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"

# API settings (exactly like your Python code)
API_BASE = "https://panipahraapivdb.onrender.com/"
LOCATION_ID = "location01A"  # Same as your Python script

def connect_wifi():
    """Connect to WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if wlan.isconnected():
        print('WiFi already connected')
        return True
    
    print('Connecting to WiFi...')
    wlan.connect(SSID, PASSWORD)
    
    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        print('.', end='')
        time.sleep(1)
        timeout -= 1
    
    if wlan.isconnected():
        print('\nWiFi connected! IP:', wlan.ifconfig()[0])
        return True
    else:
        print('\nWiFi connection failed')
        return False

def update_single_cooler():
    """Update ONLY ONE location - EXACTLY like your Python function"""
    
    # Read real sensor data
    water_level, ro_tds, water_temp = read_sensors()
    
    # Your exact data structure
    data = {
        "waterLevel"   : 30,
        "roTds"        : 110,
        "waterTemp"    : water_temp,
        "safety"       : "Green",
        "systemWorking": "OK"
    }
    
    url = API_BASE + "api/coolers/" + LOCATION_ID
    
    try:
        response = urequests.put(url, json=data)
        if response.status_code == 200:
            print(f"{LOCATION_ID} UPDATED!")
            print(f"Water: {data['waterLevel']} | TDS: {data['roTds']} | Temp: {data['waterTemp']}°C")
        else:
            print(f"Failed: {response.status_code}")
        response.close()
    except Exception as e:
        print(f"Error: {e}")

# Main program
if __name__ == "__main__":
    # Connect WiFi first
    if connect_wifi():
        print(f"\nStarting updates for {LOCATION_ID} every 30 seconds...")
        print("-" * 50)
        
        while True:
            update_single_cooler()
            print("-" * 50)
            time.sleep(30)  # Same interval as your water system
    else:
        print("Cannot start without WiFi")
