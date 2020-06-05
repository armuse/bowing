Call bowing.py with the full name of the output data file (including .csv)

This code is meant to be used for the ATLAS Inner Tracker (ITk) detector upgrade, performing a quality control check on the bow of the sensors that will be put into the experiment. 

The code runs over results from the Optical 3D profilometer at SFU and calculates the sensor bow, to check if it is less than +/- 150 um. It then outputs the data used to make this decision to the necessary format to upload to the ITk Production Database. 

Input files have thousands of rows and 3 columns (x,y,z). This code returns a file with a specific header and a selection of evenly spaced data points used to find the bow. The z' is necessary to remove tilt and is calculated with our profilometer and therefore a copy of the z column in our case. 
