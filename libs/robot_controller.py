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
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    # DONE: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
    def __init__(self):
        self.running = True
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor.connected
        assert self.color_sensor.connected
        assert self.pixy.connected
        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        assert self.left_motor.connected
        assert self.right_motor.connected

    def drive_inches(self, distance, deg_speed):
        """Drives a given distance at a given speed (inches and inches/second)
           Drives forwards and backwards based on if the position is positive or negative
        """
        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

        position2 = 90 * distance
        self.left_motor.run_to_rel_pos(position_sp=position2, speed_sp=deg_speed, stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=position2, speed_sp=deg_speed, stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_turn, turn_speed):
        """Rotates by a given degree value and can rotate left or right based on the sign of the degrees"""
        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.left_motor.run_to_rel_pos(position_sp=degrees_turn*2*2.26, speed_sp=turn_speed, stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=-degrees_turn*2*2.26, speed_sp=turn_speed, stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def left_forward(self, button_state):
        """Runs the left motor at maximum speed and changing the left light green while the button is pressed"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        if button_state:
            self.left_motor.run_forever(speed_sp=900)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        else:
            self.left_motor.stop(stop_action="brake")
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def left_backward(self, button_state):
        """Runs the left motor in reverse at maximum speed and changing the left light red
           while the button is pressed"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        if button_state:
            self.left_motor.run_forever(speed_sp=-600)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        else:
            self.left_motor.stop(stop_action="brake")
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def right_forward(self, button_state):
        """Runs the right motor in at maximum speed and changing the right light green
           while the button is pressed"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        if button_state:
            self.right_motor.run_forever(speed_sp=900)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        else:
            self.right_motor.stop(stop_action="brake")
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def right_backward(self, button_state):
        """Runs the right motor in reverse at maximum speed and changing the right light red
           while the button is pressed"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        if button_state:
            self.right_motor.run_forever(speed_sp=-900)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        else:
            self.right_motor.stop(stop_action="brake")
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

    def arm_calibration(self):
        """Calibrates the gripper arm origin location by sending the arm up until it hits the touch sensor.
           After it hits the sensor, it goes down the set degrees to reach the calibrated origin"""
        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()
        arm_degrees_for_full_range = (14.2 * 360)
        self.arm_motor.run_to_rel_pos(position_sp=-arm_degrees_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()
        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        """Sends the arm up until it hits the touch sensor"""
        assert self.touch_sensor.connected
        assert self.arm_motor.connected
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

    def arm_down(self):
        """Sends the arm down the set degrees to the origin position"""
        assert self.touch_sensor.connected
        assert self.arm_motor.connected
        self.arm_motor.run_to_abs_pos(position=0)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep()

    def shutdown(self):
        """Stops the robot and sets the lights on the Brickman to green"""
        self.arm_motor.stop(stop_action="brake")
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

    def forward(self, left_speed, right_speed):
        """Moves the robot forward at the given speed"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.right_motor.run_forever(speed_sp=right_speed)
        self.left_motor.run_forever(speed_sp=left_speed)

    def left(self, left_speed, right_speed):
        """Rotates the robot left at the given speed"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.right_motor.run_forever(speed_sp=right_speed)
        self.left_motor.run_forever(speed_sp=-left_speed)

    def stop(self):
        """Stops the motors on the robot"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.right_motor.stop(stop_action="brake")
        self.left_motor.stop(stop_action="brake")

    def right(self, left_speed, right_speed):
        """Rotates the robot right at the given speed"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.right_motor.run_forever(speed_sp=-right_speed)
        self.left_motor.run_forever(speed_sp=left_speed)

    def back(self, left_speed, right_speed):
        """Moves the robot backward at the given speed"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.right_motor.run_forever(speed_sp=-right_speed)
        self.left_motor.run_forever(speed_sp=-left_speed)

    def loop_forever(self):
        """A loop for the MQTT so that it checks for inputs over the loops
           instead of the code running once and stopping"""
        self.running = True
        while self.running:
            time.sleep(0.01)

    def seek_beacon(self):
        """
        Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False.
        """

        ir_sensor = ev3.InfraredSensor()
        find_beacon = ev3.BeaconSeeker(ir_sensor, channel=1)

        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)
            current_heading = find_beacon.heading  # use the beacon_seeker heading
            current_distance = find_beacon.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.shutdown()
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)

                    if math.fabs(current_distance) == 0:
                        self.drive_inches(4, 100)
                        self.shutdown()
                        ev3.Sound.beep()
                        return True
                    else:
                        self.forward(100, 100)

                elif math.fabs(current_heading) <= 20:
                    if current_heading < 0:
                        self.forward(-100, 100)
                    else:
                        self.forward(100, -100)
                    print('turning to look for remote')
                else:
                    print(current_heading, ' , heading is too far off')

            time.sleep(0.2)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.shutdown()
        return False

    def forward_forever(self):
        """Moves the robot forward"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.right_motor.run_forever()
        self.left_motor.run_forever()

    def pixy(self):

        self.pixy.mode = "SIG1"
        self.turn_speed = 120

        while not self.touch_sensor.is_pressed:
            x = self.pixy.value(1)
            y = self.pixy.value(2)
            print("(X,Y)=({},{})".format(x, y))

            if x < 150:
                self.turn_degrees(-90, turn_speed)
                self.arm_up()
            if x > 170:
                self.turn_degrees(90, turn_speed)
            else:
                self.shutdown()
