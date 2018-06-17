"""
Calculates the correlation between two audio files
"""
import argparse
import helperFunctions
import pywt
import numpy as np

debug=0

def fdebug(text):
    if(debug!=0):
        print(text)

dbName='db8'

parser = argparse.ArgumentParser()

parser.add_argument(
    "-a","--a", help="the relative or absolute path of the sound file 1", required=True)
parser.add_argument(
    "-b", "--b", help="the relative or absolute path of the sound file 2", required=True)
args = parser.parse_args()

# removing the quotes passed
args.a = args.a.replace("\"", "")
args.a = args.a.replace("'", "")

args.b = args.b.replace("\"", "")
args.b = args.b.replace("'", "")

dataA, sampleRateA = helperFunctions.readMono(args.a)
dataB, sampleRateB = helperFunctions.readMono(args.b)

minLength = np.minimum(len(dataA), len(dataB))

dataA = helperFunctions.normalize(dataA)
dataB = helperFunctions.normalize(dataB)

dataA=dataA[0:minLength]
dataB=dataB[0:minLength]

waveletA = pywt.wavedec(dataA, dbName, 'symmetric')
waveletB = pywt.wavedec(dataB, dbName, 'symmetric')
nBands =len(waveletA)

msePerBand = np.array([]);
weightedMSEPerBand = np.array([]);
waveletCoeffsReference = len(waveletA[0]);
# keeping the first 4.. approximation/detail coefficients: they are the most important ones..?
for node in range(4):
    # print('band: ' + str(node))
    bandDataA = waveletA[node]
    bandDataB = waveletB[node]
    bandMSE = np.square(np.subtract(bandDataA, bandDataB)).mean()
    msePerBand = np.append(msePerBand, bandMSE)
    bandWeight = waveletCoeffsReference/len(bandDataA)
    bandWeight = bandWeight*bandWeight
    fdebug('\tband weight: ' + str(bandWeight))
    weightedMSE = bandMSE*bandWeight;
    weightedMSEPerBand = np.append(weightedMSEPerBand, weightedMSE)
    fdebug('\tbandMSE: ' + str(node) + ' : ' + str(bandMSE) + ', length ' + str(len(bandDataA)) + ' weight: ' + str(bandWeight))
    fdebug('\tweightedMSEPerBand: ' + str(node) + ' : ' + str(weightedMSE))    

fdebug('average of weighted MSE ' + str(np.average(weightedMSEPerBand)))
fdebug('sum of weighted MSE ' + str(np.sum(weightedMSEPerBand)))
print(np.average(weightedMSEPerBand))