#Malia Brandt and Alex Wardwell 
#December 2024
#main.py , to be run on the raspberry pi pico
#This is the main code for the hopscotch game. 

from hopscotch import Hopscotch
from machine import Pin
import time, asyncio

#create hopscotch instance 
h = Hopscotch()

#pin to communicate with the ESP-32C, when the game is finished, 
#turn the pin high for one second. The ESP is listening for this signal.
respond = Pin(21, Pin.OUT)


#when button is pressed, start the game
def callback(p):
    h.game_start_true()
    #print("starting")
#button instance 

p = Pin(20, Pin.IN, Pin.PULL_UP)  
p.irq(trigger=Pin.IRQ_RISING, handler=callback)

#main run function for the program
async def main():
    while True:
        #play game when button is pressed
        while h.return_game_start():
            h.make_pattern()
            h.display_pattern()
            await h.detect_jumps()
            
        #send message to ESP when done
        if h.return_finished()==True:
            respond.on()
            time.sleep(1)
            respond.off()

#run the main function to play the game
asyncio.run(main())
        
        
        
    


