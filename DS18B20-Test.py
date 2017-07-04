import os
import glob
import time
import httplib, urllib
import time
import math
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


sensor1_dir = '/sys/bus/w1/devices/28-011620f120ee/w1_slave'
sensor2_dir = '/sys/bus/w1/devices/28-02161de1f2ee/w1_slave'
 

 
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


while True:

	sensor1_temperature = read_temp(sensor1_dir)
	sensor2_temperature = read_temp(sensor2_dir)

	plot_to_thingspeak(sensor1_temperature, sensor2_temperature)

	print("Sensor 1: "+ str(sensor1_temperature) +"C")
	print("Sensor 2: "+ str(sensor2_temperature) +"C")	
	time.sleep(300)
