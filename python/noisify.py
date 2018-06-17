"""
Noisifies a source file
"""
import signalAnalyzer
import os
import sys
import argparse
import time
import soundfile
import sounddevice
import helperFunctions
import numpy

parser = argparse.ArgumentParser()

parser.add_argument(
    "-s", "--source", help="the relative or absolute path of the sound file you wish to noisify", required=True)
parser.add_argument(
    "-n", "--noise", help="the relative or absolute path of the noise sound file", required=True)
parser.add_argument(
    "-o", "--output", help="the relative or absolute path to store the nosified file", required=True)
parser.add_argument("--snr", default=3, type=int,
                    help="target snr (default: %(default)s)")

args = parser.parse_args()

# removing the quotes passed
args.source = args.source.replace("\"", "")
args.source = args.source.replace("'", "")

args.noise = args.noise.replace("\"", "")
args.noise = args.noise.replace("'", "")

args.output = args.output.replace("\"", "")
args.output = args.output.replace("'", "")

sourcePath = os.path.dirname(args.source)
sourceName = os.path.basename(args.source)

noisePath = os.path.dirname(args.noise)
noiseName = os.path.basename(args.noise)

dataSource, sampleRateSource = helperFunctions.readMono(args.source)
dataNoise, sampleRateNoise = helperFunctions.readMono(args.noise)

metricSource = signalAnalyzer.SignalAnalyzer(
    dataSource, sampleRateSource).getRMSIgnoringSilence(0.1)

metricSourceDB = signalAnalyzer.SignalAnalyzer.db(metricSource)

metricNoise = signalAnalyzer.SignalAnalyzer(
    dataNoise, sampleRateNoise).getRMSIgnoringSilence(0.1)

metricNoiseDB = signalAnalyzer.SignalAnalyzer.db(metricNoise)

noiseAdjustDb = (metricSourceDB - metricNoiseDB - args.snr)
dataNoiseAdjusted = signalAnalyzer.SignalAnalyzer.adjustDB(
    dataNoise, noiseAdjustDb)

metricNoiseAdj = signalAnalyzer.SignalAnalyzer(
    dataNoiseAdjusted, sampleRateNoise).getRMSIgnoringSilence(0.1)

metricNoiseAdjDB = signalAnalyzer.SignalAnalyzer.db(metricNoiseAdj)


if(sampleRateSource != sampleRateNoise):
    sys.exit(1)

print("Number of samples read: " + str(len(dataSource)))

dataNoiseAdjusted = helperFunctions.padArray(dataNoiseAdjusted, len(dataSource))

dataNoisified = dataSource + dataNoiseAdjusted
dataNoisified = helperFunctions.normalize(dataNoisified)

nameSource = helperFunctions.getFileNameWithoutExtension(args.source)
nameNoise = helperFunctions.getFileNameWithoutExtension(args.noise)
extension = helperFunctions.getFileNameExtension(args.source)

os.chdir(args.output)

targetFileName = nameSource + "_" + nameNoise + "_snr" + str(args.snr) + extension

soundfile.write(targetFileName, dataNoisified, sampleRateSource)

print("OK")