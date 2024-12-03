from machine import Pin
import time
from now import Now

input_signal = Pin(1, Pin.IN)
on = Pin(2, Pin.OUT)
on.value(0)

n = Now()

try:
    n.connect()
    on.value(1)
except:
    on.value(0)

while True:
    if input_signal.value() == 1:
        n.publish(b'3complete')
        time.sleep(0.1)
        n.publish(b'wergdfjwejif')
    time.sleep(0.1)

    # Ensure interfaces are deactivated on exit
n.close()
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
