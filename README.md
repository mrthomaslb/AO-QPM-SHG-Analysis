# AO-QPM-SHG-Analysis

##README

This program requires data input from a LabVIEW program, not included. It uses Python 3.

###AUTHORS

R. Camuccio, T. Lehman-Borer, and A. Lytle

##ANALYSIS.PY

###How to Use

The code will prompt you for an A file and a B file. Select those from the menu that pops up. Make sure that you select matching A and B files. If you want to change the wavelength(s) of lineout that the program displays, change the list `lmdas` near the top of the code. Likewise, if you want to change the smoothing factor or the minimum or maximum wavelength of the spectra displayed, change `smooth_factor`, `min_wavelength`, or `max_wavelength`, respectively.

###Potential Improvements

- increase Smooth function efficiency
- make display font match the Greek mu

##SAVE LINEOUT.PY

###How to Use

This program will also ask for an A file and a B file. As with `Analysis.py`, it will smooth, crop, and normalize the data. However, instead of displaying graphs, it will save a .DAT file, which is just an array(?) of the position values and the lineout values for the selected wavelength.

###Potential Improvements

- make more user-friendly when selecting wavelengths to save
- check for unnecessary code and remove

##WATERFALL GRAPH.PY

###How to Use

Currently, this only works with the current version of `Save Lineout.py`. You are prompted to open a set of lineouts. Upon doing so, it shows a 3d graph of positions, wavelengths, and power ratios. The power ratios are in the program itself, so to look at a new set of data, this needs to be changed.

###Potential Improvements

* make more adaptable for different saved files
* add color variation for visual clarity
