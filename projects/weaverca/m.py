import tkinter
from tkinter import ttk


# d: 4. Uncomment the code below.  It imports a library and creates a relatively simple class.
# The constructor receives a Tkinter Canvas and the one and only method draws a circle on that canvas at a given XY.

import mqtt_remote_method_calls as com
import robot_controller as robo

# robot = robo.Snatch3r()

class MyDelegate(object):

    def __init__(self, canvas):
        self.canvas = canvas

    def on_circle_draw(self, color, x, y):
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, width=3)



def main():

    root = tkinter.Tk()
    root2 = tkinter.Toplevel(root)

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    side_frame = ttk.Frame(root2, padding =10)
    side_frame.grid()

    title = "It's the hot and cold game"
    label = ttk.Label(main_frame, text=title)
    label.grid(columnspan=3)

    instructions = "hit the WASD to move around, the screen will say hot, hotter,cold, or very cold. Try to get to the object."
    label = ttk.Label(main_frame, text=instructions)
    label.grid(columnspan=3)

    # Make a tkinter.Canvas on a Frame.
    canvas = tkinter.Canvas(main_frame, background="grey", width=600, height=600)
    canvas.grid(columnspan=3)
    canvas1 = tkinter.Canvas(side_frame, background="grey", width=1000, height=600)
    canvas1.grid(columnspan=3)
    my_delegate = MyDelegate(canvas1)
    mqtt_client = com.MqttClient(my_delegate)

    if mqtt_client.connect_to_ev3() is True:
        my_delegate.on_circle_draw('red',497,288)

    # mqtt_client.send_message('pixy')      Need to put this into the Library

    # Make callbacks for mouse click events.

    canvas1.bind("<Button-1>", lambda event: left_mouse_click(event, mqtt_client))

    # Make callbacks for the two buttons.
    clear_button = ttk.Button(main_frame, text="restart")
    clear_button.grid(row=3, column=0)
    clear_button["command"] = lambda: clear(canvas)

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=2)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    forward_button = ttk.Button(main_frame, text ="Forward")
    forward_button.grid(row=2, column = 0)
    if forward_button is True:
        forward_button['command'] = lambda: drive_forward(mqtt_client,my_delegate)

    backward_button = ttk.Button(main_frame, text = "Backward")
    backward_button.grid(row=2, column =1)
    if backward_button is True:
        backward_button['command'] =lambda: drive_backward(mqtt_client)

    turn_button = ttk.Button(main_frame, text = "Turn")
    turn_button.grid(row=2, column = 2)
    if turn_button is True:
        turn_button['command'] = lambda: turn(mqtt_client)

    options_button = ttk.Button(main_frame, text = 'Options')
    options_button.grid(row=3, column = 1)
    options_button['command'] = lambda: options(mqtt_client)

    root.mainloop()


def left_mouse_click(event, mqtt_client):
    print("You clicked location ({},{})".format(event.x, event.y))
    my_color = "navy"
    mqtt_client.send_message('on_circle_draw', [my_color, event.x, event.y])



def clear(canvas):
    canvas.delete("all")


def quit_program(mqtt_client):
    if mqtt_client:
        mqtt_client.close()
    exit()


def exit_program(root3):
    if root3:
        root3.destroy()


def drive_forward(mqtt_client,my_delegate):
        mqtt_client.send_message('forward_forever')
        my_delegate.on_circle_draw("red",100, 100)


def drive_backward(mqtt_client):
        mqtt_client.send_message('back')


def turn(mqtt_client):
        mqtt_client.send_message('right')


def options(mqtt_client):
    root3 = tkinter.Toplevel()
    var1 = tkinter.IntVar(0)
    checkbutton = tkinter.Checkbutton(root3,text='Pixy Sensor',variable = var1)
    checkbutton.grid(row=0,sticky='w')
    if var1 == 0:
        mqtt_client.send_message('seek_beacon')
    var2 = tkinter.IntVar()
    var2.set(0)
    if var2 == 0:
        mqtt_client.send_message('pixy')
    checkbutton1 = tkinter.Checkbutton(root3,text='IR Sensor',variable = var2)
    checkbutton1.grid(row=1, sticky ='w')

    exit_button = tkinter.Button(root3,text= "exit", state ='active')
    exit_button.grid(columnspan = 2)
    exit_button['command'] = lambda: exit_program(root3)

    title = "Checking one of these boxes disables the sensor"
    label = ttk.Label(root3, text=title)
    label.grid(columnspan=3)


# Have to draw circle onto the canvas window through some way (to do list)
# steps:
# need to have a center, where does x and y of the robot correlate with the canvas screen?:  (maybe?)
# have to have the circle move while the robot is also moving  (have to test)
# have the circle turn a different color when it finds the object through Pixy Sensor or IR Sensor
# have to have the arm move up when object is found  (easy once I get the code before this working)
# put an image as the canvas to make the interface look better (look on tkinter website for this == 'easy')
# disable the pixy camera and the IR Sensor in some way (need some kind of command like break or don't assert)
# need to cite











# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
