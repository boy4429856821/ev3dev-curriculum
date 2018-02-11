#This is the final project for Rose-Hulman's CSSE120,
# Introduction to Software Development,class from Coleman Weaver.
#This project was created for the purpose of honing my skills
#that I have accquired from the class. Specifically, this project
#is called Hot or Cold. In this project, I will be creating an AI
# that searches for an object using the IR sensor. Once it finds an object,
# it checks if it's the object it desires by checking the color of the object
# using the pixy camera. As the robot gets closer to object, it will check how close
#the object and depending on how close it is, a popup window will display a message
# depending on how far away it is from the robot. Once the object is close enough,
# it will pick up the object and beep.


#importing library

import ev3dev.ev3 as ev3
import time
import tkinter
from tkinter import ttk
import robot_controller as robo
import mqtt_remote_method_calls as com

#creating messages to be set to EV3
def sending_messages_to_ev3():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

def sending_messages_to_pc():
    mqtt_client = com.MqttClient
    mqtt_client.connect_to_pc()


