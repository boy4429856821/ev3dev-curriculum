#!/usr/bin/env python3
"""
The goal of this module is to practice using the Pixy and MQTT at the same time.  This module will send data from the
EV3 to the PC.

Authors: David Fisher and Coleman Weaver February 2017.
"""  # Done.

import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    print("--------------------------------------------")
    print(" Pixy display")
    print(" Press the touch sensor to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("Pixy display").wait()
    print("Press the touch sensor to exit this program.")

    # Done 2
    # Then connect to the pc using the connect_to_pc method.
    mqtt_client = com.MqttClient()
    robot = robo.Snatch3r()
    mqtt_client.connect_to_pc()
    robot.pixy.mode = "SIG1"

    while not robot.touch_sensor.is_pressed:

        # Done 3
        #
        x = robot.pixy.value(1)
        y = robot.pixy.value(2)
        width = robot.pixy.value(3)
        height = robot.pixy.value(4)
        print("(X, Y)=({}, {}) Width={} Height={}".format(x, y, width, height))

        # Done 4
        # If you open m2_pc_pixy_display you can see the parameters for that method [x, y, width, height]
        mqtt_client.send_message('on_rectangle_update', [x,y,width,height])
        time.sleep(0.25)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()
    mqtt_client.close()

# Done
#
# Observations you should make, if the EV3 has data the PC can know that data too using MQTT.


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()

