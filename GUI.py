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
import json
import paho.mqtt.client as mqtt

#Global_Sub_Temp_Value = 0


# Create an MQTT client and attach our routines to it.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CoreElectronics/test")
    client.subscribe("CoreElectronics/topic")
    client.subscribe("HDU/Building1/Monitoring/Temperature")
    client.subscribe("HDU/Building1/Monitoring/Humidity")
    client.subscribe("HDU/Building1/Monitoring/Emergency")
    client.subscribe("HDU/Building1/Monitoring/OverCrowd")
    

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
        #ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys), interval=0)

        #plt.show()
    if msg.topic == "HDU/Building1/Monitoring/Humidity":
        print("TOPIC HUMIDITY")
        Global_Sub_Temp_Value = Sub_Temp_Value
        topic2.config(text=Sub_Temp_Value)
        
    if msg.topic == "HDU/Building1/Monitoring/Emergency":
        print("TOPIC Emergency Indication")
        if msg.payload == b'1':
            led.to_red()
            
        
        if msg.payload == b'0':
            led.to_grey()

        
        
    if msg.topic == "HDU/Building1/Monitoring/OverCrowd":
        print("TOPIC Emergency Indication")
        if msg.payload >= b'4':
            led1.to_red()
            
        
        if msg.payload < b'4':
            led1.to_grey()

def Graph():
    print("I am in GRAPH")

def animate(i, xs:list, ys:list):
    pass
#data from United Nations World Population Prospects (Revision 2019)
# https://population.un.org/wpp/, license: CC BY 3.0 IGO

def Take_input():
    INPUT = entry1.get()
    print(INPUT)
    
def led_on():
    print("LEDON")
   
def led_off():
    print("LEDOFF")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
print(client)

client.connect("broker.hivemq.com", 1883, 60)
root = Tk()
root. title('DIsplay Unit')

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

canvas1.create_text( 750, 450, fill="Black",font="Times 20 italic bold", text = "Overcrowd Warning")

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

def Simulator():
    for i in range(0,10):
         randomlist = random.randint(20,50)
         randomlist.append(n)
         print(randomlist[-1])


topic1 = Label(canvas1, font=("Courier", 30, 'bold'), bg="lightblue", fg="black", bd =80)
button1_canvas = canvas1.create_window( 50, 150,
									anchor = "nw",
									window = topic1)

topic2 = Label(canvas1, font=("Courier", 30, 'bold'), bg="lightblue", fg="black", bd =80)
button2_canvas = canvas1.create_window( 620, 150,
									anchor = "nw",
									window = topic2)

#TempDisplay()
digitalclock()
client.loop_start()

# Execute tkinter
root.mainloop()
