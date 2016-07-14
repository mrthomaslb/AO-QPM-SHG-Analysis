# -*- coding: utf-8 -*-
"""
Created on Tue May 24 09:18:45 2016
@author: amylytle
"""

""" Program initialization """

# Import modules
import os
import math
import numpy as np
from tkinter import filedialog

os.system("cls" if os.name == "nt" else "clear")

############################### VARIABLES ###############################
lmdas = [402,406]        #must be between min_wavelength and max_wavelength
smooth_factor = 11   #must be integer less than length of the array
min_wavelength = 395 #wavelengths must be between 348.9 nm and 561.7 nm
max_wavelength = 415 #max_wavelength must be greater than min_wavelength
#########################################################################

# Program header
print("---------------------------------------------------")
print(" Analysis Program for Counterpropagating Scan Data")
print(" Authors: R. Camuccio, T. Lehman-Borer, and A. Lytle")
print(" Version: 2.0")
print("---------------------------------------------------")
print()
 
#### FUNCTIONS ####
def Smooth(intensity_array, smooth_factor):
    smooth_int = np.zeros_like(intensity_array)
    edge_pixels = (smooth_factor-1)//2

    shape_array = np.shape(intensity_array)
    nWl = shape_array[0]
    nPos = shape_array[1]
    
    for i in range(nPos):
        for j in range(0,edge_pixels):
            smooth_int[j,i] = intensity_array[j,i]
        for j in range(edge_pixels, nWl-edge_pixels):
            smooth_int[j,i] = np.add.reduce(intensity_array[j-edge_pixels:j+edge_pixels+1,i])/smooth_factor
        for j in range(nWl-edge_pixels,nWl):
            smooth_int[j,i] = intensity_array[j,i]
    
    return smooth_int

def wavel_to_pixel(wavelength):
	""" This function accepts a wavelength value and returns the corresponding pixel value """
 
	A0 = 348.4316445
	A1 = 0.069763835
	A2 = -2.98682E-6
	B0 = A0-((A1**2)/(4*A2))
	B1 = (A1)/(2*A2)

	# Calculation of minimum/maximum pixel number
	pixel = int(math.floor(-(math.sqrt(((wavelength-B0)/A2)))-B1))
     
	return pixel
########################

################## Read in data ##################
print('Please select the A File.')
user_input1 = filedialog.askopenfile()
print('Please select the B File.')
user_input2 = filedialog.askopenfile()

path = str(user_input1)
position = path.find('scan')
if path[position+5]=='a':
    title = path[position-11:position+5]
else:
    title = path[position-11:position+6 ]
#I could do the same thing with the B File to check if the user selected non-matching files

raw_data = np.loadtxt(user_input1)
wocp = np.loadtxt(user_input2)

scan_length = raw_data.shape[0] - 2

#Disassembling the A File for useful parts
DeltaInt = raw_data[0:scan_length] #DeltaInt is an array of the differences in intensity
wavelengths = raw_data[scan_length:scan_length+1]
positions = raw_data[scan_length+1:scan_length+2]*1.38 #Coefficient accounts for piezo error

positions = positions[:,0:scan_length] #Because there are more wavelengths than positions for any scan we do, we have to clip this down

DeltaInt = np.transpose(DeltaInt) #now each column is a different spectrum, so it matches the B File data (3648x200)
SpectraWOCP = np.zeros_like(DeltaInt)

for i in range (0, scan_length):
    SpectraWOCP[:,i] = wocp[:,2*i]

pixels = []
for lmda in lmdas:
    pixel=wavel_to_pixel(lmda)
    pixels.append(pixel)
######################################################

################## Smooth data & normalization spectra ##################
DeltaIntSm = Smooth(DeltaInt, smooth_factor)
SpectraWOCPSm = Smooth(SpectraWOCP, smooth_factor)

#Reduce noise by subtracting to 0
offsetvalue = np.mean(SpectraWOCPSm[0:387]) #387 is the pixel for 375 nm
SpectraWOCPSm -= offsetvalue #offsetvalue is the average of all noise values from 350 nm to 375 nm for all the spectra taken in this scan
###########################################################################

################## Crop data ##################
P_min = wavel_to_pixel(min_wavelength)
P_max = wavel_to_pixel(max_wavelength)

# Crop arrays
DeltaIntSmCr = DeltaIntSm[P_min:P_max]
wavelengthsCr = np.transpose(wavelengths)[P_min:P_max]
SpectraWOCPSmCr = SpectraWOCPSm[P_min:P_max]
######################################################

################## Normalize data ##################
DeltaIntNorm = np.zeros_like(DeltaIntSmCr)

for i in range(scan_length):
    DeltaIntNorm[:,i] = DeltaIntSmCr[:,i] / SpectraWOCPSmCr[:,0]
######################################################

#Determining filename  
scan_number = input('Scan #: ')
filename = './scan' + scan_number + 'lineouts.dat'

################## Save data to file ##################
lineouts = np.zeros((np.shape(positions)[1]+1,len(pixels)+1))
lineouts[1:,0] = positions[0]
for i in range(len(lmdas)):
    #put the wavelength in row 0
    lineouts[0:1:,i+1]=lmdas[i]
    lineout = DeltaIntNorm[pixels[i]-P_min]
    #put the lineout below
    lineouts[1:,i+1]=lineout
np.savetxt(filename,lineouts)
######################################################
