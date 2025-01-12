import matplotlib.pyplot as plt
import numpy

data_points = [1,2,2,2,2,2,2,3,4,5,5,5,6,6,6,7,7,7,8,8]
bin = numpy.arange(numpy.min(data_points), numpy.max(data_points) + 2)
hist, bins = numpy.histogram(data_points,bins=bin)
print(hist, bins)
plt.stairs(hist, bins)
plt.show()
