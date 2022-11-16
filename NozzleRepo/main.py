import _thread
from machine import ADC, Pin
import utime
import math
from PiicoDev_SSD1306 import *
from PiicoDev_Unified import sleep_ms

pins = [
    Pin(15,Pin.OUT),
    Pin(14,Pin.OUT),
    Pin(16,Pin.OUT),
    Pin(17,Pin.OUT),
    ]

full_step_sequence = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
    ]
full_step_sequence2 = [
    [0,0,0,1],
    [0,0,1,0],
    [0,1,0,0],
    [1,0,0,0]
    ]

spLock = _thread.allocate_lock()
display = create_PiicoDev_SSD1306()

# Text and numbers
thick = 15
for counter in range(0,101):
    display.fill(0)
    display.text("Loading",30,20, 1)
    display.text(str(counter),50,35, 1)
    display.fill_rect(10, HEIGHT-thick, counter, thick, 1)
    display.show()
   
sleep_ms(500)

display.fill(0)


# use variables instead of numbers:
soil = ADC(Pin(26)) # Soil moisture PIN reference

#Calibraton values
min_moisture=0
max_moisture=65535

readDelay = 00.1 # delay between readings

def spinStepper():
    for j in range(1, 100):
        for step in full_step_sequence2:
            for i in range(len(pins)):
                pins[i].value(step[i])
                utime.sleep(0.001)
            
def updateLcd():
    display.fill(0)
    # read moisture value and convert to percentage into the calibration range
    moisture = (max_moisture-soil.read_u16())*100/(max_moisture-min_moisture) 
    # print values
    print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
    display.text("moisture:" + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")", 0, 10, 1)
    display.show()
    utime.sleep(readDelay) # set a delay between readings
   
    
while True:
   updateLcd()
   spinStepper()
