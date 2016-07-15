# -*- coding: utf-8 -*-

from mpl_toolkits.mplot3d import Axes3D #needed for projection='3d'
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import random
import os

os.system("cls" if os.name == "nt" else "clear")

print("---------------------------------------------------")
print(" Waterfall Graph Program for Counterpropagating Scan Data")
print(" Author: T. Lehman-Borer")
print("---------------------------------------------------")
print()

# VARIABLES #
lmda = 404
ratios = [(420/97)**.5, (320/97)**.5, (220/98)**.5, (121/97)**.5, (80/97)**.5]
scan_length = 200
#############

print('Select all DAT files to plot')
filelist = filedialog.askopenfilenames()

#Load positions into the first column
shg = np.zeros((scan_length+1,len(filelist)+1))
shg[:,0] = np.loadtxt(filelist[0])[:,0]

#Load each lineout
for x in range(len(filelist)):
    load = np.loadtxt(filelist[x])
    wavelengths = []
    for col in range(np.shape(load)[1]):
        wavelengths.append(int(load[:1:,col]))
    #find correct column
    shg[:,x+1] = load[:,wavelengths.index(lmda)]

fig = plt.figure()
ax = fig.gca(projection='3d')

def cc(arg):
    return colorConverter.to_rgba(arg, alpha=0.6)

#initialize
verts = []
maxy = 0
miny = 0

for z in range(len(ratios)):
    xs = list(shg[1:,0])
    ys = list(shg[1:,z+1])
    verts.append([(max(xs),0)]+list(zip(xs, ys))+[(min(xs),0)])
    if max(ys) > maxy:
        maxy = max(ys)
    if min(ys) < miny:
        miny = min(ys)
colors = [cc('r'), cc('y'), cc('g'), cc('b'), cc('m'), cc('c'), cc('k'), cc('w')]
if len(ratios)<8:
    fc = colors[:len(ratios)]
else:
    fc = colors
    for c in range(len(ratios)-8):
        r = random.random()
        g = random.random()
        b = random.random()
        fc.append((r,g,b ))
poly = PolyCollection(verts, facecolors=fc)
poly.set_alpha(0.7) #transparency
ax.add_collection3d(poly, zs=ratios, zdir='y')

ax.set_xlabel('Position')
ax.set_xlim3d(min(xs), max(xs))
ax.set_ylabel('E Field Ratio')
ax.set_ylim3d(0, max(ratios))
ax.set_zlabel('Change in Intensity')
ax.set_zlim3d(miny,maxy)

plt.show()
