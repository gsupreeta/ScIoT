import requests
import sys
import serial
import time
import paho.mqtt.client as mqtt
#import BLUBackground_GUI

global user_temp
global sensor_temp
global sensor_humidity


# Function for taking input from UI
def user_input():
    #user_temp= BLUBackground_GUI.Take_input()
    user_temp =50
    #print(user_temp)
    #user_temp = val
    #return user_temp
    #user_temp = user_val
    #print(user_temp)
    #temp_planning(user_temp)
    return user_temp

# Function to read data from Temperature sensor
def sensor_input():
    arduinoData = serial.Serial('COM7', 9600)
    sensor_temp = arduinoData.readline()
    sensor_humidity = arduinoData.readline()
    sensor_temp = str(sensor_temp, 'utf-8')
    sensor_humidity = str(sensor_humidity, 'utf-8')
    return sensor_temp, sensor_humidity

# Function to provide dynamic data to online editor of pddl
def temp_planning():
    sensed_temp, sensed_humidity = sensor_input()
    print(sensed_temp, sensed_humidity)

    set_temp = user_input()
    print(set_temp)

    if (float(sensed_temp) == set_temp):
        with open("problem-1.pddl") as p:
            with open("problem.pddl", "w") as p1:
                for line in p:
                    p1.write(str(line))
        data = {'domain': open(sys.argv[1], 'r').read(),
                'problem': open(sys.argv[2], 'r').read()}
        return data
    elif (set_temp > float(sensed_temp)):
        with open("problem-2.pddl") as p:
            with open("problem.pddl", "w") as p2:
                for line in p:
                    p2.write(str(line))
        data = {'domain': open(sys.argv[1], 'r').read(),
                'problem': open(sys.argv[2], 'r').read()}
        return data
    else:
        with open("problem-3.pddl") as p:
            with open("problem.pddl", "w") as p3:
                for line in p:
                    p3.write(str(line))
        data = {'domain': open(sys.argv[1], 'r').read(),
                'problem': open(sys.argv[2], 'r').read()}
        return data


# Function to execute AI planning and get plan.txt file
def AIplanning():
    data_input = temp_planning()
    response = requests.post('http://solver.planning.domains/solve', json=data_input).json()
    #print(response)
    var1 = response['result']['plan'][0]['name']
    #print(var1)
    with open(sys.argv[3], 'w') as f:
        f.write(str(var1))

#Function to publish data to MQTT
counter=0
while(1):
    AIplanning()
    with open("plan.txt", "r") as f:
        zero_line = f.readline()
        if ('user-input' in zero_line):
            a="1"
        if ('same' in zero_line):
            a="0"
        if ('sensor-input' in zero_line):
            a="2"
    client = mqtt.Client("P1")  # create new instance
    print("connecting to broker")
    client.connect("broker.hivemq.com")  # connect to broker
    client.subscribe("HDU/Building1/Monitoring/Temperature")
    client.connect("broker.hivemq.com")
    client.publish("HDU/Building1/Monitoring/Temperature", a)
    print("Data published!")
    if(counter >1000):
        break

counter=counter+1
print(counter)
time.sleep(5)
