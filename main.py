from hopscotch import Hopscotch
from machine import Pin
import time, asyncio

h = Hopscotch()
respond = Pin(21, Pin.OUT)



def callback(p):
    h.game_start_true()
    #print("starting")

p = Pin(20, Pin.IN, Pin.PULL_UP)  # guess with PULL_UP does...
p.irq(trigger=Pin.IRQ_RISING, handler=callback)


async def main():
    while True:
        #play game
        while h.return_game_start():
            h.make_pattern()
            h.display_pattern()
            await h.detect_jumps()
            
        #send message to ESP when done
        if h.return_finished()==True:
            respond.on()
            time.sleep(1)
            respond.off()
            
asyncio.run(main())
        
        
        
    


