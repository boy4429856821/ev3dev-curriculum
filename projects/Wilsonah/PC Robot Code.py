"""
Author: Andrew Wilson

Objective: This code is meant to be the code run on the PC for the Robot Project. This code will send physical and
           digital (GUI) inputs. It will receive analog inputs from the color sensor. It plays a Pokemon themed game of
           Rock, Paper, Scissors.
"""
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import random


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, color_message):
        self.challenger = color_message
        self.color = 0

    """Receives a color value from the robot color sensor and determines the challenger from it"""
    def color_found(self, color):
        self.color = color
        if self.color == ev3.ColorSensor.COLOR_RED:
            message_to_display = "Tailor Red"
            self.challenger.configure(text=message_to_display)

        if self.color == ev3.ColorSensor.COLOR_BLUE:
            message_to_display = "Origami Artist Blue"
            self.challenger.configure(text=message_to_display)

        if self.color == ev3.ColorSensor.COLOR_BROWN:
            message_to_display = "Geologist Brown"
            self.challenger.configure(text=message_to_display)

        if self.color == ev3.ColorSensor.COLOR_YELLOW:
            message_to_display = "Champion Goldy"
            self.challenger.configure(text=message_to_display)


def main():
    root = tkinter.Tk()
    root2 = tkinter.Tk()
    root.title("Ground Control")
    root2.title("Map")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    second_frame = ttk.Frame(root2, padding=20, relief='raised')
    second_frame.grid()

    canvas = tkinter.Canvas(second_frame, background='green', width=800, height=500)
    canvas.grid(columnspan=2)

    """Creates the graphic for the game map and sets the icon representing the robot"""
    canvas.create_rectangle((0, 500), (300, 450), fill="black")
    canvas.create_rectangle((300, 500), (350, 300), fill="black")
    canvas.create_rectangle((150, 300), (350, 350), fill="black")
    canvas.create_rectangle((150, 350), (200, 100), fill="black")
    canvas.create_rectangle((150, 100), (600, 150), fill="black")
    canvas.create_rectangle((600, 100), (650, 400), fill="black")
    canvas.create_rectangle((600, 400), (750, 450), fill="black")
    canvas.create_rectangle((750, 400), (800, 450), fill="silver")
    canvas.create_oval(150, 425, 175, 450, fill="blue", width=3)
    canvas.create_oval(125, 275, 150, 250, fill="brown", width=3)
    canvas.create_oval(425, 150, 450, 175, fill="red", width=3)
    canvas.create_oval(787.5, 412.5, 762.5, 437.5, fill="gold", width=3)
    """Creates the labels and inputs on the Tkinter"""
    game_label = ttk.Label(main_frame, text="Rock, Paper, or Scissors?")
    game_label.grid(row=4, column=1)

    game_entry = ttk.Entry(main_frame, width=8)
    game_entry.grid(row=5, column=1)

    result_message = ttk.Label(main_frame, text="--")
    result_message.grid(row=6, column=1)

    enter_button = ttk.Button(main_frame, text="SHOOT!")
    enter_button.grid(row=6, column=0)
    enter_button['command'] = lambda: game(game_entry, color_message, challenger_message, result_message, canvas)

    # Buttons for quit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=6, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    """Push at the beginning to start searching for a color"""
    e_button = ttk.Button(main_frame, text="Seek Opponent")
    e_button.grid(row=5, column=2)
    e_button['command'] = (lambda: seek_color(mqtt_client, color_message, challenger_message, result_message))

    """Creates the Labels for the challengers"""
    color_label = ttk.Label(main_frame, text="  Challenger ")
    color_label.grid(row=0, column=1)

    color_message = ttk.Label(main_frame, text="--")
    color_message.grid(row=1, column=1)

    challenger_message = ttk.Label(main_frame, text="--")
    challenger_message.grid(row=2, column=1)

    """Sends the delegate through the mqtt"""
    pc_delegate = MyDelegateOnThePc(color_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    """Loops to keep checking the inputs and actually renders the canvas and Tkinter"""
    root.mainloop()


"""On the click of the button SHOOT!, the "game" function reads the entry box and plays a game of Rock, Paper, Scissors 
   based on the challengers occupation (their name). The Champion is the only legitimate game. Thunderbolt is a backdoor easter egg 
   so I can show me beating the champion (and for fun, the others) and not face a random number generator to make the 
   video"""


def game(entry, color_message, challenger_play, result, canvas):
    player = canvas.create_oval(25, 465, 50, 490, fill="grey", width=3)
    if color_message.cget("text") == "--":
        result.configure(text="There is a time and place for everything, but not now")
    if color_message.cget("text") == "Tailor Red":
        canvas.delete(player)
        player = canvas.create_oval(425, 115, 450, 140, fill="grey", width=3)
        if entry.get() == "Scissors":
            result.configure(text="You Tied. Try Again")
            challenger_play.configure(text="Scissors")
        if entry.get() == "Rock":
            result.configure(text="YOU WIN!")
            challenger_play.configure(text="Scissors")
        if entry.get() == "Paper":
            result.configure(text="You Lost. Try Again")
            challenger_play.configure(text="Scissors")
        if entry.get() == "Thunderbolt":
            result.configure(text="The Scissors were struck by lightning. YOU WIN!")
            challenger_play.configure(text="Scissors")

    if color_message.cget("text") == "Geologist Brown":
        canvas.delete(player)
        player = canvas.create_oval(165, 275, 190, 250, fill="grey", width=3)
        if entry.get() == "Scissors":
            result.configure(text="You Lost. Try Again")
            challenger_play.configure(text="Rock")
        if entry.get() == "Rock":
            result.configure(text="You Tied. Try Again")
            challenger_play.configure(text="Rock")
        if entry.get() == "Paper":
            result.configure(text="YOU WIN!")
            challenger_play.configure(text="Rock")
        if entry.get() == "Thunderbolt":
            result.configure(text="The Rock was struck by lightning. YOU WIN!")
            challenger_play.configure(text="Rock")

    if color_message.cget("text") == "Origami Artist Blue":
        canvas.delete(player)
        player = canvas.create_oval(150, 465, 175, 490, fill="grey", width=3)
        if entry.get() == "Scissors":
            result.configure(text="YOU WIN")
            challenger_play.configure(text="Paper")
        if entry.get() == "Rock":
            result.configure(text="You Lost. Try Again")
            challenger_play.configure(text="Paper")
        if entry.get() == "Paper":
            result.configure(text="You Tied. Try Again")
            challenger_play.configure(text="Paper")
        if entry.get() == "Thunderbolt":
            result.configure(text="The Paper was struck by lightning. YOU WIN!")
            challenger_play.configure(text="Paper")

    if color_message.cget("text") == "Champion Goldy":
        canvas.delete(player)
        player = canvas.create_oval(787.5 - 50, 412.5, 762.5 - 50, 437.5, fill="grey", width=3)
        plays = ["Rock", "Paper", "Scissors"]
        play = plays[random.randrange(0, 4)]
        if entry.get() == play:
            result.configure(text="You Tied. Try Again")
            challenger_play.configure(text=play)
        if entry.get() != play:
            if play == "Rock":
                if entry.get() == "Paper":
                    result.configure(text="YOU ARE THE NEW CHAMPION!")
                    challenger_play.configure(text=play)
                if entry.get() == "Scissors":
                    result.configure(text="You Lost. Try Again")
                    challenger_play.configure(text=play)
            if play == "Paper":
                if entry.get() == "Scissors":
                    result.configure(text="YOU ARE THE NEW CHAMPION!")
                    challenger_play.configure(text=play)
                if entry.get() == "Rock":
                    result.configure(text="You Lost. Try Again")
                    challenger_play.configure(text=play)
            if play == "Scissors":
                if entry.get() == "Rock":
                    result.configure(text="YOU ARE THE NEW CHAMPION!")
                if entry.get() == "Paper":
                    result.configure(text="You Lost. Try Again")
                    challenger_play.configure(text=play)
        if entry.get() == "Thunderbolt":
            result.configure(text="The {} was struck by lightning. YOU ARE THE NEW CHAMPION!".format(play))
            challenger_play.configure(text=play)


def seek_color(mqtt_client, color_message, challenger_play, result):
    """Sends command to robot to search for colors and clears the GUI"""
    color_message.configure(text="--")
    challenger_play.configure(text="--")
    result.configure(text="--")
    mqtt_client.send_message("find_color")


# Quit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()
