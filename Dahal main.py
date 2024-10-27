#Malia Brandt 
#For Musical Instrument Midterm October 2024
#This code is meant to run on the Dahal board. It connects the Dahal board to the servo,
#which can be controlled by the potentiometer position. It displays the potentiometer
#value on the lcd on the dahal board. 

from machine import Pin, SoftI2C, PWM, ADC
import servo
import ssd1306
import adxl345
import time


i2c = SoftI2C(scl = Pin(7), sda = Pin(6))

pot = ADC(Pin(3))
pot.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V

motor = servo.Servo(Pin(2))

#change the servo position based on the potentiometer input 
def servo_move(pot_num):
    max_pot = 4095
    conversion = 66/4095
    motor.write_angle(66-int(conversion*pot_num))

screen = ssd1306.SSD1306_I2C(128,64,i2c)
while True:
    pot_num = pot.read()
    screen.fill(0)
    screen.text(f'potentiometer', 0, 0, 1) # to display text
    screen.text('val:' + str(pot_num), 0, 10, 1)
    #text here to receive MQTT commands, saying the tuning
    screen.show()
    servo_move(pot_num)
    
    

