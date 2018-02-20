



#importing libraries
import ev3dev.ev3 as ev3
import time
import tkinter
from tkinter import ttk
import robot_controller as robo
import mqtt_remote_method_calls as com








#creates a Mqtt Client
def sending_messages_to_ev3():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()