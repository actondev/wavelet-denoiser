import numpy, WindowBundle

data = numpy.array([3, -4, 6, -8, 7])
band1 = WindowBundle.WindowBundle(data)
print(band1.getMax())

