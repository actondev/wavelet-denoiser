s = 'hello mothafuckah'
print(s)
import time

import soundfile as sf
import sounddevice as sd
from noiseProfiler import NoiseProfiler

data, fs = sf.read('../samples/alex_f16.wav')
# if it's stereo it will have 2 columns.. so, checking for number of columns and if there is more than 1,
# transpose & keep the first row
if (len(data.shape) > 1):
    data = data.T[0]

from denoise import Denoiser

denoise = Denoiser()
noiseProfile = NoiseProfiler(data)

# dataN = denoise.padArray(dataN, len(data))
# dataN = noiseProfile.getNoiseOrZero()
dataN = noiseProfile.getNoiseDataPredicted()
print("dataN length:" + str(len(dataN)))
print("data length:" + str(len(data)))

# dataDenoised = denoise.denoise_wavedec(Xin=data, Nin=dataN)
dataDenoised = denoise.denoise_wpa(Xin = data, Nin= dataN)

import test_play
test_play.play(sd, dataDenoised, fs)

time.sleep(5)
