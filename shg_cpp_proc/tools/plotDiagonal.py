# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:25:49 2014

@author: etienne

This scripts plots the SHG along a certain diagonal from the 2D graphs. The
initial time (where we start the diagonal) must be supplied to the code. Since
the diagonal is moving at the group velocity, plotting it follows the
evolution of a pulse.
"""

import numpy as np
import matplotlib.pyplot as plt


# Enter the location of the saved data files.
diagonalLoc = "../data/diagonal.dat"
xAxisLoc = "../data/xAxis.dat"
tAxisLoc = "../data/tAxis.dat"

# Loading files
diagonal = np.loadtxt(diagonalLoc)
xAxis = np.loadtxt(xAxisLoc)
tAxis = np.loadtxt(tAxisLoc)

sizeX = xAxis.size
sizeT = tAxis.size

print(diagonal.shape)
print(xAxis.shape)

firstCollisionPt = 16e-6
lastCollisionPt = 20e-6
numCollisionPts = 200

collisionPts = np.linspace(firstCollisionPt, lastCollisionPt,
                           num=numCollisionPts)

indexCol = 0

plt.figure()
plt.plot(xAxis, diagonal[:,indexCol], color='b')
plt.xlabel('Position (um)')
plt.show()