# -*- coding: utf-8 -*

import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog

os.system("cls" if os.name == "nt" else "clear")

print("---------------------------------------------------")
print(" Stacked Plot Program for Counterpropagating Scan Data")
print(" Authors: E. Gagnon, T. Lehman-Borer, and A. Lytle")
print("---------------------------------------------------")
print()

# VARIABLES #
lmda = 404
ratios = [(420/97)**.5, (320/97)**.5, (220/98)**.5, (121/97)**.5, (80/97)**.5]
#Make sure that the values are E-Field ratios, not power ratios
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
    

#set all of the lineouts in phase
roll = [7,3,0,13,22]
for col in range(1,6):
    shg[:,col]=np.roll(shg[:,col],roll[col-1])
    #now I want to set all of the rolled values to 0
    shg[0:roll[col-1]+1:,col]=np.zeros_like(shg[0:roll[col-1]+1:,col])

#The beam ratio with each lineout (in order)
scal_rat = []
tickLabels = []
count = 1
for r in ratios:
    scal_rat.append(.25*r) #coefficient determines vertical spread of lineouts
    tickLabels.append('r='+str(r)[:4])
    shg[:,count] = [x+scal_rat[-1] for x in shg[:,count]]
    #Add the last scaled to every term in shg[:,1,2,3...]
    count+=1

fontSize = 16
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
for i in range(len(filelist)):
    #dotted lines for axes
    ax1.plot([-1,1],[scal_rat[i],scal_rat[i]],'--', color = '.5')
    #If the above line gives an index error, 'ratios' is too short
    #actual lineouts
    ax1.plot(shg[1:,0],shg[1:,(i+1)], lw=2)
ax1.set_ylim(min(scal_rat)-.02,max(scal_rat)+.06) #modify if clipping lineouts
ax1.set_xlim(-1,1)
ax1.set_xlabel('Relative Delay ($\mu$m)',fontsize=fontSize)
#ax1.set_ylabel('Second harmonic generation (a.u.)',fontsize=fontSize)
ax1.set_yticks(scal_rat)
ax1.set_yticklabels(tickLabels,fontsize=fontSize)
for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(fontSize)

fig1.tight_layout()
fig1.show()
