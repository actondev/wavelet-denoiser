"""
Signal analysis useful functions
"""

import math
import numpy
import windowBundle


class SignalAnalyzer:
    'Signal analyzer'

    def __init__(self,
                 data,
                 sampleRate
                 ):
        self.data = data
        self.sampleRate = sampleRate
        self.windows = None

    def getRMSIgnoringSilence(self, silenceThreshold, timeBin=0.4):
        power = 0
        binSize = math.ceil(timeBin*self.sampleRate)
        self.windows = self.extractWindows(self.data, binSize)
        nonSilenceRMS = list()
        for window in self.windows:
            rms = window.getRMS()
            # add some check if rms>threshold, meaning it's a non-silent area
            nonSilenceRMS.append(rms)

        # getting the average rms
        averageRMS = numpy.average(nonSilenceRMS)

        return averageRMS

    # mean absolute
    def getMAIgnoringSilence(self, silenceThreshold, timeBin=0.4):
        binSize = math.ceil(timeBin*self.sampleRate)
        self.windows = self.extractWindows(self.data, binSize)
        metricList = list()
        for window in self.windows:
            ma = window.getMA()
            # add some check if rms>threshold, meaning it's a non-silent area
            metricList.append(ma)

        # getting the average rms
        avgMetric = numpy.average(metricList)

        return avgMetric

    def extractWindows(self, data, binSize):
        windows = list()
        dataLength = len(data)
        nWindows = math.ceil(dataLength / binSize)
        lastWindowPaddingSamples = dataLength - nWindows * binSize
        for i in range(0, nWindows):
            windowBeginning = i * binSize
            windowEnd = windowBeginning + binSize
            windowData = data[windowBeginning:windowEnd]
            # checking wether we need to pad the last band
            if(i == nWindows - 1 and windowEnd - windowBeginning < binSize):
                paddingLength = windowEnd - windowBeginning - binSize
                paddingArray = numpy.zeros(paddingLength)
                windowData = numpy.concatenate(windowData, paddingArray)
            window = windowBundle.WindowBundle(windowData, i)
            windows.append(window)

        return windows

    @staticmethod
    def db(value):
        return 20*math.log10(value)

    @staticmethod
    def adjustDB(data, adjustDB):
        factor = math.pow(10, adjustDB/20)
        return data*factor
