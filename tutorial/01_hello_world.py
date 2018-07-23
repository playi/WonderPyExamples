from threading import Thread
import time

import WonderPy.core.wwMain
from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.components.wwMedia import WWMedia


"""
This example shows very basic connecting to a robot and sending some simple commands.
Basic steps:

1. add the imports
2. create a Class (in this case named "MyClass").
3. create a method named "on_connect" which accepts self and a robot parameter.
     eg on_connect(self, robot).
     This will be called when the program connects to a robot.
4. kick things off my passing an instance of your Class to WonderPy.wwMain.start():
     WonderPy.wwMain.start(MyClass())
5. Try it! Your on_connect method should be called.
6. on_connect() itself should not block - ie, it should return control as soon as possible.
     However, on_connect() can launch some asynchronous processes, which can block.
     So do that. In this example we spawn a thread on method thread_hello().
7. In the thread, try out some robot commands!
     * Commands of the flavour "stage_foo()" simply send the command to the robot and return.
         ie, they do not block.
     * Commands of the flavour "do_foo()" send the commands and block until the command completes.
"""


class MyClass(object):

    def on_connect(self, robot):
        """
        Called when we connect to a robot. This method is optional. Do not Block in this method !
        """

        print("Starting a thread for %s." % (robot.name))
        Thread(target=self.thread_hello, args=(robot,)).start()

    def thread_hello(self, robot):
        """
        :param robot: WWRobot
        """

        # dictionary mapping robot types to a few sounds for that robot
        hello_sounds = {
            WWRobotConstants.RobotType.WW_ROBOT_DASH : [WWMedia.WWSound.WWSoundDash.HOWDY,
                                                        WWMedia.WWSound.WWSoundDash.HOWSGOING       ],
            WWRobotConstants.RobotType.WW_ROBOT_DOT  : [WWMedia.WWSound.WWSoundDot .HOWDY,
                                                        WWMedia.WWSound.WWSoundDot .HOLD_ME         ],
            WWRobotConstants.RobotType.WW_ROBOT_CUE  : [WWMedia.WWSound.WWSoundCue .zest_HEYWHSU,
                                                        WWMedia.WWSound.WWSoundCue .charge_BORESTNOC],
        }

        if robot.robot_type not in hello_sounds:
            raise ValueError("unhandled robot type: %s on %s" % (str(robot.robot_type), robot.name))

        for sound_name in hello_sounds[robot.robot_type]:

            print("On %s, setting all RGB lights to white." % (robot.name))
            robot.cmds.RGB.stage_all(1, 1, 1)

            print("On %s, playing '%s'." % (robot.name, sound_name))
            robot.cmds.media.do_audio(sound_name)

            print("On %s, setting all RGB lights to off." % (robot.name))
            robot.cmds.RGB.stage_all(0, 0, 0)

            print("Waiting a little bit.")
            time.sleep(1)

        print("That's all for now.")


# kick off the program !
if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
