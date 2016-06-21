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
import tkFileDialog

os.system("cls" if os.name == "nt" else "clear")

# Program header
print("---------------------------------------------------")
print(" Analysis Program for Counterpropagating Scan Data")
print(" Authors: R. Camuccio, T. Lehman-Borer, and A. Lytle")
print(" Version: 2.0")
print("---------------------------------------------------")
print

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

			# Slice the array around the pixels of interest
			slice_array = intensity_array[j-edge_pixels:j+edge_pixels+1]

			# Average the sliced array into one value
			for k in range(0, len(slice_array)):
				current_sum = current_sum + slice_array[k]
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
	""" This function accepts a wavelength and intensity array and returns a sliced wavelength and intensity array """

	# Specify minimum wavelength
	print
	min_wavelength = input("Select minimum wavelength above 348.9 nm and below 561.7 nm: ")
	while min_wavelength < 348.9 or min_wavelength > 561.7:
		min_wavelength = input("ERROR! Minimum wavelength must be above 348.9 nm and below 561.7 nm: ")

	# Specify maximum wavelength
	print
	max_wavelength = input("Select maximum wavelength above 348.9 nm and below 561.7 nm: ")
	while max_wavelength < 348.9 or max_wavelength > 561.7:
		max_wavelength = input("ERROR! Maximum wavelength must be above 348.9 nm and below 561.7 nm: ")

	# Check that minimum and maximum are correct with respect to each other
	while max_wavelength <= min_wavelength:
		max_wavelength = input("ERROR! Maximum wavelength must be greater than minimum wavelength. Select another: ")

	# Calculation of minimum/maximum pixel number
	P_min = wavel_to_pixel(min_wavelength)
	P_max = wavel_to_pixel(max_wavelength)



	# Transpose wavelength array for slicing
	wavelength_array = np.transpose(wavelength_array)

	# Slice arrays
	intensity_array = intensity_array[P_min:P_max]
	wavelength_array = wavelength_array[P_min:P_max]
 	spectrum_array = spectrum_array[P_min:P_max]

	# Transpose wavelength array back to original transposition
	wavelength_array = np.transpose(wavelength_array)

	return wavelength_array, intensity_array, P_min, spectrum_array
########################

################## Read in data ##################
print('Please select the A File.')
user_input1 = tkFileDialog.askopenfile()
print('Please select the B File.')
user_input2 = tkFileDialog.askopenfile()

raw_data = np.loadtxt(user_input1)

wocp = np.loadtxt(user_input2)
wocp = np.transpose(wocp)
NormSpec = wocp[0] #This is the spectrum we're normalizing to.

m = raw_data.shape[0]
n = raw_data.shape[1]

scan_length = m - 2

DeltaInt = raw_data[0:scan_length]
wavelengths = raw_data[scan_length:scan_length+1]
positions = raw_data[scan_length+1:scan_length+2]*1.38

positions = np.transpose(positions)
positions = positions[0:scan_length]
pos=positions[scan_length-1]
posscale=pos[0]
positions = np.transpose(positions)

DeltaInt = np.transpose(DeltaInt)

lmda1 = 402 #int(raw_input("Select wavelength for relative position lineout: "))
lmda2 = 404
lmda3 = 410
lmda4 = 420

pixel1=wavel_to_pixel(lmda1)
pixel2=wavel_to_pixel(lmda2)
pixel3=wavel_to_pixel(lmda3)
pixel4=wavel_to_pixel(lmda4)

pixel=wavel_to_pixel(lmda1)

# Prompt user input of smoothing factor
print
print("Length of input array = " + str(len(wavelengths[0])))
smooth_factor = input("Smoothing factor: ")

# Check if smoothing factor is within reasonable bounds
while smooth_factor > len(wavelengths[0]):
	smooth_factor = input("Choose smoothing factor less than length of array: ")

# Check if smoothing factor is integer type
while smooth_factor != int(smooth_factor):
	smooth_factor = input("Choose smoothing factor that is integer type: ")
######################################################

################## Smooth data ##################
DeltaIntSm = Smooth(positions, wavelengths, DeltaInt, smooth_factor)
######################################################
print("Smoothed")

################## Smooth normalization spectrum ##################
NormSpecSm = Smooth(positions, wavelengths, NormSpec, smooth_factor)
#I just made the position_array and wavelength_array variables that I passed in
#the same as when I smoothed the data, but I don't know if this is correct.
######################################################
print("Smoothed Spectrum")

################## Crop data ##################
CroppedData = CropData(wavelengths, DeltaIntSm, NormSpecSm)
wavelengthsCr = CroppedData[0]
DeltaIntSmCr = CroppedData[1]
MinPixel = CroppedData[2]
NormSpecSmCr = CroppedData[3]
######################################################
print("Cropped")

################## Normalize data ##################
temp = np.zeros_like(DeltaIntSmCr)
temp = np.transpose(temp)
temp2 = np.transpose(DeltaIntSmCr)

for i in range(len(temp)):
	temp[i] = temp2[i] / NormSpecSmCr

DeltaIntNorm = np.transpose(temp)
######################################################
print("Normalized")

#Determining filename  
scan_number = raw_input('Scan #: ')
filename = './scan' + scan_number + 'lineouts.dat'

################## Save data to file ##################
lineout1 = DeltaIntNorm[pixel1-MinPixel]
lineout2 = DeltaIntNorm[pixel2-MinPixel]
lineout3 = DeltaIntNorm[pixel3-MinPixel]
lineout4 = DeltaIntNorm[pixel4-MinPixel]
len = np.shape(lineout1)
lineouts = np.zeros((len[0],5))
lineouts[:,1] = lineout1
lineouts[:,2] = lineout2
lineouts[:,3] = lineout3
lineouts[:,4] = lineout4
lineouts[:,0] = positions[0]
np.savetxt(filename,lineouts)
######################################################
