# -*- coding: utf-8 -*

import numpy as np
import matplotlib.pyplot as plt

#Load positions into the first column
shg = np.zeros((200,6))
shg[:,0] = np.loadtxt('./scan2lineouts.dat')[:,0]

#Load each lineout
for x in range(1,6):
    shg[:,x] = np.loadtxt('./scan'+str(2*x)+'lineouts.dat')[:,2]

#set all of the lineouts in phase
roll = [7,3,0,13,22]
for col in range(1,6):
    shg[:,col]=np.roll(shg[:,col],roll[col-1])#-12) #un-comment and remove close-paren to lower how much each one is shifted
    #now I want to set all of the rolled values to 0
    shg[0:roll[col-1]+1:,col]=np.zeros_like(shg[0:roll[col-1]+1:,col])

#The beam ratio with each lineout (in order)
ratios = [420/97, 320/97, 220/98, 121/97, 80/97]
scal_rat = []
tickLabels = []
count = 1
for r in ratios:
    scal_rat.append(.07*r)
    tickLabels.append('r='+str(r)[:4])
    shg[:,count] = [x+scal_rat[-1] for x in shg[:,count]]
    #Add the last scaled to every term in shg[:,1,2,3...]
    count+=1

fontSize = 32
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
for i in range(5):
    #dotted lines for axes
    ax1.plot([-1,1],[scal_rat[i],scal_rat[i]],'--', color = '.5')
    #actual lineouts
    ax1.plot(shg[:,0],shg[:,(i+1)], lw=2)
ax1.set_ylim(min(scal_rat)-.02,max(scal_rat)+.05)
ax1.set_xlim(-1,1)
ax1.set_xlabel('Relative Delay ($\mu$m)',fontsize=fontSize)
#ax1.set_ylabel('Second harmonic generation (a.u.)',fontsize=fontSize)
ax1.set_yticks(scal_rat)
ax1.set_yticklabels(tickLabels,fontsize=fontSize)
for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(fontSize)

fig1.tight_layout()
fig1.show()
