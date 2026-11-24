# -------------------------------------------------------------
# --  SensorHandler.py
# --  Reads data from the Sensors & updates the API of the NeerNetra App
# --      Water Temp
# --      Water Level
# --      Water TDS
# --      Water Consumed
# -------------------------------------------------------------  
# --  Updated on : 08 Dec 2025
# --  Updated by : Yashvardhan Yadav
# --  Code tested, Proved and Freezed.
# --------------------------------------------------------------

""" Class   : SensorHandler
    Purpose : Handle all the Sensors of the NeerNetra App
        Water Temp
        Water Level
        Water TDS
        Water Consumed
"""
__author__  = 'Yashvardhan Yadav'
__Version__ = "relay.2025.12.01"

from machine import Pin, ADC
import time

Cooler_Tank_Capacity_Ltr = 60
Relay_Ops_Delay_Time     = 2

# Analog Inputs (Sensors)
Pin_Water_Temp  = 34   # GPIO34 - Water Temp
Pin_Water_Level = 35   # GPIO35 - Water Level
Pin_Water_TDS   = 36   # GPIO36 - Water TDS
Pin_Water_Flow  = 39   # GPIO39 - Water Consumed

class SensorHandler ():
    ''' Class for Getting Data from Sensors
        Pin_Water_Temp  = 34   # GPIO34 - Water Temp
        Pin_Water_Level = 35   # GPIO35 - Water Level
        Pin_Water_TDS   = 36   # GPIO36 - Water TDS
        Pin_Water_Flow  = 39   # GPIO39 - Water Consumed
    '''       
    
    
    def __init__(self ):
        print('Senor Controller Initialisation Commenced')
        # Setting Pins
        self.Pin_water_temperature       = Pin(34, Pin.IN)
        self.Pin_cooler_tank_water_level = Pin(35, Pin.IN)
        self.Pin_water_tds               = Pin(36, Pin.IN)
        self.Pin_water_flow              = Pin(39, Pin.IN)
        
        # initialising ADCs : Create ADC object on GPIO34 (ADC1_CH6)
        self.adc_water_temperature       = ADC(Pin(self.Pin_water_temperature))
        self.adc_cooler_tank_water_level = ADC(Pin(self.Pin_cooler_tank_water_level))
        self.adc_water_tds               = ADC(Pin(self.Pin_water_tds))
        self.adc_water_flow              = ADC(Pin(self.Pin_water_flow))
        
        
        print('Senor Controller Initialisation Completed and set to off condition')
    
    def get_water_temperature (self):
        print ("Reading Water Temp :")
        raw_value  = self.adc_water_temperature.read()  # Read 0-4095
        Water_Temp = int ((raw_value / 4095) * 40 ) # Convert to volts
        # print (f"Raw: {raw_value}, Water Temperature = {Water_Temp}")
        print (f'Water Temperature = {Water_Temp}. Method get_water_temperature Completed')
        return Water_Temp
    
    
    def get_cooler_tank_water_level (self):
        print ("Reading Cooler Tank Water Level :")
        raw_value  = self.adc_cooler_tank_water_level.read()  # Read 0-4095
        Cooler_Tank_Water_Level = int ((raw_value / 4095) * Cooler_Tank_Capacity_Ltr ) # Convert to volts
        # print (f"Raw: {raw_value}, Water Temperature = {Water_Temp}")
        print (f'Cooler Tank Water = {Cooler_Tank_Water_Level} Ltr. Method get_cooler_tank_water_level Completed')
        return Cooler_Tank_Water_Level
    
    def get_water_tds (self):
        print ("Reading RO Water TDS :")
        raw_value  = self.adc_water_tds.read()  # Read 0-4095
        RO_Water_TDS = int ((raw_value / 4095) * 1000 ) # Convert to volts
        # print (f"Raw: {raw_value}, Water Temperature = {Water_Temp}")
        print (f'RO Water TDS = {RO_Water_TDS} Ltr. Method get_water_tds Completed')
        return RO_Water_TDS
    
    def get_water_flow (self):
        print ("Reading Cooler Tank Water Level :")
        raw_value  = self.adc_water_flow.read()  # Read 0-4095
        Water_Flow = int ((raw_value / 4095) * 200 ) # Convert to volts
        # print (f"Raw: {raw_value}, Water Temperature = {Water_Temp}")
        print (f'Water Consumed = {Water_Flow} Ltr. Method get_water_flow Completed')
        return Water_Flow
    
    def Test_Com (self):
        """ Test Communication between ESP Device and CBM App
            --  No Sensors are activated or de-activated, enabled/disabled
            --  Only messages are exchanged and Results are printed on screen
        """
        myResponse =  {"Communication Test":{
                                                "Class"  : self.__class__.__name__, 
                                                "Status" : "OK"
                                            } 
                      }
        print  (myResponse)
        return myResponse

        
# --Class Definition Ends---------------------------

#------- Main Program Ends---------------------------
if __name__ == "__main__" :
    objMyRelayControl = SensorHandler ()
    
    print ('Repeating Operation 4 Times in sequence for both relays.')
    # Repeat Operation 10 Times
    for i in range(15):
        print ("Cycle From Class Local : ", i+1, "Commence")
        print ( "Water Temp :", objMyRelayControl.get_water_temperature()," Water Level: ",objMyRelayControl.get_cooler_tank_water_level())
        time.sleep (Relay_Ops_Delay_Time)

        print ("Cycle : ", i+1, "Completed")
        print ("------------------------------------")
#--------- Main Program Ends-------------------------