import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = plt.axes(projection="3d")
# z = np.linspace(0,1,100)
z = np.arange(0, 5 * np.pi, 0.1)
x = np.cos(z)
y = np.sin(z)
line, = ax.plot3D(x, y, z, "green")

# ax.set( xlabel='Z')
# ax.set( ylabel='X')
# ax.set( zlabel='Y')
ax.set( xlabel='X')
ax.set( ylabel='Y')
ax.set( zlabel='Z')
# ax.plot3D(y,z, "green")
ax.view_init(0, -180, 0 )

plt.show()

