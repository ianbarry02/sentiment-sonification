# Code modified from Matt Russo: https://youtu.be/DUdLRy8i9qI?si=eXDV4-gPaEE7uYKp

import pandas as pd
filename = 'S02E08_sentiment'  #name of csv data file
df = pd.read_csv('[sentiment score file pathname]')
df = df.dropna(subset=['sentiment_score', 'sentiment_change']) #get rid of all rows with sentiment score or change missing

import matplotlib.pylab as plt
score = df['sentiment_score'].values   #get sentiment score values in an array
change = df['sentiment_change'].values  #get sentiment change values in an array
plt.scatter(score, change, s=change)
plt.xlabel('Sentiment Score')
plt.ylabel('Sentiment Evolution')
#plt.show()

# Mapping function
def map_value(value, min_value, max_value, min_result, max_result):
 '''maps value (or array of values) from one range to another'''
 
 result = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
 return result

# Set duration and tempo
duration_beats = 52.8 #desired duration in beats (actually, onset of last note)
t_data = map_value(score, 0, max(score), 0,duration_beats)

bpm = 60  #beats per minute, if bpm = 60, 1 beat = 1 sec 
duration_sec = duration_beats*60/bpm #duration in seconds 
print('Duration:', duration_sec, 'seconds')

# Normalize and scale the data
y_data = map_value(change, min(change), max(change), 0, 1) 
plt.scatter(score, y_data, s=50*y_data)
plt.xlabel('Sentiment Score')
plt.ylabel('Sentiment Evolution')
#plt.show()

y_scale = 0.5  #lower than 1 to spread out more evenly
y_data = y_data**y_scale
plt.scatter(score, y_data, s=50*y_data)
plt.xlabel('Sentiment Score')
plt.ylabel('Sentiment Evolution')
#plt.show()

# Map data to notes
from audiolazy import str2midi, midi2str

# Test audiolazy library has loaded
print(str2midi('C3'))

# Pick some octaves to map data onto
note_names = ['C1','C2','G2',
             'C3','E3','G3','A3','B3',
             'D4','E4','G4','A4','B4',
             'D5','E5','G5','A5','B5',
             'D6','E6','F#6','G6','A6']

note_midis = [str2midi(n) for n in note_names] 
n_notes = len(note_midis)

# Map data
midi_data = []
for i in range(len(y_data)):
    note_index = round(map_value(y_data[i], 0, 1, n_notes-1, 0)) 
    midi_data.append(note_midis[note_index])
plt.scatter(t_data, midi_data, s=50*y_data)
plt.xlabel('time [beats]')
plt.ylabel('midi note numbers')
#plt.show()

# Specify velocity of notes to map data onto
vel_min,vel_max = 35,127   #minimum and maximum note velocity
vel_data = []
for i in range(len(y_data)):
    note_velocity = round(map_value(y_data[i],0,1,vel_min, vel_max)) 
    vel_data.append(note_velocity)
    
plt.scatter(t_data, midi_data, s=vel_data)
plt.xlabel('time [beats]')
plt.ylabel('midi note numbers')
#plt.show()

# Write midi file
from midiutil import MIDIFile 
    
#create midi file object, add tempo
my_midi_file = MIDIFile(1) #one track 
my_midi_file.addTempo(track=0, time=0, tempo=bpm) 
#add midi notes
for i in range(len(t_data)):
    my_midi_file.addNote(track=0, channel=0, time=t_data[i], pitch=midi_data[i], volume=vel_data[i], duration=2)
#create and save the midi file itself
with open(filename + '.mid', "wb") as f:
    my_midi_file.writeFile(f)

# Make music
import pygame 
pygame.init()
pygame.mixer.music.load(filename + '.mid')
pygame.mixer.music.play()
#pygame.mixer.music.stop() #run this to stop, it's the only way!