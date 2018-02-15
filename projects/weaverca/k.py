
import tkinter
from tkinter import ttk
import robot_controller as robo
import mqtt_remote_method_calls as com





def main():
    root = tkinter.Tk()
    root.title = "MQTT Shared Circles"

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    instructions = "Click the window to make a circle"
    label = ttk.Label(main_frame, text=instructions)
    label.grid(columnspan=2)

    # Make a tkinter.Canvas on a Frame.
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=800, height=500)
    canvas.grid(columnspan=2)

    # Make callbacks for mouse click events.
    canvas.bind("<Button-1>", lambda event: left_mouse_click(event, mqtt_client))

    # Make callbacks for the two buttons.
    clear_button = ttk.Button(main_frame, text="Clear")
    clear_button.grid(row=3, column=0)
    clear_button["command"] = lambda: clear(canvas)

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=1)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    # Create an MQTT connection
    # DONE: 5. Delete the line below (mqtt_client = None) then uncomment the code below.  It creates a real mqtt client.
    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect("draw", "draw")

    root.mainloop()