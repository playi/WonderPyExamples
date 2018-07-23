from threading import Thread
import WonderPy.core.wwMain
from WonderPy.core.wwConstants import WWRobotConstants

STAR_NUM_POINTS     =  5
STAR_EDGE_LENGTH_CM = 50


class MyClass(object):

    def on_connect(self, robot):
        """
        start threads which emit robot commands based on their own timing, rather than in response to sensor packets.
        """

        if not robot.has_ability(WWRobotConstants.WWRobotAbilities.BODY_MOVE, True):
            exit(1)

        Thread(target=self.async_1, args=(robot,)).start()

    def async_1(self, robot):

        while True:

            print("Press the button!")
            robot.block_until_button_main_press_and_release()

            print("Resetting the pose global position to origin")
            robot.cmds.body.do_pose(0, 0, 0, 0, WWRobotConstants.WWPoseMode.WW_POSE_MODE_SET_GLOBAL)

            robot.cmds.accessory.do_sketchkit_pen_down()
            global STAR_NUM_POINTS
            global STAR_EDGE_LENGTH_CM
            self.do_star(robot, STAR_NUM_POINTS, STAR_EDGE_LENGTH_CM)
            robot.cmds.accessory.do_sketchkit_pen_up()

    def do_star(self, robot, numPoints, edge_length):
        if numPoints % 2 == 0:
            print("can only do stars with an odd number of points")
            return

        if numPoints < 3:
            print("Need at least 3 points for a star")

        turn_deg =  180.0 * (1.0 - 1.0 / numPoints)
        half_internal = (180.0 - turn_deg) * 0.5
        speed = 20.0

        # turn clockwise away from center by half of one full vertex angle
        robot.cmds.body.do_pose(0, 0, -half_internal, 0.5, WWRobotConstants.WWPoseMode.WW_POSE_MODE_RELATIVE_COMMAND)

        for n in xrange(numPoints):
            print("driving to vertex %d" % (n + 1))
            robot.cmds.body.do_pose(0, edge_length, 0, edge_length / speed,
                                    WWRobotConstants.WWPoseMode.WW_POSE_MODE_RELATIVE_COMMAND)

            # turn counter-clockwise by one vertex angle
            td = turn_deg

            # if last vertex, turn an additional half vertex angle to restore the original orientation of the robot
            if n == numPoints - 1:
                td += half_internal

            robot.cmds.body.do_pose(0, 0, td, 0.5, WWRobotConstants.WWPoseMode.WW_POSE_MODE_RELATIVE_COMMAND)


if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
