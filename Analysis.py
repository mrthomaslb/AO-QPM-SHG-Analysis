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
import matplotlib.pyplot as plt
from tkinter import filedialog
from matplotlib import rc

os.system("cls" if os.name == "nt" else "clear")

############################### VARIABLES ###############################
lmdas = [402]        #must be between min_wavelength and max_wavelength
smooth_factor = 11   #must be integer less than length of the array
min_wavelength = 395 #wavelengths must be between 348.9 nm and 561.7 nm
max_wavelength = 416 #max_wavelength must be greater than min_wavelength
#########################################################################

# Program header
print("---------------------------------------------------")
print(" Analysis Program for Counterpropagating Scan Data")
print(" Authors: R. Camuccio, T. Lehman-Borer, and A. Lytle")
print(" Version: 2.0")
print("---------------------------------------------------")
print()
 
#### FUNCTIONS ####
def Smooth2(position_array, wavelength_array, intensity_array, smooth_factor):
    smooth_int = np.zeros_like(intensity_array)
    edge_pixels = (smooth_factor-1)//2

    shape_array = np.shape(intensity_array)
    nWl = shape_array[0]
    nPos = shape_array[1]
    
    for i in range(nPos):
        for j in range(edge_pixels, nWl-edge_pixels):
            smooth_int[j,i] = (intensity_array[j-edge_pixels:j+edge_pixels+1,i]).mean()
    
    return smooth_int

def Smooth(position_array, wavelength_array, intensity_array, smooth_factor):
	""" This function accepts a wavelength and intensity array and returns a smoothed intensity array """

	# Create temporary list for value handling
	new_list = []

	# Calculate edge pixels to avoid smoothing
	edge_pixels = (smooth_factor - 1) // 2

	# Initialize sum
	current_sum = 0

	# Place front edge values into list
	for i in range(len(position_array)): #for each spectrum,
		for j in range(edge_pixels):   #
			new_list.append(intensity_array[j])

		# Place values of interest into smoothing algorithm
		for j in range(edge_pixels, len(intensity_array)-edge_pixels):

			# Crop the array around the pixels of interest
			crop_array = intensity_array[j-edge_pixels:j+edge_pixels+1]

			# Average crop_array into one value
			for k in range(smooth_factor):
				current_sum += crop_array[k]
			other_sum = np.sum(crop_array[0:smooth_factor]) #This is a single value, but current_sum is a 200x1 array
			#print(current_sum, type(current_sum))
			average = current_sum / smooth_factor


			# Place averaged value into output list
			new_list.append(average)

			# Reset sum
			current_sum = 0

		# Place rear edge values into list
		for j in range(edge_pixels):
			new_list.append(intensity_array[len(intensity_array)-edge_pixels+j])

	# Convert list into array
	intensity_array = np.asarray(new_list)
 
	# Return smoothed intensity array
	return intensity_array

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

def CropData(wavelength_array, intensity_array, spectrum_array, min_wavel, max_wavel):
	""" This function accepts a wavelength and intensity array and returns a cropped wavelength and intensity array """

	# Calculation of minimum/maximum pixel number
	P_min = wavel_to_pixel(min_wavel)
	P_max = wavel_to_pixel(max_wavel)

	# Crop arrays
	intensity_array = intensity_array[P_min:P_max]
	wavelength_array = wavelength_array[P_min:P_max]
	spectrum_array = spectrum_array[P_min:P_max]

	return wavelength_array, intensity_array, P_min, spectrum_array
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

# Prompt user input of smoothing factor
print
print("Length of input array = " + str(len(wavelengths[0])))
######################################################

################## Smooth data & normalization spectra ##################
DeltaIntSm = Smooth2(positions, wavelengths, DeltaInt, smooth_factor)
print("Smoothed")

SpectraWOCPSm = Smooth2(positions, wavelengths, SpectraWOCP, smooth_factor)
print("Smoothed Spectrum")

#Reduce noise by subtracting to 0
offsetvalue = np.mean(SpectraWOCPSm[0:387]) #387 is the pixel for 375 nm
SpectraWOCPSm -= offsetvalue #offsetvalue is the average of all noise values from 350 nm to 375 nm for all the spectra taken in this scan
###########################################################################

################## Crop data ##################
CroppedData = CropData(np.transpose(wavelengths), DeltaIntSm, SpectraWOCPSm, min_wavelength, max_wavelength)
wavelengthsCr = CroppedData[0]
DeltaIntSmCr = CroppedData[1]
MinPixel = CroppedData[2]
SpectraWOCPSmCr = CroppedData[3]
######################################################
print("Cropped")

################## Normalize data ##################
DeltaIntNorm = np.zeros_like(DeltaIntSmCr)

for i in range(scan_length):
    DeltaIntNorm[:,i] = DeltaIntSmCr[:,i] / SpectraWOCPSmCr[:,i]
######################################################
print("Normalized")

################## Plot data ##################
xmin=positions[0].min()
xmax=positions[0].max()
ymin=wavelengthsCr[:,0].min()
ymax=wavelengthsCr[:,0].max()
lmda_count = 0

for pixel in pixels:
    plt.rc('font.serif')
    fig1 = plt.figure()
    fig1.suptitle(title, fontsize=20)
    
    ax1 = fig1.add_subplot(221)
    im1 = ax1.imshow(DeltaIntSmCr, vmin=DeltaIntSmCr.min(), vmax=DeltaIntSmCr.max(), interpolation="hanning",
    origin='lower', extent=[xmin, xmax, ymin, ymax])
    ax1.set_aspect((xmax-xmin)/(ymax-ymin))
    plt.colorbar(im1)
    plt.title('Raw Spectrum')
    plt.xlabel(r'Relative position ($\mu$m)')
    plt.ylabel("Wavelength (nm)")

    ax2 = fig1.add_subplot(222)
    im2 = ax2.imshow(DeltaIntNorm, vmin=DeltaIntNorm.min(), vmax=DeltaIntNorm.max(), interpolation="hanning",
    origin='lower', extent=[xmin, xmax, ymin, ymax])
    ax2.set_aspect((xmax-xmin)/(ymax-ymin))
    plt.colorbar(im2)
    plt.title('Normalized Spectrum')
    plt.xlabel(r'Relative position ($\mu$m)')
    plt.ylabel("Wavelength (nm)")
                     
    ax3 = fig1.add_subplot(223)
    plt.plot(positions[0], DeltaIntNorm[pixel-MinPixel])
    plt.title('%s nm Lineout' % lmdas[lmda_count])
    plt.xlabel(r'Relative position ($\mu$m)')
    plt.ylabel("% Change in Intensity")
                     
    ax4 = fig1.add_subplot(224)
    plt.plot(wavelengthsCr[:,0], SpectraWOCPSmCr[:,0])
    plt.title('WOCP Spectrum')
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity (arb. units)")
    plt.show()
    lmda_count += 1
######################################################
