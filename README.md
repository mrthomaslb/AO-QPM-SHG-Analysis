# AO-QPM-SHG-Analysis

##README
All .py files use Python 3. The software requires data input from a LabVIEW program, not included.

Authors: R. Camuccio, T. Lehman-Borer, and A. Lytle
##ANALYSIS.PY
###How to Use
The code will prompt you for an A file and a B file. Select those from the menu that pops up. Make sure that you select matching A and B files. If you want to change the wavelength(s) of lineout that the program displays, change the list `lmdas` near the top of the code. Likewise, if you want to change the smoothing factor or the minimum or maximum wavelength of the spectra displayed, change `smooth_factor`, `min_wavelength`, or `max_wavelength`, respectively.
###Potential Improvements
- increase Smooth function efficiency
- make display font match the Greek mu

##SAVE LINEOUT.PY
###How to Use
This program will also ask for an A file and a B file. As with `Analysis.py`, it will smooth, crop, and normalize the data. However, instead of displaying graphs, it will save a .DAT file, which is just an array of the position values and the lineout values for the selected wavelength. The top row of the file has the wavelength of each respective lineout.

##STACKED PLOT.PY
###How to Use
You are prompted to open a set of lineouts. These must be selected together, using the `SHIFT` key. It displays a stacked graph of several lineouts at different beam electric field ratios. Make sure that the variables in the top section of the code are correct for the data you are using.

##WATERFALL GRAPH.PY
###How to Use
You are prompted to open a set of lineouts. These must be selected together, using the `SHIFT` key. Upon doing so, it shows a 3d graph of positions, wavelengths, and electric field ratios. Make sure that the variables in the top section of the code are correct for the data you are using.
