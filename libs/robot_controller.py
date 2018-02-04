"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    # DONE: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.TouchSensor = ev3.TouchSensor
        assert self.arm_motor.connected
        assert self.TouchSensor
        assert self.left_motor.connected
        assert self.right_motor.connected

    def drive_inches(self, distance, deg_speed):

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

        position2 = 90 * distance
        self.left_motor.run_to_rel_pos(position_sp=position2, speed_sp=deg_speed, stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=position2, speed_sp=deg_speed, stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_turn, turn_speed):

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.left_motor.run_to_rel_pos(position_sp=degrees_turn*4.15, speed_sp=turn_speed, stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=-degrees_turn*4.15, speed_sp=turn_speed, stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def left_forward(self, button_state):
        assert self.left_motor.connected

        while button_state:
            self.left_motor.run_forever(speed=600)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        self.left_motor.stop(stop_action="brake")

    def right_forward(self, button_state):
        assert self.right_motor.connected

        while button_state:
            self.right_motor.run_forever(speed=600)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        self.right_motor.stop(stop_action="brake")

    def right_backward(self, button_state):
        assert self.right_motor.connected

        while button_state:
            self.right_motor.run_forever(speed=-600)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        self.right_motor.stop(stop_action="brake")

    def left_backward(self, button_state):
        assert self.left_motor.connected

        while button_state:
            self.left_motor.run_forever(speed=-600)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        self.left_motor.stop(stop_action="brake")

    def shutdown(self):
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")
        print("Goodbye!")
        ev3.Sound.speak("Goodbye")

    def arm_calibiration(self, degrees):
        assert self.arm_motor.connected
        self.arm_motor.run_direct(speed_sp=700, position_sp=degrees, stop_action='brake')
        self.arm_motor.wait_while(ev3.MediumMotor.STATE_RUNNING)

    def arm_up(self):
        assert self.arm_motor.connected
        assert self.TouchSensor
        self.arm_motor.run_forever(speed_sp=900)
        while not self.TouchSensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")

    def arm_down(self):
        assert self.arm_motor.connected
        self.arm_motor.run_direct(speed_sp=900, position_sp=5112, stop_action="brake")
        self.arm_motor.wait_while(ev3.MediumMotor.STATE_RUNNING)