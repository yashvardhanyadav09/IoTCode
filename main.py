# ------------------------------------------------------------------------------
# --  main.py
# ------------------------------------------------------------------------------
# --  Updated on : 07 Dec 2025
# --  Updated by : Yashvardhan Yadav & Subrajoyti Das
# --  Status     : Under Progress
# --               Cooler and RO on/Off in working
# ------------------------------------------------------------------------------
# --  This is Main file of the NeerNetra (Water Point Controller) App
# --  WiFi Data Communication enabled 
# --  ESP_Connection_Mode : WiFi
# -----------------------------------------------------------------------------
# --  Rest Functioning is same
# --  Controls the entire Hardware
# --  Additional Feature added to monitor & Display : MotorRelay Pin Status
# -----------------------------------------------------------------------------
""" Class   -   Main
    Purpose -   This is Main file of the NeerNetra app
                WiFi Data Communication enabled 
                ESP_Connection_Mode : WiFi
                Reads Data from all sensors and updates the API
"""
__author__  = 'Yashvardhan Yadav & Subrajoyti Das'
__Version__ = "main.2025.12.01"

# importing modules

import urequests
import ujson
import network
import machine
import time, sys, _thread
import DeviceHandler
import SensorHandler

SSID     = "WiFi-SSID"
PASSWORD = "WiFi-Password"

# API settings (exactly like your Python code)
API_BASE = "https://panipahraapivdb.onrender.com/"
LOCATION_ID = "location01A"  # Same as your Python script

Relay_Ops_Delay_Time = 5
# Sleep delay in seconds

# Pin Settings
# ========== PIN DEFINITIONS ==========
# Digital Outputs (Relays/Pumps)
Pin_Cooler      = 25  # GPIO25 - Relay/Pump 1
Pin_RO          = 26  # GPIO26 - Relay/Pump 2

# Analog Inputs (Sensors)
Pin_Water_Level = 34   # GPIO34 - Water Level
Pin_Water_Temp  = 35   # GPIO35 - Water Temp  
Pin_Water_TDS   = 36   # GPIO36 - Water TDS
Pin_Water_Flow  = 39   # GPIO39 - Water Consumed

# ST7789 LCD (6 pins)
Pin_TFT_CLK     = 18     # SCK
Pin_TFT_MOSI    = 14     # MOSI (changed from 19)
Pin_TFT_RST     = 27     # Reset (changed from 15)
Pin_TFT_DC      = 33     # Data/Command (changed from 2)
Pin_TFT_CS      =  5     # Chip Select


# -----------Initialising Devices/Sensors-------------
myDevices  = DeviceHandler.DeviceControl()
mySensors  = SensorHandler.SensorHandler()
# -------------Sensor Initilisation Completed ------

#-----------------Wifi Connection ------------------
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
#-----------------------------------------------------------------
def send_data_to_api():
    if connect_wifi():
        # Check if Wifi Connection is available
        print(f"\nSending update to NeerNetra-IoT-API-Server for {LOCATION_ID} .\n","-" * 50)
        
        """Update my data to API-Server """
        # Prepare Data to be uploaded
        data = {
            "waterLevel"   : Cooler_Water_Tank_Level,
            "roTds"        : Water_TDS,
            "waterTemp"    : Water_Temperature,
            "safety"       : "Green",
            "systemWorking": "OK"
        }
        
        url = API_BASE + "api/coolers/" + LOCATION_ID
        
        try:
            response = urequests.put(url, json=data)
            if response.status_code == 200:
                print(f"{LOCATION_ID} UPDATED!")
                print(f"Water: {data['Cooler_Water_Tank_Level']} | TDS: {data['Water_TDS']} | Temp: {data['Water_Temperature']}°C")
            else:
                print(f"Failed: {response.status_code}")
            response.close()
        except Exception as e:
            print(f"Error: {e}")     
        print("--------- API Data Updat completed----------", "-" * 50)
    else:
        print("Cannot start without WiFi")

#---------------------- Main Program ---------------------------------- 
running_Count = 1
while True :
    print (f"------------- Cycle{running_Count}-------------")
    #------------------------------------------------------------------
    # Measure Water Temperature in Cooler and set Cooler Refridgeration
    #------------------------------------------------------------------
    Water_Temperature =  mySensors.get_water_temperature ()
    print (f"Water Temperature :{Water_Temperature}")
    
    # Setting Cooler 
    if  Water_Temperature > 25 :
        print (f"Cooler Turned on at {Water_Temperature}")
        myDevices.Set_Cooler_On ()
    elif Water_Temperature < 14 :
        print (f"Cooler Turned off at {Water_Temperature}")
        myDevices.Set_Cooler_Off ()
        
    #------------------------------------------------------------------
    # Measure Water Level in Cooler and set RO
    #------------------------------------------------------------------
    Cooler_Water_Tank_Level = mySensors.get_cooler_tank_water_level ()
    print (f"Cooler Water Tank Level :{Cooler_Water_Tank_Level} Ltr")
    
    #Setting RO
    if Cooler_Water_Tank_Level < 40 :
        print (f"RO Turned ON at {Cooler_Water_Tank_Level} Ltr")
        myDevices.Set_RO_On ()
    elif Cooler_Water_Tank_Level >= 55 :
        print (f"RO Turned OFF at {Cooler_Water_Tank_Level} Ltr")
        myDevices.Set_RO_Off  ()

    Water_Consumed =  mySensors.get_water_flow ()
    print (f"Water Consumed :{Water_Consumed}")
    
    Water_TDS =  mySensors.get_water_tds ()
    print (f"RO Water TDS   :{Water_TDS}")

    #print ("Operation Completed. Restart Device to check Light again")
    print (f"Water Temp = {Water_Temperature} deg Cel, Level= {Cooler_Water_Tank_Level} lts, Water Consumed = {Water_Consumed} lts, RO Water TDS = {Water_TDS}")
    print (f"-------------Cycle No {running_Count} Completed-------------")
    
    # Send Data to NeerNetra-IoT-API-Server
    send_data_to_api()
    
    running_Count+=1
    time.sleep (Relay_Ops_Delay_Time)
#------------------------------------ End of Main program ----------------------------