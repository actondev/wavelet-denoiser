"""
A class to morph a wavelet packet 
"""

import pywt


class WaveletMorpher():

    def __init__(self, original: pywt.WaveletPacket, target: pywt.WaveletPacket, dbName='db8'):
        self.original = original
        self.target = target
        self.dbName = dbName
        self.wlevels = self.original.maxlevel

    def morph(self, steps=1):
        if self.target == None:
            return self.original

        diff = self.__extractDiff()
        morphedList = list()
        for i in range(steps):
            morphedList.append(self.__morphWavelet(diff, i, steps))
        
        return morphedList

    def __extractDiff(self):
        leafNodes = [node.path for node in self.original.get_level(
            self.original.maxlevel, 'freq')]
        diffLeafData = {}

        for node in leafNodes:
            originalLeafData = self.original[node].data
            targetLeafData = self.target[node].data
            diffLeafData[node] = targetLeafData - originalLeafData
        
        return diffLeafData

    def __morphWavelet(self, diff, step, steps):
        step = step + 1
        morphed = pywt.WaveletPacket(
            data=None, wavelet=self.dbName, mode='symmetric')
        for key, value in diff.items():
            originalData = self.original[key].data
            diffData = diff[key]*step/(steps+1)
            morphedData =  originalData + diffData
            morphed[key] = morphedData
        
        return morphed
