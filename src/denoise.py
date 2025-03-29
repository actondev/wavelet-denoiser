''' Wavelet Denoiser '''

import numpy
import pywt
from windowBundle import WindowBundle
from noiseProfiler import NoiseProfiler


class Denoiser:
    'Basic denoiser wrapper for keeping store of the settings'

    def __init__(self,
                 a=2,
                 b=1,
                 c=2,
                 d=0.1,
                 akGrad=0.5,
                 akOffset=1,
                 akSlope='ASC',
                 wlevels=8,
                 waveletName='db8',
                 filterType=2,
                 method='wpa'
                 ):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.akGrad = akGrad
        self.akOffset = akOffset
        self.waveletName = waveletName
        self.akSlope = akSlope
        self.wlevels = wlevels
        self.filterType = filterType
        self.method = method
        print("Denoiser options: ")
        print("a: " + str(a))
        print("b: " + str(b))
        print("c: " + str(c))
        print("d: " + str(d))
        print("akGrad: " + str(akGrad))
        print("akOffset: " + str(akOffset))
        print("filterType: " + str(filterType))
        print("method: " + method)
        print("wavelet: " + waveletName)

    def padArray(self, srcArr, targetSize):
        targetArr = srcArr[:]
        print("current len " + str(len(targetArr)))
        while (len(targetArr) < targetSize):
            targetArr = numpy.concatenate((targetArr, srcArr))
        # removing possible extra data
        # the second argument in slice is the id of the last elem NOT INCLUDED
        targetArr = targetArr[0:targetSize]
        return targetArr

    def denoise(self, Xin, Nin):
        if (self.method == 'wpa'):
            return self.denoise_wpa(Xin, Nin)
        elif (self.method == 'dwt'):
            return self.denoise_wavedec(Xin, Nin);

    def denoise_wpa(self, Xin, Nin):
        # print("Xin len " + str(len(Xin)))
        X = pywt.WaveletPacket(Xin, self.waveletName,
                               'symmetric', self.wlevels)
        N = pywt.WaveletPacket(Nin, self.waveletName,
                               'symmetric', self.wlevels)
        Y = pywt.WaveletPacket(
            data=None, wavelet=self.waveletName, mode='symmetric')
        # print("X len" + str(X.maxlevel))
        # the output of pywt.wavedec will be arrays (trees) of size/length wlevels+1
        # so at the index of 1[wlevels] we have the "leaf node"
        nBands = pow(2, self.wlevels)
        XleafNodes = [node.path for node in X.get_level(self.wlevels, 'freq')]
        Ak = self.linearAk(nBands, self.akSlope)
        # print(Ak)
        # print(XleafNodes)
        bandId = 0
        numOfBands = len(XleafNodes)
        counter = 0;
        for node in XleafNodes:
            print(str(round(counter/numOfBands*100)) + "%")
            bandAk = Ak[bandId]
            bandId += 1
            XbandData = X[node].data
            NbandData = N[node].data
            YbandData = self.denoise_band(XbandData, NbandData, bandAk)
            Y[node] = YbandData
            counter=counter+1

        # reconstructing the audio from Y
        Yaudio = Y.reconstruct(update=False)
        return Yaudio

    def denoise_wavedec(self, Xin, Nin):
        """ Multilevel 1D Discrete Wavelet Transform of data """
        # print("Xin len " + str(len(Xin)))
        X = pywt.wavedec(Xin, self.waveletName, 'symmetric')
        N = pywt.wavedec(Nin, self.waveletName, 'symmetric')
        Y = []
        # print("X len" + str(X.maxlevel))
        # the output of pywt.wavedec will be arrays (trees) of size/length wlevels+1
        # so at the index of 1[wlevels] we have the "leaf node"
        nBands = len(X)
        Ak = self.linearAk(nBands, self.akSlope)
        # print(Ak)
        # print(XleafNodes)
        bandId = 0
        for node in range(nBands):
            print(str(round(bandId/nBands*100)) + "%")
            bandAk = Ak[bandId]
            XbandData = X[node]
            NbandData = N[node]
            YbandData = self.denoise_band(XbandData, NbandData, bandAk)
            Y.append(YbandData)
            bandId += 1            

        # reconstructing the audio from Y
        Yaudio = pywt.waverec(Y, self.waveletName, mode='symmetric')
        return Yaudio;

    def denoise_band(self, X, N, ak):
        Px = self.aPowered(X)
        Nabs = numpy.absolute(N)
        Pn = numpy.sum(numpy.power(Nabs, self.a)) / len(N)
        PxAverage = self.powerAveraged(Px)
        Hd = self.noiseFilter(PxAverage, Pn, ak)
        Hb = self.signalPresenceFilter(PxAverage, Pn, ak)
        Y = X * Hd * Hb
        if(self.filterType != 1):
            # in the type II we average/smooth the Px taking into account the
            # a-power of the prediction about the original signal
            predictedPower = self.aPowered(Y)
            PxAverageII = self.powerAveragedII(Px, predictedPower)
            if(self.filterType == 2):
                Hd = self.noiseFilter(PxAverageII, Pn, ak)
            elif(self.filterType == 3):
                # hybrid - (reversed hybrid from the paper.. the paper version
                # was giving weird result)
                Hd = self.noiseFilter(PxAverage, Pn, ak)
            Hb = self.signalPresenceFilter(PxAverageII, Pn, ak)
            Y = X * Hd * Hb
        return Y

    def aPowered(self, X):
        Xabs = numpy.absolute(X)
        return numpy.power(Xabs, self.a)

    def powerAveraged(self, Px):
        nSamples = len(Px)
        Pout = numpy.zeros(nSamples)
        Pout[0] = Px[0]
        for i in range(1, nSamples):
            Pout[i] = self.d * Px[i] + (1 - self.d) * Pout[i - 1]
        return Pout

    def powerAveragedII(self, Px, Py):
        nSamples = len(Px)
        Pout = numpy.zeros(nSamples)
        Pout[0] = Px[0]
        for i in range(1, nSamples):
            Pout[i] = self.d * Px[i] + (1 - self.d) * Py[i - 1]
        return Pout

    def noiseFilter(self, Px, Pn, ak):
        nSamples = len(Px)
        Hd = numpy.zeros(nSamples)
        # iterating through the 'w' (from the paper)
        for i in range(0, nSamples):
            Hd[i] = pow((1 - self.c * Pn * ak / Px[i]), self.b)
        return Hd

    def linearAk(self, nBands, slope):
        # for a range(0,5) we get 0,1,2,3,4 (n-1 elements)
        Ak = numpy.array(range(0, nBands, 1)) / (nBands - 1)
        Ak = Ak * self.akGrad
        Ak = Ak + self.akOffset
        if slope == "desc":
            Ak = Ak[::-1]
        return Ak

    def signalPresenceFilter(self, Px, Pn, ak):
        nSamples = len(Px)
        Hbn = numpy.zeros(nSamples)
        # iterating through the 'w' (from the paper)
        for i in range(nSamples):
            if (Px[i] >= self.c * ak * Pn):
                Hbn[i] = 1
        return Hbn
