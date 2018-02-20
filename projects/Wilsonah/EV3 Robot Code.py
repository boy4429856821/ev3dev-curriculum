"""
Author: Andrew Wilson

Objective: This code is meant to be the code run on the EV3 robot for the Robot Project. This code will receive physical
           and digital (GUI) inputs from the PC. It will also send Brickman button inputs and sensor data to the PC
"""
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True


def main():
    robot = robo.Snatch3r()
    ev3.Sound.speak("I am Running")  # Makes the robot speak so i know it has run the program
    mqtt_client = com.MqttClient(robot)
    robot.set_mqtt(mqtt_client)  # Sets the mqtt so I can use it in the delegate
    mqtt_client.connect_to_pc()
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.


main()





