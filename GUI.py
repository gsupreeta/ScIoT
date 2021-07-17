# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 02:17:09 2021

@author: dell
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 20:57:31 2021

@author: dell
"""

# Import module
from tkinter import *
import tk_tools
import time
import datetime as dt
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import json
import paho.mqtt.client as mqtt
#import serial
import requests
import matplotlib.animation as animation

#Global_Sub_Temp_Value = 0

# Create figure for plotting
fig, ax = plt.subplots()
xs = []
ys = []


# Create an MQTT client and attach our routines to it.

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CoreElectronics/test")
    client.subscribe("CoreElectronics/topic")
    client.subscribe("HDU/Building1/Monitoring/Temperature")
    client.subscribe("HDU/Building1/Monitoring/Humidity")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    #print(msg.payload)
    #print(json.loads(msg.payload.decode()))
    Sub_Temp_Value = json.loads(msg.payload.decode())
    print(msg.topic)
    # print(Sub_Temp_Value)
    # return Sub_Temp_Value
    if msg.topic == "HDU/Building1/Monitoring/Temperature":
        print("TOPIC TEMP")
        Global_Sub_Temp_Value = Sub_Temp_Value
        topic1.config(text=Sub_Temp_Value)
        ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys), interval=0)

        plt.show()
    if msg.topic == "HDU/Building1/Monitoring/Humidity":
        print("TOPIC HUMIDITY")
        Global_Sub_Temp_Value = Sub_Temp_Value
        topic2.config(text=Sub_Temp_Value)
     
        
    if msg.payload == b'1':
        print("666")
        print("Received message Emergency Indication ON ")
        led.to_green()
        # Do something
        
    if msg.payload == b'2':
        print("666")
        print("Received message Emergency Indication OFF")
        led.to_grey()
        # Do something
    

    if msg.payload == b'3':
        print("Received message OverCrowd Indication ON ")
        led1.to_green()
        # Do something else
        
    if msg.payload == b'4':
        print("Received message OverCrowd Indication OFF")
        led1.to_grey()
        # Do something else
 

def Graph():
    print("I am in GRAPH")
    ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys), interval=0)

    plt.show()
    # time = []
    # time.append([dt.datetime.now() + dt.timedelta(hours=i) for i in range(12)])
    # population_by_continent = [25,0,0,0,0,0,0,0,0,0,0]
    # population_by_continent.append(random.randint(25,27))
    # LastValue = population_by_continent[-1]
    # print(LastValue)
    
    # fig, ax = plt.subplots()
    # plt.gcf().autofmt_xdate()
    # myFmt = mdates.DateFormatter('%H:%M')
    # plt.gca().xaxis.set_major_formatter(myFmt)

    # ax.scatter(time, LastValue)
    # ax.legend(loc='upper left')
    # ax.set_title('World population')
    # ax.set_xlabel('Time')
    # ax.set_ylabel('Number of people (millions)')

    # plt.show()

def animate(i, xs:list, ys:list):
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(random.randint(20,40))
    # Limit x and y lists to 10 items
    xs = xs[-10:]
    ys = ys[-10:]
    
    # Draw x and y lists
    ax.clear()
    #ax.plot(xs, ys)
        
    #vals = [25,30]
    #colors = ["red" if ys <= 25 else "yellow"]
    
    Barcolor = 'blue'
    plt.bar(xs, ys, color = Barcolor, width = 0.4)
    # Format plot
    ax.set_ylim([0,40])
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.20)
    ax.set_title('Plot of random numbers from https://qrng.anu.edu.au')
    ax.set_xlabel('Date Time (hour:minute:second)')
    ax.set_ylabel('Random Number')
        
# data from United Nations World Population Prospects (Revision 2019)
# https://population.un.org/wpp/, license: CC BY 3.0 IGO

def Take_input():
    INPUT = entry1.get()
    print(INPUT)
    
def led_on():
    integer_val = 1
    #urllib.request.urlopen("https://api.thingspeak.com/update?api_key=8LQBHYHYYL5IY7Z5&field2="+str(integer_val));
    print("LEDON")
    #ser.write(bytes('H', 'UTF-8'))
   
def led_off():
    integer_val = 0
    #urllib.request.urlopen("https://api.thingspeak.com/update?api_key=8LQBHYHYYL5IY7Z5&field2="+str(integer_val));
    print("LEDOFF")
    #ser.write(bytes('L', 'UTF-8'))
    
#URL = 'https://api.thingspeak.com/channels/1408549/feeds.json?api_key=SU8TJU0HVDKH9LEC&results'
# get_data = requests.get(URL).json()
# feild_1 = get_data['feeds']
# print(feild_1)
# temperature_data=[]
# for x in feild_1:
#     temperature_data.append(x['field1'])
# print(temperature_data)

# Over_Crowding_Indicator=[]
# for x in feild_1:
#     Over_Crowding_Indicator.append(x['field2'])
# print(Over_Crowding_Indicator)
    
# Create object

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
print(client)

client.connect("broker.hivemq.com", 1883, 60)
root = Tk()

# Adjust size
root.geometry("1000x650")

# Add image file
bg = PhotoImage(file = "BLUBCGND_RESIZE.png")

# Create Canvas
canvas1 = Canvas( root, width = 1000,
				height = 900)

canvas1.pack(fill = "both", expand = True)

# Display image
canvas1.create_image( 0, 0, image = bg,
					anchor = "nw")

# Add Text
canvas1.create_text( 500, 20, fill="Black",font="Times 20 italic bold", text = "High Dependency Unit Monitoring")

canvas1.create_text( 190, 100, fill="Black",font="Times 20 italic bold", text = "Temperature Monitoring")
canvas1.create_text( 750, 100, fill="Black",font="Times 20 italic bold", text = "Humidity Monitoring")


# Create Buttons
button1 = Button( root, text = "Switch ON",command = led_on)
#button3 = Button( root, text = "Start")
button2 = Button( root, text = "Switch OFF",command = led_off)

# Display Buttons
button1_canvas = canvas1.create_window( 450, 150,
									anchor = "nw",
									window = button1)

button2_canvas = canvas1.create_window( 450, 200,
									anchor = "nw",
									window = button2)

# button3_canvas = canvas1.create_window( 100, 70, anchor = "nw",
# 									window = button3)

led = tk_tools.Led(canvas1, size=100)
# led.grid(row=5, column=0, sticky='news')
led_canvas = canvas1.create_window(100,500,anchor="nw",window = led)
#led.pack()
led.to_grey()

canvas1.create_text( 190, 450, fill="Black",font="Times 20 italic bold", text = "Emergency Indication")

led1 = tk_tools.Led(canvas1, size=100)
# led.grid(row=5, column=0, sticky='news')
led_canvas = canvas1.create_window(700,500,anchor="nw",window = led1)
#led.pack()
led1.to_grey()
#Last_element = Over_Crowding_Indicator[-1]

# interger_LastElement = int(Last_element)
# print(interger_LastElement)
# print(type(interger_LastElement))
# if interger_LastElement >= 1:
#       led1.to_green()
# else: 
#      led1.to_grey()
#led.to_green(on=True)
canvas1.create_text( 750, 450, fill="Black",font="Times 20 italic bold", text = "Overcrowd Warning")

canvas1.create_text( 490, 260, fill="Black",font="Times 10 italic bold", text = "Desired Temperature")

entry1 = Entry(canvas1, width =15)
entry1_canvas = canvas1.create_window( 420, 270,
									anchor = "nw",
									window = entry1)

#entry1.pack()

button3 = Button( root, text = "Set",command = Take_input)
button3_canvas = canvas1.create_window( 530, 270,
									anchor = "nw",
									window = button3)

button4 = Button( root, text = "Graph",command = Graph)
button4_canvas = canvas1.create_window( 200, 400,
									anchor = "nw",
									window = button4)

#def digitalclock():
#     text_input = time.strftime("%H:%M:%S")
#     msg = canvas1.create_text( 530, 300, fill="White",font="Times 20 italic bold", text = text_input)
#     canvas1.after(200, canvas1.delete, digitalclock)
def digitalclock():
   text_input = time.strftime("Time:%H:%M:%S")
   label.config(text=text_input)
   label.after(200, digitalclock)
   
label = Label(canvas1, font=("Courier", 10, 'bold'), bg="white", fg="black", bd =10)
DigitalCLock_Label = canvas1.create_window( 850, 15,
									anchor = "nw",
									window = label)

date = dt.datetime.now()
format_date = f"{date:%a, %b %d %Y}"
#display(format_date)
canvas1.create_text( 80, 30, fill="White",font="Times 15 bold", text = format_date)
#w = Label1(canvas1, text=f"{dt.datetime.now():%a, %b %d %Y}", fg="white", bg="black", font=("helvetica", 40))
#DateLabel = canvas1.create_window( 100, 20,
#									anchor = "nw",
#									window = w)

def Simulator():
    for i in range(0,10):
         randomlist = random.randint(20,50)
         randomlist.append(n)
         print(randomlist[-1])

# mqtt_client_demo.on_connect
# Temp_Value = mqtt_client_demo.on_message

# def TempDisplay(Sub_Temp_Value):
#    # li = [1, 2, 3]
#    # li.append(random.randint(20,50))
#    # a = li[-1]
#    # print(a)  
#    print(Sub_Temp_Value)
#    Temp_Value = Sub_Temp_Value
#    T_label.config(text=Temp_Value)
#    T_label.after(1000, TempDisplay)
   
# #canvas1.create_text( 80, 30, fill="White",font="Times 15 bold", text = Celcius)   
# print(Global_Sub_Temp_Value)

# T_label = Label(canvas1, font=("Courier", 40, 'bold'), bg="lightblue", fg="black", bd =80)
# Temp_Label = canvas1.create_window( 100, 180,
#  									anchor = "nw",
#  									window = T_label)   

topic1 = Label(canvas1, font=("Courier", 30, 'bold'), bg="lightblue", fg="black", bd =80)
button1_canvas = canvas1.create_window( 100, 130,
									anchor = "nw",
									window = topic1)

topic2 = Label(canvas1, font=("Courier", 30, 'bold'), bg="lightblue", fg="black", bd =80)
button2_canvas = canvas1.create_window( 650, 130,
									anchor = "nw",
									window = topic2)
#topic1.grid(sticky = N, row = 2, column = 1, padx = 5, pady = (20,20))

# client.on_connect = on_connect
# client.on_message = on_message

#client.connect("broker.hivemq.com", 1883, 60)

# Sub_Temp_Value_SUB = mqtt_client_demo.on_message()
# print(Sub_Temp_Value_SUB)

#TempDisplay()
digitalclock()
client.loop_start()

#client.loop_forever()
#Simulator()
#Graph()

# Execute tkinter
root.mainloop()
