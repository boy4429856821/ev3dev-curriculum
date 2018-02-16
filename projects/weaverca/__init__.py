

import ev3dev.ev3 as ev3
import time
import tkinter
from tkinter import ttk
import robot_controller as robo
import mqtt_remote_method_calls as com

def main():
    Tinker = tkinter.Tk()
    Tinker.title = "It's the Hot or Cold Game"
    main_frame = ttk.Frame(Tinker, padding=5)
    main_frame.grid()
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=800, height=500)
    canvas.grid(columnspan=2)
    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)

































