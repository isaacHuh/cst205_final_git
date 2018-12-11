import wave
import numpy
import random


all_files = ["G_chord.wav", "C_chord.wav", "Am_chord.wav" , "E_chord.wav" , "Dm_chord.wav" , "Em_chord.wav" , "F_chord.wav" , "G7_chord.wav" , "B7_chord.wav" , "Bm_chord.wav" , "idk_chord.wav" , "A_chord.wav" , "D_chord.wav"]
infiles = []
for i in range(len(all_files)):
	rand_num = random.randint(0,(len(all_files)-1))
	infiles.append(all_files[rand_num]) 

outfile = "beat_new.wav"
#this makes the file where it will play the sound
data = []
for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()

output = wave.open(outfile, 'wb')
output.setparams(data[0][0])

add_num = random.randint(3,(len(data)-1))
for i in range(add_num):
	output.writeframes(data[i][1])

output.close()

class Beats:
    sounds = [] 
    @staticmethod
    def playRandom():
        random.choice(SoundManager.sounds).play()
#This is the code that makes the sounds go at random