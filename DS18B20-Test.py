import os
import glob
import time
import httplib, urllib
import time
import math
import datetime
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

from os import listdir
from os.path import isfile, join, isdir


DevicesPath = '/sys/bus/w1/devices/'
DevicesDirs = [f for f in listdir(DevicesPath) if isdir(join(DevicesPath, f))]

sensorCount = 0
sensorDirName = []
sensorDirPath = []

for dir in DevicesDirs:
    if dir[0:3] == '28-':
        sensorCount = sensorCount+1
        sensorDirName.append(dir)


for dir in sensorDirName:
    sensorDirPath.append(DevicesPath + dir)

print("Number of DS18b20 sensors found: {}".format(sensorCount))

for num in range(sensorCount):
    print(sensorDirPath[num-1])


 

sensor1_dir = '/sys/bus/w1/devices/28-011620f120ee/w1_slave'
sensor2_dir = '/sys/bus/w1/devices/28-02161de1f2ee/w1_slave'
 
PollingPeriod = 300 #Poll every 300 seconds
 
def read_temp_raw(sensor_dir):
    f = open(sensor_dir, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp(sensor_dir):
    lines = read_temp_raw(sensor_dir)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(sensor_dir)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
	
def plot_to_thingspeak(data_to_plot1,data_to_plot2):

	try:
		params = urllib.urlencode({'field1': float(data_to_plot1), 'field2': float(data_to_plot2), 'key':'89HYGVJ42Q4I9N2D'})  
        	# use your API key generated in the thingspeak channels for the value of 'key'	
        	# temp is the data you will be sending to the thingspeak channel for plotting the graph. You can add more than one channel and plot more graphs
		headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
		conn = httplib.HTTPConnection("api.thingspeak.com:80")                
	except:
		print "Error"
	try:
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
	
		print response.status, response.reason
		data = response.read()
		conn.close()
	except:
		print "connection failed"


print ("DS18b20 Temperature Sensor Logger")
print ("Polling every {} seconds".format(PollingPeriod))

while True:

	sensor1_temperature = read_temp(sensor1_dir)
	sensor2_temperature = read_temp(sensor2_dir)
	
	
	print (time.strftime("%Y-%m-%d %H:%M"))
	plot_to_thingspeak(sensor1_temperature, sensor2_temperature)

	print("Sensor 1: "+ str(sensor1_temperature) +"C")
	print("Sensor 2: "+ str(sensor2_temperature) +"C")	
	time.sleep(PollingPeriod)
