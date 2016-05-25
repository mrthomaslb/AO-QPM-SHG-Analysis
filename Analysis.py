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
#import matplotlib.gridspec as gridspec

os.system("cls" if os.name == "nt" else "clear")

# Program header
print("---------------------------------------------------")
print(" Analysis Program for Counterpropagating Scan Data")
print(" Authors: R. Camuccio, T. Lehman-Borer, and A. Lytle")
print(" Version: 2.0")
print("---------------------------------------------------")
print

#### FUNCTIONS ####
def SmoothData(position_array, wavelength_array, intensity_array):
	""" This function accepts a wavelength and intensity array and returns a smoothed intensity array """

	# Create temporary list for value handling
	new_list = []

	# Prompt user input of smoothing factor
	print
	print("Length of input array = " + str(len(wavelength_array[0])))
	smooth_factor = input("Smoothing factor: ")

	# Check if smoothing factor is within reasonable bounds
	while smooth_factor > len(wavelength_array[0]):
		smooth_factor = input("Choose smoothing factor less than length of array: ")

	# Check if smoothing factor is integer type
	while smooth_factor != int(smooth_factor):
		smooth_factor = input("Choose smoothing factor that is integer type: ")

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

def SmoothSpectrum(intensity_array):
	""" This function accepts a wavelength and intensity array and returns a smoothed intensity array """

	# Create temporary list for value handling
	new_list = []

	smooth_factor = 11

	# Calculate edge pixels to avoid smoothing
	edge_pixels = (smooth_factor - 1) // 2

	# Initialize sum and average
	current_sum = 0
	average = 0

	# Place front edge values into list
	for i in range(edge_pixels):
		new_list.append(intensity_array[i])

	# Place values of interest into smoothing algorithm
	for i in range(edge_pixels, len(intensity_array)-edge_pixels):

		# Slice the array around the pixels of interest
		slice_array = intensity_array[i-edge_pixels:i+edge_pixels+1]

		# Average the sliced array into one value
		for j in range(0, len(slice_array)):
			current_sum = current_sum + slice_array[j]
			average = current_sum / smooth_factor

		# Place averaged value into output list
		new_list.append(average)

		# Reset sum and average
		current_sum = 0
		average = 0

	# Place rear edge values into list
	for i in range(edge_pixels):
		new_list.append(intensity_array[len(intensity_array)-edge_pixels+i])

	# Convert list into array
	intensity_array = np.asarray(new_list)
 
 	# Subtract dark count offset
	offset = intensity_array[len(intensity_array)-1000:len(intensity_array)]
	offsetmean = np.mean(offset)
	intensity_array -= offsetmean

	# Return smoothed intensity array
	return intensity_array
########################

################## Read in data ##################
user_input1 = raw_input("A file: ")
user_input2 = raw_input("B file: ")

raw_data = np.loadtxt(user_input1)

wocp = np.loadtxt(user_input2)
wocp = np.transpose(wocp)
NormSpec = wocp[0] #This is the spectrum we're normalizing to.

m = raw_data.shape[0]
n = raw_data.shape[1]

scan_length = m - 2

DeltaInt = raw_data[0:scan_length]
wavelengths = raw_data[scan_length:scan_length+1]
positions = raw_data[scan_length+1:scan_length+2]

positions = np.transpose(positions)
positions = positions[0:scan_length]
pos=positions[scan_length-1]
posscale=pos[0]
positions = np.transpose(positions)

DeltaInt = np.transpose(DeltaInt)

lmda = int(raw_input("Select wavelength for relative position lineout: "))

pixel=wavel_to_pixel(lmda)
######################################################

################## Smooth data ##################
DeltaIntSm = SmoothData(positions, wavelengths, DeltaInt)
######################################################
print("Smoothed")

################## Smooth normalization spectrum ##################
NormSpecSm = SmoothSpectrum(NormSpec)
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
DeltaIntSmCrNorm = np.transpose(DeltaIntSmCr)

for i in range(len(DeltaIntSmCrNorm)):
	DeltaIntSmCrNorm[i] = DeltaIntSmCrNorm[i] / NormSpecSmCr

DeltaIntNorm = np.transpose(DeltaIntSmCrNorm)
######################################################
print("Normalized")

#fig1 = plt.figure()
#ax1 = fig1.add_subplot(111)
#im1 = ax1.imshow(DeltaIntSmCr,vmin=DeltaIntSmCr.min(),vmax=DeltaIntSmCr.max())
#plt.show()
################## Plot data ##################
plt.subplot(2, 2, 1)
plt.contourf(positions[0], wavelengthsCr[0], DeltaIntSmCr, 50, cmap=plt.cm.winter)
plt.xlabel("Relative position (um)")
plt.ylabel("Wavelength (nm)")
plt.plot((-posscale, posscale), (lmda, lmda), 'r--')

plt.subplot(2, 2, 2)
plt.contourf(positions[0], wavelengthsCr[0], DeltaIntNorm, 50, cmap=plt.cm.winter)
plt.xlabel("Relative position (um)")
plt.ylabel("Intensity (arb. units)")

plt.subplot(2, 2, 3)
plt.plot(positions[0], DeltaIntNorm[pixel-MinPixel])
plt.xlabel("Relative position (um)")
plt.ylabel("Intensity (arb. units)")

plt.subplot(2, 2, 4)
plt.plot(wavelengthsCr[0], NormSpecSmCr)
plt.xlabel("Relative position (um)")
plt.ylabel("Intensity (arb. units)")

plt.show()
######################################################


################## Plot data ##################
#gs = gridspec.GridSpec(2, 2, width_ratios=[1,1], height_ratios=[1,1])	

#a = plt.subplot(gs[0])
#b = plt.subplot(gs[1])
#c = plt.subplot(gs[2])
#d = plt.subplot(gs[3])

#plt.suptitle("Raw/Normalized Plot for " + str(user_input1), fontsize=14, fontweight='bold')
#cs1 = a.contourf(positions[0], wavelengthsCr[0], DeltaIntSmCr, 50, cmap=plt.cm.winter)
#a.set_title("Raw Plot")
#a.set_xlabel("Relative position (um)")
#a.set_ylabel("Wavelength (nm)")
#a.plot((-posscale, posscale), (lmda, lmda), 'r--')
#plt.colorbar(cs1, ax=a)

#b.set_title("Normalization Spectrum")
#b.set_xlabel("Wavelength (nm)")
#b.set_ylabel("Intensity (arb. units)")
#b.plot(wavelengthsCr, NormSpecSmCr[0])

#cs2 = c.contourf(positions[0], wavelengthsCr[0], DeltaIntNorm, 50, cmap=plt.cm.winter)
#c.set_title("Normalized Plot")
#c.set_xlabel("Relative position (um)")
#c.set_ylabel("Wavelength (nm)")
#c.plot((-posscale, posscale), (lmda, lmda), 'r--')
#plt.colorbar(cs2, ax=c)

#d.set_title("Normalized Spectrum at " + str(lmda) + " nm")
#d.set_xlabel("Relative position (um)")
#d.set_ylabel("Intensity (arb. units)")
#d.plot(positions[0], DeltaIntNorm[pixel-MinPixel])

#plt.show()
######################################################
