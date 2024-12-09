#Malia Brandt and Julian Moody
#December 2024
#mario_theme.py
#This code defines frequency notes on the raspberry pi pico buzzer, then plays the 
#mario victory theme song. This will be played when the hopscotch game is finished correctly. 
#Code outline created by ChatGPT, code edited by Malia, melody transcribed by Malia, Julian, and Alex

from machine import Pin, PWM
import time, asyncio


#plays the mario theme song
async def play_mario_theme():

    # Buzzer instance 
    buzzer = Pin('GPIO18', Pin.OUT) 
    pwm = PWM(buzzer)
    
    # Define the notes and their corresponding frequencies in Hz (approx.)
    notes = {
        'C': 261,
        'D': 294,
        'Ef': 311,
        'E': 330,
        'F': 349,
        'G': 392,
        'Af': 415,
        'A': 440,
        'Bf': 466,
        'B': 494,
        'C5': 523,
        'D5': 587,
        'Ef5': 622,
        'E5': 659,
        'F5': 698,
        'G5': 784,
        'Af5': 831,
        'Bf5': 932,
        'C6': 1047,
        'REST': 8
    }

    # Define the melody of the Super Mario Level Victory theme song (in terms of notes and duration)
    melody = [
            ('C', 0.1), ('E', 0.1), ('G', 0.1), ('C5', 0.1), ('E5', 0.1), ('G5', 0.2),
            ('E5', 0.1), ('REST', 0.2), ('C', 0.1), ('Ef', 0.1), ('Af', 0.1), ('C5', 0.1),
            ('Ef5', 0.1), ('Af5', 0.2), ('Ef5', 0.1), ('REST', 0.2), ('D', 0.1), ('F', 0.1), ('Bf', 0.1),
            ('D5', 0.1), ('F5', 0.1), ('Bf5', 0.2), ('Bf5', 0.1), ('Bf5', 0.1), ('Bf5', 0.1), ('C6', 0.8),
        ]

    # Play the melody
    for note, duration in melody:
        try: 
            if note == 'REST':
                pwm.duty_u16(0)  # Turn off the buzzer
                await asyncio.sleep(duration)
            elif note in notes:
                pwm.freq(notes[note])
                pwm.duty_u16(32768)  # Play sound at half power
                await asyncio.sleep(duration)
                pwm.duty_u16(0)  # Turn off the buzzer after note
                await asyncio.sleep(0.05)  # Short pause between notes
        except:
            await asyncio.sleep(0.05)

#Testing code
#asyncio.run(play_mario_theme())






