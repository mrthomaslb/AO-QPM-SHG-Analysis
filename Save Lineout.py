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

#### FUNCTIONS ####
def Smooth(position_array, wavelength_array, intensity_array, smooth_factor):
	""" This function accepts a wavelength and intensity array and returns a smoothed intensity array """

	# Create temporary list for value handling
	new_list = []

	# Calculate edge pixels to avoid smoothing
	edge_pixels = (smooth_factor - 1) // 2

	# Initialize sum and average
	current_sum = 0
	average = 0

	# Place front edge values into list
	for i in range(len(position_array)):
		for j in range(edge_pixels):
			new_list.append(intensity_array[j])

	# Place values of interest into smoothing algorithm
	for i in range(len(position_array)):
		for j in range(edge_pixels, len(intensity_array)-edge_pixels):

			# Crop the array around the pixels of interest
			crop_array = intensity_array[j-edge_pixels:j+edge_pixels+1]

			# Average crop_array into one value
			for k in range(0, len(crop_array)):
				current_sum = current_sum + crop_array[k]
			average = current_sum / smooth_factor

			# Place averaged value into output list
			new_list.append(average)

			# Reset sum and average
			current_sum = 0
			average = 0

	# Place rear edge values into list
	for i in range(len(position_array)):
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

def CropData(wavelength_array, intensity_array, spectrum_array):
	""" This function accepts a wavelength and intensity array and returns a cropped wavelength and intensity array """

	# Specify minimum wavelength
	min_wavelength = 395 
	max_wavelength = 420 

	# Calculation of minimum/maximum pixel number
	P_min = wavel_to_pixel(min_wavelength)
	P_max = wavel_to_pixel(max_wavelength)

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

lmda1 = 402
lmda2 = 404
lmda3 = 411

pixel1=wavel_to_pixel(lmda1)
pixel2=wavel_to_pixel(lmda2)
pixel3=wavel_to_pixel(lmda3)

pixel=wavel_to_pixel(lmda1)

smooth_factor = 11
######################################################

################## Smooth data & normalization spectra ##################
DeltaIntSm = Smooth(positions, wavelengths, DeltaInt, smooth_factor)

SpectraWOCPSm = Smooth(positions, wavelengths, SpectraWOCP, smooth_factor)

offsetvalue = np.mean(SpectraWOCPSm[0:387]) #387 is the pixel for 375 nm
SpectraWOCPSm -= offsetvalue #offsetvalue is the average of all noise values from 350 nm to 375 nm for all the spectra taken in this scan
###########################################################################

################## Crop data ##################
CroppedData = CropData(np.transpose(wavelengths), DeltaIntSm, SpectraWOCP)
wavelengthsCr = CroppedData[0]
DeltaIntSmCr = CroppedData[1]
MinPixel = CroppedData[2]
SpectraWOCPSmCr = CroppedData[3]
######################################################

################## Normalize data ##################
DeltaIntNorm = np.zeros_like(DeltaIntSmCr)

for i in range(scan_length):
    DeltaIntNorm[:,i] = DeltaIntSmCr[:,i] / SpectraWOCPSmCr[:,i]
######################################################

#Determining filename  
scan_number = input('Scan #: ')
filename = './scan' + scan_number + 'lineouts.dat'

################## Save data to file ##################
lineout1 = DeltaIntNorm[pixel1-MinPixel]
lineout2 = DeltaIntNorm[pixel2-MinPixel]
lineout3 = DeltaIntNorm[pixel3-MinPixel]
length = np.shape(lineout1)
lineouts = np.zeros((length[0],5))
lineouts[:,1] = lineout1
lineouts[:,2] = lineout2
lineouts[:,3] = lineout3
lineouts[:,0] = positions[0]
np.savetxt(filename,lineouts)
######################################################