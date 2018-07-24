import sys
from threading import Thread
import WonderPy.core.wwMain
from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.util import wwMath


class MyClass(object):

    def on_sensors(self, robot):
        """
        Print the distance data from each of the three distance sensors,
        also move the robot's head and body in reaction.
        See the comments in wwSensorDistance.py for more details about this sensor.
        """

        if not robot.has_ability(WWRobotConstants.WWRobotAbilities.DISTANCE_DETECT, True):
            exit(1)

        flf = robot.sensors.distance_front_left_facing
        frf = robot.sensors.distance_front_right_facing
        rer = robot.sensors.distance_rear

        # print out the values
        things = [
            ("front left-facing dist" , flf.distance_approximate),
            ("refl"                   , flf.reflectance),
            ("front right-facing dist", frf.distance_approximate),
            ("refl"                   , frf.reflectance),
            ("front rear dist"        , rer.distance_approximate),
            ("refl"                   , rer.reflectance),
        ]
        s = ""
        for thing in things:
            s += "%s: %7.2f  " % (thing[0], thing[1])
        sys.stdout.write('\r%s' % (s))
        sys.stdout.flush()

        # move the head up/down in response to the front distance
        front            = (flf.distance_approximate + frf.distance_approximate) * 0.5
        front_normalized = wwMath.inverse_lerp(0.0, 50.0, front)
        head_tilt        = wwMath.lerp(robot.head_tilt_min_deg, robot.head_tilt_max_deg, front_normalized)
        robot.cmds.head.stage_tilt_angle(head_tilt)

        # move the robot away from nearby obstacles
        dist_norm_front = 1.0 - wwMath.clamp01(front/10.0)
        dist_norm_rear  = 1.0 - wwMath.clamp01(rer.distance_approximate/10.0)
        dist_norm_delta = dist_norm_rear - dist_norm_front
        robot.cmds.body.stage_linear_angular(dist_norm_delta * 40.0, 0)


if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
