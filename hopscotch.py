#Malia Brandt and Alex Wardwell
#hopscotch.py
#This file contains the Hopscotch class. This class is able to create a randomized pattern for the 
#user to follow. It then stores and displays the pattern on the neopixels. It can detect the pattern of buttons 
#pressed by the user, comparing themt to the correct pattern generated. If a wrong step is detected, the
#process repeats, generating and displaying a new pattern. If the user gets to the last row without messing up, 
#there is a light show and the mario theme plays on the buzzer

#randomize pattern (which square per row)
#remember that pattern
#display
#detect kid's jumping pattern
    #put data into an array, compare to pattern array
#give reward (if right) OR show when wrong (then try again)

import time, asyncio
from machine import Pin
import random
import neopixel
import mario_theme 

class Hopscotch():
    def __init__(self):
        #current pattern 
        self.pattern = [0]*5
        
        #create array of neopixels
        self.leds = []

        #fill the array with initialized pins 0-9
        for i in range(10,20):
            led = neopixel.NeoPixel(Pin(i),10)
            self.leds.append(led)
        self.neopixels_off()
        
        #setup array of buttons
        self.buttons = []
        
        #initialize button pins
        for i in range(0,10):
            button = Pin(i, Pin.IN)
            self.buttons.append(button)
        
        #commands for neopixels
        self.on = (55,0,200)
        self.purple = (55, 0, 200)
        self.off = (0,0,0)
        
        #array with the player's pattern
        self.player = [0]*5
        
        #tells if the game is started
        self.game_start = False
        
        #tells if game has finished
        self.finished = False
        
    def game_start_true(self):
        self.game_start=True
    
    def game_start_false(self):
        self.game_start=False
        
    def return_game_start(self):
        return self.game_start
    
    def return_finished(self):
        return self.finished

    #turn all neopixels off
    def neopixels_off(self):
        for i in range(10):
            neopixel = self.leds[i]
            for i in range(10):
                neopixel[i] = (0,0,0)
                neopixel.write()
            
    #all neopixels on
    def neopixels_on(self, color):
        for i in range(10):
            neopixel = self.leds[i]
            for i in range(10):
                neopixel[i] = color
                neopixel.write()
        
    #turn a single strip of neopixels on    
    def neo_on(self, pixel):
        neopixel = pixel
        for i in range(10):
            pixel[i] = (0,255,0)
            pixel.write()
    
    #turns a neopixel strip of 10 off
    def neo_off(self, pixel):
        neopixel = pixel
        for i in range(10):
            pixel[i] = (0,0,0)
            pixel.write()
            
    #turns leds off by row -- used for incorrect pattern detection
    def leds_off_by_row(self):
        for i in range(5):
            self.neo_off(self.leds[2*i])
            self.neo_off(self.leds[2*i+1])
            time.sleep(0.5)

    #display winning pattern, long version
    async def winning_pattern(self):
        self.neopixels_off()
        for m in range(1):
            for i in range(5):
                self.neo_on(self.leds[2*i+1])
                await asyncio.sleep(0.25)
            await asyncio.sleep(0.01)
            for j in range(5):
                self.neo_on(self.leds[8-(2*j)])
                await asyncio.sleep(0.25)
            await asyncio.sleep(0.01)
            for k in range(5):
                self.neo_off(self.leds[2*k+1])
                await asyncio.sleep(0.25)
            await asyncio.sleep(0.01)
            for l in range(5):
                self.neo_off(self.leds[8-(2*l)])
                await asyncio.sleep(0.25)
            await asyncio.sleep(0.01)
        
        colors = [(255,0,0),(125,125,0),(0,255,0)]
        for x in range(3):
            self.neopixels_on(colors[x])
            await asyncio.sleep(0.35)
            self.neopixels_off()
            await asyncio.sleep(0.35)

    #winning pattern alternate version, shorter
    def alt_winning_pattern(self):
        colors = [(255,0,0),(125,125,0),(0,255,0)]
        for x in range(2):
            self.neopixels_on(colors[x])
            time.sleep(0.35)
            self.neopixels_off()
            time.sleep(0.35)
        self.neopixels_on(colors[2])
        

    #random number generator for pattern 
    #1 = Right, 2 = Left, 3 = Both
    def make_pattern(self):
        for i in range(0,5):
            self.pattern[i] = random.randint(1,3)
        print(self.pattern)
        
    #display the pattern on the LEDs
    def display_pattern(self):
        self.finished = False
        for i in range(0,5):
            row = i+1
            print("row: ", row)
            if self.pattern[i] == 1:
                print("1")
                #make led[2i] light up
                self.neo_on(self.leds[2*i])
            elif self.pattern[i] == 2:
                print("2")
                #make led[2i+1] light up
                self.neo_on(self.leds[2*i+1])
            else:
                print("3")
                #make both light up
                self.neo_on(self.leds[2*i])
                self.neo_on(self.leds[2*i+1])
                
            time.sleep(1)
            #all leds off
            self.neopixels_off()
            time.sleep(0.25)
     
    async def compare(self, index):
        print("comparing")
        #if the arrays don't match, reset 
        if self.pattern[index] != self.player[index]:
            print(self.pattern[index], ", ", self.player[index])
            #flash leds
            self.neopixels_on((0,255,0))
            await asyncio.sleep(1)
            self.neopixels_off()
            #set array to 0s
            self.player = [0]*5
            #make new pattern
            self.make_pattern()
            
            for i in range(4):
                self.neopixels_on((0,255,0))
                await asyncio.sleep(0.5)
                self.neopixels_off()
                await asyncio.sleep(0.5)
            
            #display new pattern
            self.display_pattern()
        elif index == 4:
            #end the game if correct and at the final index
            self.finished = True
            self.game_start=False
            await asyncio.sleep(0.5)
            #lightshow yay
#             task1 = asyncio.create_task(self.winning_pattern())
#             task2 = asyncio.create_task(mario_theme.play_mario_theme())
#             await asyncio.gather(task2, task1)
            self.alt_winning_pattern()
            await mario_theme.play_mario_theme()
            self.neopixels_off()
            
                
            
    #check if the buttons are stepped on in the right order
    async def detect_jumps(self):
        #loop through checking pin status for each row
        #if pin is high, append to the array
        while not self.finished:
            for i in range(5):
                row = i+1
                #print(i, ": ", self.buttons[i].value())
                #if only left button pressed, set value to 1
                if self.buttons[2*i].value() == 0 and self.buttons[2*i+1].value() == 1:
                    print("row:", row)
                    print("1")
                    self.player[i] = 1
                    self.neo_on(self.leds[2*i])
                    await self.compare(i)
                #if only right button pressed, set value to 2
                elif self.buttons[2*i].value()==1 and self.buttons[2*i+1].value() == 0:
                    print("row:", row)
                    self.player[i] = 2
                    print("2")
                    self.neo_on(self.leds[2*i +1])
                    await self.compare(i)
                #if both buttons pressed, set value to 3
                elif self.buttons[2*i].value()==0 and self.buttons[2*i+1].value()==0:
                    print("row:", row)
                    self.player[i] = 3
                    print("3")
                    self.neo_on(self.leds[2*i])
                    self.neo_on(self.leds[2*i+1])
                    await self.compare(i)
                await asyncio.sleep(0.075)
    





