from threading import Thread
import time

import WonderPy.core.wwMain
from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.components.wwMedia import WWMedia


"""
This example shows connecting to the robot and issuing some simple commands.
See the other 'tutorial' and 'misc' examples for more complex scenarios!
"""


class MyClass(object):

    def on_connect(self, robot):
        """
        Called when we connect to a robot. This method is optional. Do not Block in this method !
        """

        print("Starting a thread for %s." % (robot.name))
        Thread(target=self.thread_hello, args=(robot,)).start()

    def thread_hello(self, robot):
        # robot is the robot we've connected to.

        # get a short list of sounds to play for this robot
        sound_names = self.get_hello_sounds(robot)

        for sound_name in sound_names:
            # for each sound in the list: turn on the lights, play the sound, dim the lights, then pause a little.
            print("On robot %s, setting all RGB lights to white." % (robot.name))
            robot.cmds.RGB.stage_all(1, 1, 1)

            print("On robot %s, playing '%s'." % (robot.name, sound_name))
            robot.cmds.media.do_audio(sound_name)

            print("On robot %s, setting all RGB lights to dim." % (robot.name))
            robot.cmds.RGB.stage_all(0.2, 0.2, 0.2)

            print("Waiting a little bit.")
            time.sleep(3)

        print("On robot %s, setting all RGB lights to off." % (robot.name))
        robot.cmds.RGB.stage_all(0, 0, 0)
        print("That's all for now.")

    def get_hello_sounds(self, for_this_robot):
        # we don't know ahead-of-time if the robot will be a Cue, Dash, or Dot,
        # so we handle each of those cases now with an appropriate list of sounds to play:
        if for_this_robot.robot_type == WWRobotConstants.RobotType.WW_ROBOT_DASH:
            return [WWMedia.WWSound.WWSoundDash.HOWDY,
                    WWMedia.WWSound.WWSoundDash.HOWSGOING,
                    WWMedia.WWSound.WWSoundDash.LETS_GO,
                    ]

        elif for_this_robot.robot_type == WWRobotConstants.RobotType.WW_ROBOT_DOT:
            return [WWMedia.WWSound.WWSoundDot.HOWDY,
                    WWMedia.WWSound.WWSoundDot.HOLD_ME,
                    WWMedia.WWSound.WWSoundDot.READYSET,
                    ]

        elif for_this_robot.robot_type == WWRobotConstants.RobotType.WW_ROBOT_CUE:
            return [WWMedia.WWSound.WWSoundCue.zest_HEYWHSU,
                    WWMedia.WWSound.WWSoundCue.charge_BORESTNOC,
                    WWMedia.WWSound.WWSoundCue.pep_YOUSOGOT,
                    ]
        else:
            raise ValueError("unhandled robot type: %s on %s" % (str(for_this_robot.robot_type), for_this_robot.name))



# kick off the program !
if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
