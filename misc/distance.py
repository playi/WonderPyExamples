import sys
from threading import Thread
import WonderPy.core.wwMain
from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.util import wwMath


class MyClass(object):

    def on_connect(self, robot):
        Thread(target=self.thread_turn_around, args=(robot,)).start()

    def thread_turn_around(self, robot):

        while True:
            if robot.sensors.distance_rear.distance_approximate < 10:
                print("Hey, there's something behind me!")
                robot.cmds.body.do_turn(180, 360)
            robot.block_until_sensors()

    def on_sensors(self, robot):
        """
        Print the distance data from each of the three distance sensors.
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


if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
