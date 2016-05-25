# -------------------------------------------------------------------
# Authors: R. Camuccio, T. Lehman-Borer, and A. Lytle
# Date: 6.9.2015
# Version 2.0 (5.23.2016)
#
# This program is designed for counterpropagating scan data analysis
# -------------------------------------------------------------------

""" Program initialization """

# Import modules
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Clear terminal
os.system("cls" if os.name == "nt" else "clear")

# Program header
print("---------------------------------------------------")
print(" Analysis Program for Counterpropagating Scan Data")
print(" Authors: R. Camuccio, T. Lehman-Borer, and A. Lytle")
print(" Version: 2.0")
print("---------------------------------------------------")
print


#### SLICE FUNCTION####
def slice_routine(wavelength_array, intensity_array, min_wavelength, max_wavelength):
	""" This function accepts a wavelength and intensity array and returns a sliced wavelength and intensity array """

	# Define coefficients
	A0 = 348.4316445
	A1 = 0.069763835
	A2 = -2.98682E-6
	B0 = A0-((A1**2)/(4*A2))
	B1 = (A1)/(2*A2)

	# Calculation of minimum/maximum pixel number
	P_min = -(math.sqrt(((min_wavelength-B0)/A2)))-B1
	P_max = -(math.sqrt(((max_wavelength-B0)/A2)))-B1

	# Round and convert pixel numbers to integers
	P_min = int(math.floor(P_min))
	P_max = int(math.floor(P_max))

	# Transpose wavelength array for slicing
	wavelength_array = np.transpose(wavelength_array)

	# Slice arrays
	intensity_array = intensity_array[P_min:P_max]
	wavelength_array = wavelength_array[P_min:P_max]

	# Transpose wavelength array back to original transposition
	wavelength_array = np.transpose(wavelength_array)

	return wavelength_array, intensity_array, P_min
#######################
 
#### SMOOTH FUNCTION ####
def smooth_routine(position_array, wavelength_array, intensity_array, smooth_factor):
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
########################
 
#### SPECTRAL SMOOTH FUNCTION ####
def specsmooth_routine(wavelength_array, intensity_array, smooth_factor):
	""" This function accepts a wavelength and intensity array and returns a smoothed intensity array """

	# Create temporary list for value handling
	new_list = []

	# Calculate edge pixels to avoid smoothing
	edge_pixels = (smooth_factor - 1) // 2

	# Initialize sum and average
	current_sum = 0
	average = 0

	print("Plotting...")

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

	# Return smoothed intensity array
	return intensity_array
#################################

###############################################################################
""" Normalization """


##### NORMALIZATION INPUT ROUTINE ######################
print("This function will normalize specified a-file.")
print

user_input1 = raw_input("A file: ")
array_a = np.loadtxt(user_input1)

user_input2 = raw_input("B file: ")
wocp_array = np.loadtxt(user_input2)
wocp_array = np.transpose(wocp_array)
wocp_array = wocp_array[0] #This is the spectrum we're normalizing to.

m = array_a.shape[0]
n = array_a.shape[1]

scan_length = m - 2

intensity_array = array_a[0:scan_length]
wavelength_array = array_a[scan_length:scan_length+1]
position_array = array_a[scan_length+1:scan_length+2]

position_array = np.transpose(position_array)
position_array = position_array[0:scan_length]
position_array = np.transpose(position_array)

intensity_array = np.transpose(intensity_array)
########################################################


##### PARAMETER ROUTINE #######################
lmda = int(raw_input("Spectrum wavelength: "))

A0 = 348.4316445
A1 = 0.069763835
A2 = -2.98682E-6
B0 = A0-((A1**2)/(4*A2))
B1 = (A1)/(2*A2)

pixel = -(math.sqrt(((lmda-B0)/A2)))-B1
pixel = int(math.floor(pixel))
###############################################


#### PARAMETERS (MAX MIN SMOOTH) ####
# I'm doing this here, outside any function, so that it is only done once.

# Specify minimum wavelength
min_wavelength = input("Minimum wavelength: ")
while min_wavelength < 348.9 or min_wavelength > 561.7:
	min_wavelength = input("ERROR! Minimum wavelength must be above 348.9 nm and below 561.7 nm: ")

# Specify maximum wavelength
max_wavelength = input("Maximum wavelength: ")
while max_wavelength < 348.9 or max_wavelength > 561.7:
	max_wavelength = input("ERROR! Maximum wavelength must be above 348.9 nm and below 561.7 nm: ")

# Check that minimum and maximum are correct with respect to each other
while max_wavelength <= min_wavelength:
	max_wavelength = input("ERROR! Maximum wavelength must be greater than minimum wavelength. Select another: ")
 
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
##################################
 

##### SMOOTH ROUTINE ################################
temp1 = smooth_routine(position_array, wavelength_array, intensity_array, smooth_factor)
#####################################################


##### SLICE ROUTINE #######################
slice_return = slice_routine(wavelength_array, temp1, min_wavelength, max_wavelength)
temp2 = slice_return[0]
temp1 = slice_return[1]

P_min = slice_return[2]
###########################################


##### PLOT ROUTINE #########################################################################
gs = gridspec.GridSpec(2, 2, width_ratios=[1,1], height_ratios=[1,1])	

a = plt.subplot(gs[0])
b = plt.subplot(gs[1])
c = plt.subplot(gs[2])
d = plt.subplot(gs[3])

plt.suptitle("Raw/Normalized Plot for " + str(user_input1), fontsize=14, fontweight='bold')
cs1 = a.contourf(position_array[0], temp2[0], temp1, 50, cmap=plt.cm.winter)
a.set_title("Raw Plot")
a.set_xlabel("Relative position (um)")
a.set_ylabel("Wavelength (nm)")
a.plot((-0.5, 0.5), (lmda, lmda), 'r--')
plt.colorbar(cs1, ax=a)
############################################################################################

##### SPECTRAL SMOOTHING ROUTINE #######################
wocp_array = specsmooth_routine(wocp_array, wocp_array, smooth_factor)
########################################################


##### NOISE SUBTRACTION ROUTINE #########################
noise = wocp_array[len(wocp_array)-1000:len(wocp_array)]
mean = np.mean(noise)

wocp_array -= mean

intensity_array = np.transpose(intensity_array)

for i in range(len(intensity_array)):
	intensity_array[i] = intensity_array[i] / wocp_array

intensity_array = np.transpose(intensity_array)
#########################################################


##### SMOOTH ROUTINE ###############################################################
intensity_array = smooth_routine(position_array, wavelength_array, intensity_array, smooth_factor)
####################################################################################


##### SLICE ROUTINE #############################################
slice_return = slice_routine(wavelength_array, intensity_array, min_wavelength, max_wavelength)
wavelength_array = slice_return[0]
intensity_array = slice_return[1]
#################################################################


##### SOI PLOT ROUTINE ###################################
d.set_title("Normalized Spectrum at " + str(lmda) + " nm")
d.set_xlabel("Relative position (um)")
d.set_ylabel("Intensity (arb. units)")  
d.plot(position_array[0], temp1[pixel-P_min])
##########################################################


##### PLOT ROUTINE ############################################################
cs2 = c.contourf(position_array[0], wavelength_array[0], intensity_array, 50, cmap=plt.cm.winter)
c.set_title("Normalized Plot")
c.set_xlabel("Relative position (um)")
c.set_ylabel("Wavelength (nm)")
c.plot((-0.5, 0.5), (lmda, lmda), 'r--') #should I make these values dependent on something instead of just keeping it set constant?
plt.colorbar(cs2, ax=c)
###############################################################################
	
##### WOCP PLOT ROUTINE ###############
#b.set_title("WOCP Spectrum")
#b.set_xlabel("Wavelength (nm)")
#b.set_ylabel("Intensity (arb. units)")

#A0 = 348.4316445
#A1 = 0.069763835
#A2 = -2.98682E-6
#B0 = A0-((A1**2)/(4*A2))
#B1 = (A1)/(2*A2)

#P_min = -(math.sqrt(((390-B0)/A2)))-B1
#P_max = -(math.sqrt(((425-B0)/A2)))-B1
#P_min = int(math.floor(P_min))
#P_max = int(math.floor(P_max))

#wocp_array = wocp_array[P_min:P_max]

#b.plot(temp2[0], wocp_array) #There's no error if I comment this out, but it doesn't display one of the graphs
#######################################


##### FINALIZING ROUTINE ########################
plt.show()
#################################################


###############################################################################
""" Program termination """

# Program termination message
print
print("Program terminated.")
print
