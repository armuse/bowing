import sys
from datetime import datetime
import pandas as pd
import numpy as np
import scipy as sp

#call this with the input data file as a command line arguement

def getData():

	filename = sys.argv[1]
	if filename.find('.ASC') < 0: sys.exit("File "+filename+" does not exist.")
	df = pd.read_csv(filename,encoding = "utf-8",sep='\t')
	return df

def cleanData(df):
	df = df[df['Z'].notna()]
	df = df[df['Z']!='Bad']
	return df

def make13x13(data):
	#trim off edges of sensor (might need to increase the trim a bit for different sensor types)
	#find max X and Y
	maxX = data['X'].max()
	maxY = data['Y'].max()
	X_low = 0.1*maxX
	X_high = 0.9*maxX
	Y_low = 0.1*maxY
	Y_high = 0.9*maxY

	grid13x13_xy = []
	#based on low and high X/Y, find 13x13 x,y coordinates for grid
	for i in range(1,14):
		X_range = X_high-X_low
		xpoint = round((i/21)*X_range,3)
		for i in range(1,14):
			Y_range = Y_high-Y_low
			ypoint = round((i/13)*Y_range,3)
			grid13x13_xy.append([xpoint,ypoint])

	grid13x13Z = []
	#find the nearest x,y the profilometer recorded to the x,y coordinates found above
	try:
		for coordinate in grid13x13_xy:
			min_index = data['X'].sub(coordinate[0]).abs().idxmin()
			max_index = data['X'].sub(coordinate[0]).abs().idxmax()
			data_tmp = data[min_index:max_index]
			y_index = data_tmp['Y'].sub(coordinate[1]).abs().idxmin()
			grid13x13Z.append([data['X'][min_index],data['Y'][y_index],data['Z'][y_index]])
	except ValueError:
		pass

	return grid13x13Z

def removeTilt(df):
	#df = pd.DataFrame(grid,columns = ['X','Y','Z'])
	#df['Z'] = round(df['Z'].astype(np.float)/1000,3)

	#fit to a plane
	Y = df['Z']
	X = df[['X','Y']]
	X = X.to_numpy()
	X = X.astype(np.float)
	Y = Y.astype(np.float)
	a = np.linalg.solve(np.dot(X.T,X),np.dot(X.T,Y))
	predictedY = np.dot(X,a)
	predictedY = predictedY
	Zprime = predictedY.tolist()
	df['Znew'] = Zprime
	df["Z'"] = (df['Znew'] - df['Z'])
	df.drop(columns=['Znew'])

	return df

def calculateBow(grid,outfile):
	df = pd.DataFrame(grid,columns = ['X','Y','Z'])
	df['Z'] = round(df['Z'].astype(np.float)/1000,3) #Z is in nm instead of um unlike X, Y
	#df['X'] = round(df['X'].astype(np.float),3)
	#df['Y'] = round(df['Y'].astype(np.float),3)
	maxZ = df['Z'].astype(np.float).max()
	minZ = df['Z'].astype(np.float).min()
	bow = maxZ - minZ

	if len(sys.argv) >= 3: #if the data does not already have the tilt removed,
		df = removeTilt(df)
		df.drop(['Znew'], axis=1)
		df["Z'"] = round(df["Z'"],3)
		maxZdiff = df["Z'"].max()
		minZdiff = df["Z'"].min()
		bow = maxZdiff - minZdiff
	else:
		df["Z'"] = df['Z']
	df['X'] = round(df['X'],3)
	df['Y'] = round(df['Y'],3)
	cols = ["X","Y","Z","Z'"]
	df.to_csv(outfile,columns=cols,mode='a',index=False)
	#return bow,df
	if bow < 150:
		print('Acceptable bowing of ',bow)
	else: print('Bowing too large: ',bow)

def header():
	#ask header questions
	sensors = {'R0',"R1","R2","R3","R4","R5"}
	sensor_type = input('Enter sensor type: ')
	if sensor_type not in sensors: sys.exit('Not a sensor type.')

	batch = input('Enter batch number: ')
	wafer = input('Enter Wafer #: ')
	today = datetime.today().strftime('%d %B %Y')
	time = datetime.now().strftime('%H:%M:%S')

	user = input('Enter user: ')
	users = ['alyssa','graham','luise','scott','xavier']
	if (user.lower() not in users): sys.exit('Unknown user')

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
	out.write('Time: '+time+'\n')
	out.write('Institute: SFU'+'\n')
	out.write('User: '+user+'\n')
	out.write('TestType: SENSOR_METROLOGY'+'\n')
	out.write('Temperature: '+temp+'\n')
	out.write('Humidity: '+humidity+'\n')
	out.write('\n')

	out.close()

	return outfile

def main():

	outfile = header()
	data = getData()
	data = cleanData(data)
	grid = make13x13(data)
	calculateBow(grid,outfile)

if __name__ == "__main__":
	main()
