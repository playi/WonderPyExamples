import sys
import colorsys

import WonderPy
from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.util import wwMath


class MyClass(object):

    def on_connect(self, robot):
        if not robot.has_ability(WWRobotConstants.WWRobotAbilities.HEAD_MOVE, True):
            exit(1)

        # turn off the eyering to show the other lights better
        robot.cmds.eyering.stage_eyering([False] * 12, 0.0)

        print("Turn my head this way and that!")

    def on_sensors(self, robot):
        """
        Print the head pan and tilt values.
        Also just for fun, convert them into HSV colors on the robot's RGB leds
        """

        pan  = robot.sensors.head_pan .degrees
        tilt = robot.sensors.head_tilt.degrees

        things = [
            ("pan" , pan ),
            ("tilt", tilt),
        ]
        s = ""
        for thing in things:
            s += "%s: %7.2f  " % (thing[0], thing[1])
        sys.stdout.write('\r%s' % (s))
        sys.stdout.flush()

        # hsv
        pan_normalized = wwMath.clamp01(wwMath.inverse_lerp(robot.head_pan_min_deg , robot.head_pan_max_deg , pan ))
        tlt_normalized = wwMath.clamp01(wwMath.inverse_lerp(robot.head_tilt_min_deg, robot.head_tilt_max_deg, tilt))

        h = pan_normalized
        if (tlt_normalized < 0.5):
            s = 1.0
            v = wwMath.inverse_lerp(0.0, 0.5, tlt_normalized)
        else:
            s = wwMath.inverse_lerp(1.0, 0.5, tlt_normalized)
            v = 1.0

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        robot.cmds.RGB.stage_all(r, g, b)


if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
