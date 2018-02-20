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


import time

import ev3dev.ev3 as ev3

import mqtt_remote_method_calls as com
from projects.weaverca import robot_controller1 as robo


def main():
    delegate = robo.Snatch3r()
    ev3.Sound.speak("Let's play the Hot and Cold Game!")
    mqtt = com.MqttClient(delegate)
    delegate.set_mqtt(mqtt)
    mqtt.connect_to_pc()
    mqtt.send_message('draw_circle_from_robot')



    time.sleep(0.05)
    delegate.loop_forever()

main()


