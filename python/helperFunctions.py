import soundfile
import numpy
import os


def padArray(srcArr, targetSize):
    targetArr = srcArr[:]
    print("current len " + str(len(targetArr)))
    while (len(targetArr) < targetSize):
        targetArr = numpy.concatenate((targetArr, srcArr))
    # removing possible extra data
    # the second argument in slice is the id of the last elem NOT INCLUDED
    targetArr = targetArr[0:targetSize]
    return targetArr


def readMono(filePath):
    # print("trying to open " + filePath)
    data, sampleRate = soundfile.read(filePath)

    # if it's stereo it will have 2 columns.. so, checking for number of columns and if there is
    # more than 1, transpose & keep the first row
    if len(data.shape) > 1:
        data = data.T[0]

    return data, sampleRate


def normalize(data):
    peakMax = numpy.max(data)
    peakMin = numpy.min(data)
    peakAbs = numpy.max([peakMax, -peakMin])
    return 1/peakAbs*data


def getFileNameWithoutExtension(filePath):
    baseName = os.path.basename(filePath)
    fileName, fileExtension = os.path.splitext(baseName)

    return fileName


def getFileNameExtension(filePath):
    baseName = os.path.basename(filePath)
    fileName, fileExtension = os.path.splitext(baseName)

    return fileExtension