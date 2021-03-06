import sys 
from datetime import datetime
import pandas as pd
import numpy as np

#call this with the input data file as a command line arguement

def getData(): 

	# read in data points
	
	filename = sys.argv[1]
	if filename.find('.csv') < 0: sys.exit("File "+filename+" does not exist.")
	data = pd.read_csv(filename)
	return data
	
def calculateBow(data):

	#clean up data, remove NaN etc, add z' column
	data = data.set_axis(["x(mm)", "y(mm)", "z(um)"],axis=1)
	data['z\'(um)'] = data[['z(um)']]

	#move to next row in y at each break, save each y bunch as a new dataframe
	breaks = data.index[data['x(mm)'] == 0].tolist()
	splitdata = np.split(data,breaks)
	df30 = pd.DataFrame(columns = ["x(mm)", "y(mm)", "z(um)"])
	for i in range(1,len(breaks)):
		splitdata[i] = splitdata[i].dropna()
		splitdata[i] = splitdata[i].reset_index(drop=True)
		ind = int(len(splitdata[i])/30)
		if ind == 0: continue #first value may be 0
		print(splitdata[i][::ind])
		df30 = df30.append(splitdata[i][::ind])
	
	print(df30)

	return df30

def isAcceptable(df30,wafer):

	#is the Bow (max-min) within specifications?

	maxBow = 150
	bow = df30['z\'(um)'].max() - df30['z\'(um)'].min()

	if bow < maxBow:
		isOK = True
		print('The bowing for sensor ' + wafer + " is acceptable")
	else:
		isOK = False
		print('The bowing for sensor ' + wafer + " is not acceptable")
	return isOK

def header():

	#gather information for heading from operator

	sensors = {'R0',"R1","R2","R3","R4","R5"}
	sensor_type = input('Enter sensor type: ')
	if sensor_type not in sensors: sys.exit('Not a sensor type.')

	batch = input('Enter batch number: ')
	wafer = input('Enter Wafer #: ')
	today = datetime.today().strftime('%d %B %Y')
	timestamp = datetime.now().strftime('%H:%M:%S')
	user = input('Enter user: ')

	temp = input('Enter temperature: ')
	if (float(temp) < 16.5) or (float(temp) > 21.5): sys.exit('Unallowable temperature.')

	humidity = input('Enter humidity: ')
	if float(humidity) > 20.: sys.exit('Unallowable humidity.')

	#write heading using user inputs

	outfile = batch+'_'+wafer+"_metrology.dat"
	out = open(outfile,'w')

	out.write('Type: '+sensor_type+'\n')
	out.write('Batch: '+batch+'\n')
	out.write('Wafer: '+wafer+'\n')
	out.write('Date: '+today+'\n')
	out.write('Time: '+timestamp+'\n')
	out.write('Institute: SFU'+'\n')
	out.write('User: '+user+'\n')
	out.write('TestType: SENSOR_METROLOGY'+'\n')
	out.write('Temperature: '+temp+'\n')
	out.write('Humidity: '+humidity+'\n')
	out.write('\n')

	out.close()

	return outfile

def output(df30,outfile):

	#write out data used to make bow decision

	df30.to_csv(outfile,mode='a',index=False)

def main(): 
	data = getData()
	df30 = calculateBow(data)
	outfile = header()
	wafer = outfile.split('_')[1]
	isAcceptable(df30,wafer)
	output(df30,outfile)

if __name__ == "__main__":
	main()
