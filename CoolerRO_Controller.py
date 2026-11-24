# -------------------------------------------------------------
# --  CoolerRO_Controller.py
# --  This is Relay Control file of the CBM App
# --  Relay 1 = Water cooler Charge
# --  Realy 2 = RO
# -------------------------------------------------------------  
# --  Updated on : 07 Dec 2025
# --  Updated by : Yahsvardhan Yadav
# --  Code tested, Proved and Freezed.
# --------------------------------------------------------------

""" Class   : Relay_Control
    Purpose : This is Relay Control file of the CBM App
                Relay 1 = Water Cooler 
                Realy 2 = RO
"""
__author__  = 'Yahsvardhan Yadav'
__Version__ = "relay.2025.12.1"

from machine import Pin, I2C
from time import sleep
       
Relay_Ops_Delay_Time  = 1
    
class RelayControl ():
    ''' Class for Controlling Relays for Mobile Charging and Printer
        Pin_No_Relay_1 = 5 
        Pin_No_Relay_2 = 18
    '''       

    def __init__(self ):
        print('Relay Control Initialisation Commenced')
        self.Pin_Cooler = Pin(5 ,Pin.OUT)
        self.Pin_RO     = Pin(18 ,Pin.OUT)
        
        # setting Default value to Off
        self.Pin_RO.value(0)
        self.Pin_Cooler.value(0)
        print('Relay Control Initialisation Completed and set to off condition')
    
    def Set_Cooler_On (self):
        self.Pin_Cooler.value(1)
        print ('Cooler On')
    
    def Set_Cooler_Off (self):
        self.Pin_Cooler.value(0)
        print ('Cooler Off')
    
    def Set_RO_On (self):
        self.Pin_RO.value(1)
        print ('RO On')
    
    def Set_RO_Off (self):
        self.Pin_RO.value(0)
        print ('RO Off')

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
    objMyRelayControl = RelayControl ()
    
    print ('Repeating Operation 4 Times in sequence for both relays.')
    # Repeat Operation 10 Times
    for i in range(4):        
        objMyRelayControl.Set_Cooler_On()
        sleep (Relay_Ops_Delay_Time)

        objMyRelayControl.Set_Cooler_Off()
        sleep (Relay_Ops_Delay_Time)

        objMyRelayControl.Set_RO_On()
        sleep (Relay_Ops_Delay_Time)

        objMyRelayControl.Set_RO_Off()
        sleep (Relay_Ops_Delay_Time)
    
#--------- Main Program Ends-------------------------