"""
Cross Correlation Index
"""
import argparse
import helperFunctions
import numpy as np
import math

debug=0

def fdebug(text):
    if(debug!=0):
        print(text)

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

meanA = np.mean(dataA)
meanB = np.mean(dataB)

sumDiffsASquared = 0;
sumDiffsBSquared = 0;
sumNominator = 0;
for i in range(minLength):
    diffA = dataA[i] - meanA;
    diffB = dataB[i] - meanB;
    sumNominator += diffA*diffB;

    sumDiffsASquared += diffA**2;
    sumDiffsBSquared += diffB**2;

cii = sumNominator/(math.sqrt(sumDiffsASquared*sumDiffsBSquared))
cii = round(cii,3)

print(str(cii))