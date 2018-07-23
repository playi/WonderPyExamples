# -*- coding: utf-8 -*-

from threading import Thread
import WonderPy.core.wwMain
from WonderPy.core.wwConstants import WWRobotConstants


"""
This example shows connecting to the robot and sending commands each time sensors are received.
This builds on the "01_hello_world.py" example.
"""


class MyClass(object):

    def on_sensors(self, robot):
        """
        Called approximately 30 times per second - each time sensor data is received from the robot.
        This method is optional.
        Do not block in here !
        This means only call the stage_foo() flavor of robot commands, and not the do_foo() versions.
        """

    def on_connect(self, robot):
        """
        Called when we connect to a robot. This method is optional. Do not Block in this method !
        """

        print("Starting a thread for %s." % (robot.name))
        Thread(target=self.thread_mover, args=(robot,)).start()

    def thread_mover(self, robot):
        # turn the robot this way and that

        if not robot.has_ability(WWRobotConstants.WWRobotAbilities.BODY_MOVE, True):
            # it doesn't do any harm to send drive commands to a robot with no wheels,
            # but it doesn't help either.
            print(u"%s cannot drive! try a different example." % (robot.name))
            return

        while True:

            # call convenience function to wait for button press
            print(u"%s waiting for button press." % (robot.name))
            robot.block_until_button_main_press_and_release()

            print(u"%s driving forward 20cm at 10cm/s." % (robot.name))
            robot.cmds.body.do_forward(20, 10)

            print(u"%s turning head to 120° left." % (robot.name))
            robot.cmds.head.stage_pan_angle(120)

            print(u"%s turning body around to the left." % (robot.name))
            robot.cmds.body.do_turn(180, 200)

            print(u"%s turning head back to  0°." % (robot.name))
            robot.cmds.head.stage_pan_angle(0)

            # now repeat: drive back. this time we'll turn the head / body the other way tho.

            print(u"%s driving forward 20cm at 10cm/s." % (robot.name))
            robot.cmds.body.do_forward(20, 10)

            print(u"%s turning head to 120° right." % (robot.name))
            robot.cmds.head.stage_pan_angle(-120)

            print(u"%s turning body around to the right." % (robot.name))
            robot.cmds.body.do_turn(-180, 200)

            print(u"%s turning head back to  0°." % (robot.name))
            robot.cmds.head.stage_pan_angle(0)


if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
