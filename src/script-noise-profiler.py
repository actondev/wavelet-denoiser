import soundfile
import sounddevice
import noiseProfiler
import argparse
import time
import os

parser = argparse.ArgumentParser()

parser.add_argument(
    "-f", "--file", help="the relative or absolute path of the sound file you wish to denoise", required=True)
args = parser.parse_args()
args.file = args.file.replace("\"", "")
args.file = args.file.replace("'", "")

filePath = os.path.dirname(args.file)
fileName = os.path.basename(args.file)
# we will now be working in the provided sample path -> so we will write
# there
os.chdir(filePath)

print("trying to open " + args.file)
data, sampleRate = soundfile.read(fileName)

# if it's stereo it will have 2 columns.. so, checking for number of columns and if there is
# more than 1, transpose & keep the first row
if len(data.shape) > 1:
    data = data.T[0]

print("Number of samples read: " + str(len(data)))


noiseProfiler = noiseProfiler.NoiseProfiler(data);
noiseProfiler.drawOriginalVsNoiseAndSingal()
noiseData = noiseProfiler.getNoiseDataPredicted()

sounddevice.play(noiseData, sampleRate)
time.sleep(4)
