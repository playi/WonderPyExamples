import math
import WonderPy.core.wwMain
from WonderPy.util import wwMath

"""
This example shows connecting to the robot and sending commands each time sensors are received.
Basic steps:

1. add the imports
2. create a Class (in this case named "MyClass").
3. create a method named "on_sensors" which accepts self and a robot parameter.
     eg on_sensors(self, robot).
4. kick things off by passing an instance of your Class to WonderPy.wwMain.start():
     WonderPy.wwMain.start(MyClass())
5. Try it! Your on_sensors method should be called about 30 times per second.
     Note: on_sensors() itself should not block - ie, it should return control as soon as possible.
     This means you should not call the do_foo() family of commands from here.
     Calling stage_foo() commands are fine tho.
6. Add some sensor handling!
     It's easy to print values out, but a bit more fun to turn them around into robot-expressiveness.
     In the example here we translate the robot's 3-axis accelerometer values into RGB,
     and also map the four buttons to regions of the LED eyering.
"""


class MyClass(object):

    def on_connect(self, robot):
        """
        Called when we connect to a robot. This method is optional. Do not Block in this method !
        """

        print("Tilt '%s' to control the color LEDs,\nPress the buttons on top of '%s' to light up the eye!" % (robot.name, robot.name ))

    def on_sensors(self, robot):
        """
        Called approximately 30 times per second - each time sensor data is received from the robot.
        This method is optional.
        Do not block in here !
        This means only call the stage_foo() flavor of robot commands, and not the do_foo() versions.
        """

        # map from the robots four buttons to indices of the eyering array.
        # the LED at the top of the eye-ring (12 O'Clock) is index 0, increasing clockwise to 11.
        # this will be used so that each of the three minor buttons light up a segment of 3 LEDs,
        # and the main button lights up the remaining 3.
        dict = {
            robot.sensors.button_1   : ( 7, 8,  9),
            robot.sensors.button_2   : ( 3, 4,  5),
            robot.sensors.button_3   : (11, 0,  1),
            robot.sensors.button_main: ( 2, 6, 10),
        }

        # create an array of 12 booleans according to which buttons are pressed.
        # there's probably a more pythonic way to do this.
        LEDs = [False] * 12
        for button in dict:
            if button.pressed:
                for index in dict[button]:
                    LEDs[index] = True

        # stage the command on the robot.
        # "staged" commands are saved up and only actually sent after a set of sensors is received.
        # this helps rate-limit commands to the robot, and does not block current execution.
        robot.cmds.eyering.stage_eyering(LEDs, 1.0)

        # more fun: let's convert the 3 axes of the accelerometer to an RGB color.
        # the accelerometer reports 1.0 for "z" when the robot is at rest.
        # we raise the value to the 3rd power to push small values closer to zero,
        # and then clamp to the range [0, 1].
        # this means that if the robot is say upside down, r g and b should all be 0.
        r = wwMath.clamp01(math.pow(robot.sensors.accelerometer.x, 3))
        g = wwMath.clamp01(math.pow(robot.sensors.accelerometer.y, 3))
        b = wwMath.clamp01(math.pow(robot.sensors.accelerometer.z, 3))
        robot.cmds.RGB.stage_all(r, g, b)


if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
