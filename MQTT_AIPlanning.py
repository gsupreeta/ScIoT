import requests
import sys
import serial
import time
import paho.mqtt.client as mqtt
import random

global user_temp
global sensor_temp
global sensor_humidity
global sensor_temp1
global sensor_humidity1


# Function for taking input from UI
def user_input():
    user_temp = round(random.uniform(20.0, 40.0),2)
    return user_temp

# Function to read data from BLE sensor and publish the same
def temp_sensor_input():
    arduinoData = serial.Serial('COM7', 9600)
    received_data = (arduinoData.readline())
    received_data = str(received_data, 'utf-8')
    if ((received_data.find("Gesture"))>=0):
        client = mqtt.Client("P1")  # create new instance
        client.connect("broker.hivemq.com")  # connect to broker
        client.subscribe("HDU/Building1/Monitoring/Gesture")
        client.connect("broker.hivemq.com")
        client.publish("HDU/Building1/Monitoring/Gesture", "Gesture detected")
        print("Gesture Data published!")
        received_data = (arduinoData.readline())
        received_data = str(received_data, 'utf-8')
    if (received_data.find("Temperature")>=0):
        sensor_temp= received_data.split(":")
        sensor_temp1=sensor_temp[1]
        client = mqtt.Client("P1")  # create new instance
        client.connect("broker.hivemq.com")  # connect to broker
        client.subscribe("HDU/Building1/Monitoring/Temperature")
        client.connect("broker.hivemq.com")
        print(sensor_temp1)
        client.publish("HDU/Building1/Monitoring/Temperature", sensor_temp1)
        print("Temperature Data published!")

        sensor_humidity = (arduinoData.readline())
        received_data1 = str(sensor_humidity, 'utf-8')
        if ((received_data1.find("Humidity"))>=0):
            sensor_humidity = received_data1.split(":")
            sensor_humidity1 = sensor_humidity[1]
            client = mqtt.Client("P1")  # create new instance
            client.connect("broker.hivemq.com")  # connect to broker
            client.subscribe("HDU/Building1/Monitoring/Temperature")
            client.connect("broker.hivemq.com")
            print(sensor_humidity1)
            client.publish("HDU/Building1/Monitoring/Temperature", sensor_humidity1)
            print("Humidity Data published!")
    return sensor_temp1,sensor_humidity1

#def human_sensor_input():
 #   arduinoData1 = serial.Serial('COM', 9600)
  #  human_detect = arduinoData1.readline()
   # human_detect = str(human_detect, 'utf-8')


# Function to provide dynamic data to online editor of pddl
def temp_planning():
    sensed_temp, sensed_humidity= temp_sensor_input()
    print(sensed_temp, sensed_humidity)

    #human_presence = human_sensor_input()
    #print(human_presence)

    set_temp = user_input()
    print(set_temp)

    if (float(sensed_temp or sensed_humidity) == set_temp):
        with open("problem-1.pddl") as p:
            with open("problem.pddl", "w") as p1:
                for line in p:
                    p1.write(str(line))
        data = {'domain': open(sys.argv[1], 'r').read(),
                'problem': open(sys.argv[2], 'r').read()}
        return data
    elif (set_temp > float(sensed_temp or sensed_humidity) ):#or human_presence):
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
    var1 = response['result']['plan'][0]['name']
    with open(sys.argv[3], 'w') as f:
        f.write(str(var1))

#Function to publish data to MQTT
counter=0
while(1):
    AIplanning()
    with open("plan.txt", "r") as f:
        zero_line = f.readline()
        if ('user-input' in zero_line):
            a="500"
        if ('same' in zero_line):
            a="0"
        if ('sensor-input' in zero_line):
            a="1023"
    client = mqtt.Client("P1")  # create new instance
    print("connecting to broker")
    client.connect("broker.hivemq.com")  # connect to broker
    client.subscribe("HDU/Building1/Monitoring/PDDL")
    client.connect("broker.hivemq.com")
    client.publish("HDU/Building1/Monitoring/PDDL", a)
    print("Data published!")
    if(counter >1000):
        break

counter=counter+1
print(counter)
time.sleep(5)
