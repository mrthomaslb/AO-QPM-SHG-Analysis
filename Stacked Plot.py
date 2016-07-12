# -*- coding: utf-8 -*

import numpy as np
import matplotlib.pyplot as plt

#Load positions into the first column
shg = np.zeros((200,10))
shg[:,0] = np.loadtxt('./scan2lineouts.dat')[:,0]

#Load each lineout
for x in range(1,10):
    shg[:,x] = np.loadtxt('./scan'+str(x+1)+'lineouts.dat')[:,3]

#The beam ratio with each lineout (in order)
ratios = [420/97, 371/97, 320/97, 269/97, 220/98, 171/96, 121/97, 1., 80/97]
scal_rat = []
tickLabels = []
count = 1
for r in ratios:
    scal_rat.append(.1*r)
    tickLabels.append('r='+str(r)[:4])
    shg[:,count] = [x+scal_rat[-1] for x in shg[:,count]]
    #Add the last scaled to every term in shg[:,1,2,3...]
    count+=1

fontSize = 16
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
for i in range(9):
    #dotted lines for axes
    ax1.plot([-1.38,1.38],[scal_rat[i],scal_rat[i]],'--', color = '.5')
    #actual lineouts
    ax1.plot(shg[:,0],shg[:,(i+1)], lw=2)
ax1.set_ylim(min(scal_rat)-.02,max(scal_rat)+.05)
ax1.set_xlim(-1.38,1.38)
ax1.set_xlabel('Relative Delay ($\mu$m)',fontsize=fontSize)
ax1.set_ylabel('Second harmonic generation (a.u.)',fontsize=fontSize)
ax1.set_yticks(scal_rat)
ax1.set_yticklabels(tickLabels,fontsize=fontSize)
for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(fontSize)

fig1.tight_layout()
fig1.show()