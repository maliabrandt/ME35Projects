#Malia Brandt and Alex Wardwel
#December 2024
#main.py for the ESP-32C mini 
#This code listens for a signal from the pico, then published a "complete" message
#for the interface box to receive. 
from machine import Pin
import time
from now import Now

#listening from the pico, the pin will turn high for one second when hopscotch is completed
input_signal = Pin(1, Pin.IN)

#led indicator
on = Pin(2, Pin.OUT)
on.value(0)

n = Now()

#turn led indicator on when connected, off when not
try:
    n.connect()
    on.value(1)
except:
    on.value(0)

#main loop 
while True:
    if input_signal.value() == 1:
        #send publish signal
        n.publish(b'3complete')
        time.sleep(0.1)
        #send random message afterwards (at the request of the interface team)
        n.publish(b'wergdfjwejif')
    time.sleep(0.1)

# Ensure interfaces are deactivated on exit
n.close()
#turn led off 
on.value(0)








# output_signal = Pin(16, Pin.OUT)
# output_signal.value(0)

#if receive start command from NOW, output 1
#if receive 1from input_signal, send completed NOW message

# output_signal.value(1)
# print(output_signal.value())
# print("sending go message")
# time.sleep(1)
# output_signal.value(0)
# print(output_signal.value())

# while True:
#     print(input_signal.value())
#     time.sleep(0.5)
