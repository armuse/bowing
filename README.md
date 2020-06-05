Call bowing.py with the full name of the output data file (.csv included)

This code is meant to be used for the ATLAS Inner Tracker (ITk) detector upgrade, performing a quality control check on the bow of the sensors that will be put into the experiment. 

The code runs over results from the Optical 3D profilometer at SFU and calculates a bow measurement of the sensor, returning acceptable if the bow is less than +/- 150 um. It outputs the data used to make this decision to the format necessary to upload to the ITk Production Database. 
