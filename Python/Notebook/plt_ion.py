import matplotlib.pyplot as plt
import numpy as np

##############
#  plt.ion =='hold on' in matlab
##############
t = np.arange(0, 10, .1)
plt.ion()
for w in range(1, 4):
    x = np.sin(w*t)
    plt.plot(t,x)

plt.ioff()
plt.show()

##############
# plt: ion, pause, ioff, show
##############
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(range(10), range(10))
plt.ion()
plt.show()

for i in range(10):
    ax.scatter(i, i*(1/2))
    plt.pause(.1)

plt.ioff()
plt.show()

##############
# remove scatter
##############
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(range(10), range(10))
plt.ion()
plt.show()

for i in range(10):
    point = ax.scatter(i, i * (1 / 2))
    plt.pause(.1)
    point.remove()

plt.ioff()
plt.show()

