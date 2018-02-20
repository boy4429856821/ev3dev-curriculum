import ev3dev.ev3 as ev3
import robot_controller as robo
import mqtt_remote_method_calls as com
import time


COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]


class Delegate(object):
    def __init__(self):
        self.alphabet = None
        self.drive_speed = 100
        self.decode_speed = 0.5
        self.key = None

    def handle_code(self, alphabet):
        self.alphabet = alphabet
        print('recieved alphabet')

    def handle_key(self, key):
        self.key = key
        print('recieved key')

    def speed_up(self):
        self.drive_speed += 30
        self.decode_speed -= 0.01


def main():
    print('start')
    my_delegate = Delegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    robot = robo.Snatch3r()
    alt_var = 1
    sentence = ''

    while not robot.touch_sensor.is_pressed:
        print('looping')
        time.sleep(0.1)

    print('done with loop')

    alpha = my_delegate.alphabet
    lAnswer = my_delegate.key
    print(alpha)
    print(lAnswer)

    for k in range(len(lAnswer)):
        print('loop started')
        new_word = slow_decode(lAnswer[k], alpha, my_delegate.decode_speed)
        sentence += new_word
        sentence += ' '
        mqtt_client.send_message('print_robot_message', ['The robot has decoded word ' + str(k)])
        alternate(robot, alt_var, my_delegate.drive_speed)
        alt_var += 1

    mqtt_client.send_message('print_robot_message', ['Time is up, the sentence is: ' + sentence])


def alternate(robot, alt, speed):
    if alt % 2 == 0:
        color = ev3.ColorSensor.COLOR_BLACK
    else:
        color = ev3.ColorSensor.COLOR_WHITE
    print('alternate')
    while robot.color_sensor.color != color:
        robot.forward(speed, speed)
    robot.stop()


def slow_decode(word, alphabet, del_speed):
    returned_word = ''
    for k in range(len(word)):
        for i in range(len(alphabet)):
            print('decoding' + str(i))
            time.sleep(del_speed)
            if word[k] == alphabet[i][0]:
                returned_word += alphabet[i][0]
    print('done with word')

    return returned_word


main()
