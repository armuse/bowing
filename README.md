Call bowing_2D.py with the full name of the output data file (sample.csv) For testing purposes, use Temperature = 20 and humidity = 10 when prompted. 

This code is meant to be used for the ATLAS Inner Tracker (ITk) detector upgrade, performing a quality control check on the bow of the sensors that will be put into the experiment. 

The code runs over results from the Optical 3D profilometer at SFU and calculates the sensor bow, to check if it is less than +/- 150 um. It then outputs the data used to make this decision to the necessary format to upload to the ITk Production Database. 

Input files have thousands of rows and 3 columns with data (x,y,z). This code returns a file with a specific header and a 30 evenly spaced data points used to find the bow per y value. The z' is an artifact from other collaborators and our input data has been pre-processed such that z = z'. 
