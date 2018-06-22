import soundfile
import sounddevice
import noiseProfiler
import argparse
import time
import os
import pywt
from waveletMorpher import WaveletMorpher
import waveletHelper

dataOriginal, sampleRate = soundfile.read('../samples/tone_start.wav')
dataTarget, sampleRate = soundfile.read('../samples/tone_end.wav')

print("Number of samples dataOriginal read: " + str(len(dataOriginal)))
print("Number of samples dataTarget read: " + str(len(dataTarget)))

wlevels = 6
dbName = 'db8'

wtOriginal = pywt.WaveletPacket(dataOriginal, dbName, 'symmetric', wlevels)
wtTarget = pywt.WaveletPacket(dataTarget, dbName, 'symmetric', wlevels)

morpher = WaveletMorpher(wtOriginal, wtTarget)

morphedWavelets = morpher.morph(1)

finalWavelets = list()
finalWavelets.append(wtOriginal)
for morphed in morphedWavelets:
    finalWavelets.append(morphed)
finalWavelets.append(wtTarget)

waveletHelper.plotWavelets(finalWavelets)



# waveletHelper.plotWavelets([finalWavelets[0]])
# waveletHelper.plotWavelets([finalWavelets[1]])
# waveletHelper.plotWavelets([finalWavelets[2]])

audio = waveletHelper.audioFromWavelets(finalWavelets)

sounddevice.play(audio, sampleRate)

i = 1
# time.sleep(4)