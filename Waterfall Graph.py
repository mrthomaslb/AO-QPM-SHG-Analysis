 # -*- coding: utf-8 -*-

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')


def cc(arg):
    return colorConverter.to_rgba(arg, alpha=0.6)

xs = np.arange(-1.38, 1.38, 0.1)
verts = []
zs = [4.329896907, 3.824742268, 3.298969072, 2.773195876, 2.244897959, 1.78125, 1.24742268, 1, 0.824742268]
for z in zs:
    ys = np.random.rand(len(xs))
    ys[0], ys[-1] = 0, 0
    verts.append(list(zip(xs, ys)))

poly = PolyCollection(verts, facecolors=[cc('r'), cc('g'), cc('b'),
                                         cc('y')])
poly.set_alpha(0.7)
ax.add_collection3d(poly, zs=zs, zdir='y')

ax.set_xlabel('Position')
ax.set_xlim3d(-1.38, 1.38)
ax.set_ylabel('Power Ratio')
ax.set_ylim3d(0, 4.5)
ax.set_zlabel('% Change in Intensity')
ax.set_zlim3d(0, 1)

plt.show()