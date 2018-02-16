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

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):

     def __init__(self,canvas):
        self.canvas = canvas


def main():

    tinker = tkinter.Tk()
    tinker.title = "It's the Hot or Cold Game"
    main_frame = ttk.Frame(tinker, padding=5)
    main_frame.grid()
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=800, height=500)
    canvas.grid(columnspan=2)
    canvas.bind("<Button-1>", lambda event: left_mouse_click(event, mqtt_client))
    clear_button = ttk.Button(main_frame, text="Clear")
    clear_button.grid(row=3, column=0)
    clear_button["command"] = lambda: clear(canvas)
    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=1)
    quit_button["command"] = lambda: quit_program(mqtt_client)
    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect("draw", "draw")
    print("Shutdown complete.")

    def clear(canvas):
        canvas.delete("all")

    def quit_program(mqtt_client):
        if mqtt_client:
            mqtt_client.close()
        exit()

    tinker.mainloop()


def left_mouse_click(event, mqtt_client):
    print("You clicked location ({},{})".format(event.x, event.y))
    mqtt_client.send_message('on_circle_draw', [ event.x, event.y])