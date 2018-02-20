import ev3dev.ev3 as ev3
import robot_controller as robo
import mqtt_remote_method_calls as com
import time


# create the delegate class
class Delegate(object):
    # set up variables
    def __init__(self):
        self.alphabet = None
        self.drive_speed = 100
        self.decode_speed = 0.5
        self.key = None

    # function to receive the completed alphanumeric code
    def handle_code(self, alphabet):
        self.alphabet = alphabet
        print('received alphabet')

    # function to receive the final sentence the robot is trying to decode (target sentence)
    def handle_key(self, key):
        self.key = key
        print('received key')

    # function to speed the robot up on its decoding process
    def speed_up(self):
        self.drive_speed += 30
        self.decode_speed -= 0.01


def main():
    print('start')
    # set up mqtt client and robot
    my_delegate = Delegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    robot = robo.Snatch3r()
    # create the variable that determines what color to drive to
    alt_var = 1
    # create the variable that will hold the decoded message
    sentence = ''

    # use the touch sensor to start
    while not robot.touch_sensor.is_pressed:
        print('looping')
        time.sleep(0.1)

    print('done with loop')
    # set variables to the received alphanumeric code and the target sentence
    alpha = my_delegate.alphabet
    lAnswer = my_delegate.key
    print(alpha)
    print(lAnswer)

    # cycle through the received target sentence
    for k in range(len(lAnswer)):
        print('loop started')
        # decode the string, passing in the current answer (which is a full word), the alphabet,
        # and the decode speed set by the delegate object
        new_word = slow_decode(lAnswer[k], alpha, my_delegate.decode_speed)
        # add the decoded word to the final decoded sentence variable and a space in between the words
        sentence += new_word
        sentence += ' '
        # tell the player that the robot has decoded a word
        mqtt_client.send_message('print_robot_message', ['The robot has decoded word ' + str(k)])
        # call the function that drives the robot forward to the next spot passing in the robot, alternation variable,
        # and drive speed set by the delegate
        alternate(robot, alt_var, my_delegate.drive_speed)
        # change the alternation variable
        alt_var += 1

    # once the robot is done decoding the whole string, tell the player they have lost and what the sentence was
    mqtt_client.send_message('print_robot_message', ['Time is up, the sentence is: ' + sentence])


# function for driving the robot forward to either a black or white part of the floor
def alternate(robot, alt, speed):
    # if the alternation variable is divisible by 2, drive to black. Otherwise drive to white
    if alt % 2 == 0:
        color = ev3.ColorSensor.COLOR_BLACK
    else:
        color = ev3.ColorSensor.COLOR_WHITE
    print('alternate')
    # drive the robot forward using the speed from the delegate and stop after it has found the correct color
    while robot.color_sensor.color != color:
        robot.forward(speed, speed)
    robot.stop()


# decode a word out of the final answer, slowly
def slow_decode(word, alphabet, del_speed):
    # set up the returned variable
    returned_word = ''
    # cycle through the given part of the answer
    for k in range(len(word)):
        # cycle through the alphabet
        for i in range(len(alphabet)):
            print('decoding' + str(i))
            # wait for the amount of time set by the delegate
            time.sleep(del_speed)
            # if the letter from the answer is the same as the current letter in the alphabet,
            # add that letter to the returned string
            if word[k] == alphabet[i][0]:
                returned_word += alphabet[i][0]
    print('done with word')

    return returned_word


main()
