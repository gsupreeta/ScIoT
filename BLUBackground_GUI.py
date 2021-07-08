# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 20:57:31 2021

@author: dell
"""

# Import module
from tkinter import *
import tk_tools
import urllib
import urllib3
import requests
import time
import datetime as dt
from TempSImulatorTrail import *
import matplotlib.pyplot as plt


def Take_input():
    INPUT = entry1.get()
    print(INPUT)
    
def led_on():
    integer_val = 1
    urllib.request.urlopen("https://api.thingspeak.com/update?api_key=8LQBHYHYYL5IY7Z5&field2="+str(integer_val));
    print("LEDON")
   
def led_off():
    integer_val = 0
    urllib.request.urlopen("https://api.thingspeak.com/update?api_key=8LQBHYHYYL5IY7Z5&field2="+str(integer_val));
    print("LEDOFF")
    
URL = 'https://api.thingspeak.com/channels/1408549/feeds.json?api_key=SU8TJU0HVDKH9LEC&results'
get_data = requests.get(URL).json()
feild_1 = get_data['feeds']
print(feild_1)
temperature_data=[]
for x in feild_1:
    temperature_data.append(x['field1'])
print(temperature_data)

Over_Crowding_Indicator=[]
for x in feild_1:
    Over_Crowding_Indicator.append(x['field2'])
print(Over_Crowding_Indicator)
    
# Create object
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
canvas1.create_text( 750, 100, fill="Black",font="Times 20 italic bold", text = "Pulse Monitoring")


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
Last_element = Over_Crowding_Indicator[-1]

interger_LastElement = int(Last_element)
print(interger_LastElement)
print(type(interger_LastElement))
if interger_LastElement >= 1:
      led1.to_green()
else: 
     led1.to_grey()
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
display(format_date)
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


def TempDisplay():
   li = [1, 2, 3]
   li.append(random.randint(20,50))
   a = li[-1]
   print(a)
   Temp_Value = a("Degree Celcius:%d")
   T_label.config(text=Temp_Value)
   T_label.after(1000, TempDisplay)
   
#canvas1.create_text( 80, 30, fill="White",font="Times 15 bold", text = Celcius)   

T_label = Label(canvas1, font=("Courier", 40, 'bold'), bg="lightblue", fg="black", bd =80)
Temp_Label = canvas1.create_window( 100, 180,
									anchor = "nw",
									window = T_label)   


TempDisplay()
digitalclock()
#Simulator()

# Execute tkinter
root.mainloop()
