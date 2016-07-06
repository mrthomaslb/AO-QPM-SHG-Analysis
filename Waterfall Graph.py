 # -*- coding: utf-8 -*-

from mpl_toolkits.mplot3d import Axes3D #needed for projection='3d'
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

def lineout_to_array():
    dat = filedialog.askopenfile()
    datload = np.loadtxt(dat)
    datcrop = datload[:,1:4]
    return datcrop

pick = int(input("""Select one of the following:
    1: 402 nm (scans 11-21)
    2: 404 nm (scans 2-10)
    3: 411 nm (scans 2-10)

>>>"""))
while pick!=1 and pick!=2 and pick!=3:
    pick = input("""Please just type 1, 2, or 3.

>>>""")

if pick==2 or pick==3:
    zs = [420/97, 371/97, 320/97, 269/97, 220/98, 171/96, 121/97, 1, 80/97]
    zcounter = 1
else:
    zs = [413/96, 311/96, 120/97, 100/97, 75/98, 50/97, 25/97, 219/98, 170/98, 271/98, 371/98]
    zcounter = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

def cc(arg):
    return colorConverter.to_rgba(arg, alpha=0.6)

verts = []

for z in zs:
    xs = list(np.arange(-1.38, 1.38, 0.0138))
    zcounter += 1
    print('Select scan %d lineout' % zcounter)
    if pick==1:
        ys = lineout_to_array()[:,0:1]
    elif pick==2:
        ys = lineout_to_array()[:,1:2]
    else:
        ys = lineout_to_array()[:,2]
    verts.append([(-1.38,0)]+list(zip(xs, ys))+[(1.382
    ,0)])

poly = PolyCollection(verts, facecolors=[cc('r'), cc('g'), cc('b'), cc('y')])
poly.set_alpha(0.7)
ax.add_collection3d(poly, zs=zs, zdir='y')

ax.set_xlabel('Position')
ax.set_xlim3d(-1.38, 1.38)
ax.set_ylabel('Power Ratio')
ax.set_ylim3d(0, 4.5)
ax.set_zlabel('% Change in Intensity')
ax.set_zlim3d(-.05, .05)

plt.show()
