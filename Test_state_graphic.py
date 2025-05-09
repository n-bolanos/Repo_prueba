from matplotlib import pyplot
from random import random
state = ['i','e','i','i','e','i','i','e','i','e','i','i','e','i','e','i','i','e','i']
times = []
count = 0
for i in state:
    try:
        times.append(times[count]+random())
        count +=1
    except IndexError:
        times.append(random())
    
print(times)

fig,axis = pyplot.subplots()
axis = pyplot.plot(times,state)
pyplot.show()