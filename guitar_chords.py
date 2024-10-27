#guitar_chords.py
#Malia Brandt
#This class plays chords A, D, G, C, E, Em. It can do upstrokes and downstrokes.
#0.04 is recommended as upstroke and downstroke parameters
#It is not an asyncio class.
#capo can be put on the third fret to play A, D, G, Em chords

import time
from BLE_CEEO import Yell

class Guitar:
    def __init__(self):
        self.NoteOn = 0x90
        self.NoteOff = 0x80
        self.StopNotes = 123
        self.SetInstroment = 0xC0
        self.Reset = 0xFF

        self.velocity = {'off':0, 'pppp':8,'ppp':20,'pp':31,'p':42,'mp':53,
            'mf':64,'f':80,'ff':96,'fff':112,'ffff':127}
            
        self.p = Yell('Malia', verbose = True, type = 'midi')
        self.p.connect_up()

        self.channel = 0
        
        self.cmd = self.NoteOn
        self.channel = 0x0F & self.channel
        self.timestamp_ms = time.ticks_ms()
        self.tsM = (self.timestamp_ms >> 7 & 0b111111) | 0x80
        self.tsL =  0x80 | (self.timestamp_ms & 0b1111111)

        self.c =  self.cmd | self.channel
        
        #chords in array form -- MIDI nums (in order)
        self.A_major = [45, 52, 57, 61, 64]
        self.D_major = [50,57,62,66]
        self.C_major = [48,52,55,60,64]
        self.G_major = [43,47,50,55,59,67]
        self.E_major = [40,47,52,56,59,64]
        self.E_minor = [40,47,52,56,59, 64]
        
        #capo on third?
        self.capo_on = False
        
        #chords w capo on third fret
        self.A_maj3 = [48,55,60,64,67]
        self.D_maj3 = [53,60,65,69]
        self.G_maj3 = [46,48,53,58,65,70]
        self.E_min3 = [43,50,55,5,62,67]
        self.C_maj3 = [51, 55, 58, 63, 67]
        self.E_maj3 = [43, 50, 55, 59, 62, 67]
        
        
    #disconnect from garage band
    def disconnect(self):
        self.p.disconnect()
    
    #put capo on third fret
    def turn_capo_on(self):
        self.capo_on = True
    
    #take capo off third fret 
    def turn_capo_off(self):
        self.capo_on = False
        
    #get the chords
    def get_chord(self, chord):
        if not self.capo_on:
            if chord == 'A':
                return self.A_major
            elif chord == 'D':
                return self.D_major
            elif chord == 'G':
                return self.G_major
            elif chord == 'C':
                return self.C_major
            elif chord == 'E':
                return self.E_major
            elif chord == 'Em':
                return self.E_minor
        elif self.capo_on:
            if chord == 'A':
                return self.A_maj3
            elif chord == 'D':
                return self.D_maj3
            elif chord == 'G':
                return self.G_maj3
            elif chord == 'Em':
                return self.E_min3
            elif chord == 'E':
                return self.E_maj3
            elif chord == 'C':
                return self.C_maj3
    
    #downstroke, time in between each string, 0.04 is recommended
    def strum_down(self, chord, s_time):
        for i in chord:
            note = bytes([self.tsM,self.tsL,self.c,i,self.velocity['f']])
            self.p.send(note)
            time.sleep(s_time)
    
    #downstroke, time in between each string, 0.04 is recommended
    def strum_up(self, chord, s_time):
        for i in range(len(chord) - 1,-1, -1):
            note = bytes([self.tsM,self.tsL,self.c,chord[i],self.velocity['f']])
            self.p.send(note)
            time.sleep(s_time)   
    
    #end the notes
    #NOTE: MUST END THE NOTES BEFORE PLAYING ANOTHER ONE 
    def end_chord(self, chord):
        for i in chord:
            note = bytes([self.tsM,self.tsL,self.c,i,self.velocity['off']])
            self.p.send(note)

    #play the chords, no time between each string - 0 time between strings
    def play(self, chord):
        self.strum(chord, 0)

# g = Guitar()
# 
# for i in range(2):
#     for chord in ["A", "C", "E", "D", "G", "Em"]:
#         print("chord:" + chord)
#         g.strum_down(g.get_chord(chord), 0.06)
#         time.sleep(1.5)
#         g.end_chord(g.get_chord(chord))
# #         g.strum_up(g.get_chord(chord), 0.06)
# #         time.sleep(1.5)
# #         g.end_chord(g.get_chord(chord))
#     print("turn capo on")
#     g.turn_capo_on()    
# 
# 
# 
# g.disconnect()
        

