from guitar_chords import Guitar
import asyncio, time, neopixel
from machine import Pin, ADC
from secrets import WiFi
from mqtt import MQTTClient, MQTTException
from accelerometer import Acceleration


class GuitarHero:
    #initialzing all variables
    def __init__(self):
        
        self.guitar = Guitar()
        #start with standard tuning 
        self.capo = False
        #time until end notes
        self.note_time = 0.3
        #time between string strums
        self.strum_speed = 0.01
        #accelerometer distance to strum
        self.threshold = 50000
        #light threshold to pause
        self.light_threshold = 250
        
        #button 1, 2, 3
        self.b1 = Pin('GPIO16', Pin.IN)
        self.b2 = Pin('GPIO17', Pin.IN)
        self.b3 = Pin('GPIO18', Pin.IN)
        
        #testing LEDS
        self.led1 = Pin('GPIO5', Pin.OUT)
        self.led2 = Pin('GPIO4', Pin.OUT)
        self.led3 = Pin('GPIO3', Pin.OUT)
        self.led5 = Pin('GPIO1', Pin.OUT)
        self.led1.off()
        self.led2.off()
        self.led3.off()
        self.led5.off()
        
        
        #accelerometer setup 
        self.scl = Pin('GPIO27', Pin.OUT)
        self.sda = Pin('GPIO26', Pin.OUT)
        self.t = Acceleration(self.scl, self.sda)
        
        #photoresistor setup
        self.play = True
        self.adc = ADC(28)

        
        #setup neopixel -- is on when ready to play, start off
        self.on = (0,40,0) # Green color
        self.off = (0,0,0) # off
        self.pixel = neopixel.NeoPixel(Pin(28),1)
        self.pixel[0]=self.off
        self.pixel.write()
        
        #connect to tufts wifi
        self.wf = WiFi()
        self.wf.connect_tufts()
        
        
        #initialize mqtt stuff
        self.mqtt_broker = 'test.mosquitto.org'
        #self.mqtt_broker = 'broker.hivemq.com' 
        self.port = 1883
        self.topic_sub = 'ME35-24/#'       # this reads anything sent to ME35
        self.topic_pub = 'ME35-24/tell'
        self.client = MQTTClient('ME35MaliaBrandt', self.mqtt_broker , self.port, keepalive=60)
        self.setup()
        
        
#     #more setup for mqtt stuff 
#     def setup(self):
#         self.client.connect()
#         print('Connected to %s MQTT broker' % (self.mqtt_broker))
#         self.led5.on() #turn led on when connected
#         self.client.set_callback(self.callback)          # set the callback if anything is read
#         self.client.subscribe(self.topic_sub.encode())   # subscribe to a bunch of topics
    def setup(self):
        try:
            self.client.connect()
            print('Connected to %s MQTT broker' % (self.mqtt_broker))
            self.led5.on()  # Turn LED on when connected
            self.client.set_callback(self.callback)  # Set the callback if anything is read
            self.client.subscribe(self.topic_sub.encode())  # Subscribe to topics
        except MQTTException as e:
            print(f"Failed to connect to MQTT broker: {e}")
       
    #if a MQTT message is received, set the tuning 
    def callback(self, topic, msg):
        if topic.decode() == 'ME35-24/Malia':
            print('received')
            print(msg.decode())
            if msg.decode() == "Standard":
                self.guitar.turn_capo_off()
            elif msg.decode() == "Capo":
                self.guitar.turn_capo_on()
    
    #strums the guitar, ends the note 
    async def strum_play(self, chord):
        self.guitar.strum_down(self.guitar.get_chord(chord), self.strum_speed)
        await asyncio.sleep(self.note_time)
        self.guitar.end_chord(self.guitar.get_chord(chord))
        

    #plays the chords based on what button is pressed    
    def play_chords(self):
        print(self.capo)
        print(self.b1.value())
        print(self.b2.value())
        print(self.b3.value())
        
        #check button values and play chords
        if self.b1.value() == 1:
            self.led1.on()
            if self.b2.value() == 0:
                self.led2.off()
                if self.b3.value() == 0: #only b1 plays A
                    self.led3.off()
                    asyncio.run(self.strum_play("A"))
                elif self.b3.value() == 1: #b1 and b3 plays Em
                    self.led3.on()
                    asyncio.run(self.strum_play("Em"))
            elif self.b2.value() == 1: 
                self.led2.on()
                if self.b3.value() == 0: #b1 and b2 plays E
                    self.led3.off()
                    asyncio.run(self.strum_play("E"))
                elif self.b3.value() == 1: #all doesn't play anything
                    self.led3.on()
        elif self.b1.value() == 0:
            self.led1.off()
            if self.b2.value() == 1:
                self.led2.on()
                if self.b3.value() == 0: #only b2 plays C
                    self.led3.off()
                    asyncio.run(self.strum_play("C"))
                elif self.b3.value() == 1: #b2 and b3 plays G
                    self.led3.on()
                    asyncio.run(self.strum_play("G"))
            elif self.b2.value() == 0:
                self.led2.off()
                if self.b3.value() == 0: #no buttons pressed
                    self.led3.off()
                elif self.b3.value() == 1: #only b3 plays D
                    self.led3.on()
                    asyncio.run(self.strum_play("D"))
        
    #read the light sensor, pause all functions if no light is seen
    def read_light_sensor(self):
        light_level = self.adc.read_u16()
        #print(self.play)
        #print(light_level)
        if light_level > self.light_threshold:
            self.play = True
        if light_level <= self.light_threshold:
            self.play = False
    
    #checks accelerometer, calls play_chords if displaced
    async def strum_accel(self):
        #check tuning
        self.client.check_msg()
    
        prev = self.t.read_accel()[2]
        await asyncio.sleep(0.1)
        curr = self.t.read_accel()[2]
        if abs(curr-prev) > self.threshold:
            #print("play note")
            self.play_chords()
            #print(abs(curr-prev))
        #print(prev)
        #print(curr)
    
    #main function to run the whole system
    def main(self):
        self.pixel[0]=self.on
        self.pixel.write()
        while True: #infinite loop
            #see if there is light
            self.read_light_sensor()
            #check for tuning message
            self.client.check_msg()
            #if there is light
            if self.play:
                #check for strum and button presses
                asyncio.run(self.strum_accel())
        

# g = GuitarHero()
# 
# #g.main()
# 
# while True:
#     g.client.check_msg()
#     time.sleep(0.5)

        
        
        
        
        
        
        
        



