
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import numpy as np
import wave
import sys


spf = wave.open('/home/karolina/Pulpit/speech_recognition/266711_23_K_23_1.wav','r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')


#If Stereo
if spf.getnchannels() == 2:
    print ('Just mono files')
    sys.exit(0)

plt.figure(1)
plt.title('Signal Wave...')
plt.plot(signal)
plt.show()


# In[9]:


from pydub import AudioSegment
path='/home/karolina/Pulpit/speech_recognition/266711_23_K_23_1.txt'      
a = open(path,"r")
b = a.readlines()
a.close()
path_word=['otworz.wav', 'zamknij.wav', 'zrob.wav', 'nastroj.wav', 'wlacz.wav', 'wylacz.wav', 'muzyke.wav', 'swiatlo.wav', 'zapal.wav', 'podnies.wav', 'rolety.wav', 'telewizor.wav']

count = -1
for line in b:
    count += 1
    if count >= 0:      
        d = b[count].split()
        print (d)
        t1=d[0]
        t2=d[1]
        t1=float(t1)
        t2=float(t2)
        t1=t1*1000 # works in miliseconds
        t2=t2*1000
        print (t1)
        print (t2)
 
   
    newAudio = AudioSegment.from_wav("266711_23_K_23_1.wav")
    newAudio = newAudio[t1:t2]
    
    newAudio.export(d[2], format="wav")

