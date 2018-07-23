import sys
import os.path
import argparse
from threading import Thread
import WonderPy.core.wwMain
from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.util import wwSVG
from WonderPy.util import wwPath


# a few example SVG files.
# all the paths in the chosen file will be drawn.
# see sketcher.md for notes about choosing well-conditioned SVG files.
SVG_FILES = [
    "../assets/svg_files/ww_w.svg",
    "../assets/svg_files/cue_outline.svg",
    "../assets/svg_files/square.svg",
    "../assets/svg_files/triangle.svg",
    "../assets/svg_files/crow.svg",
    "../assets/svg_files/octocat.svg",
]

FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), SVG_FILES[0])

# the SVG will be uniformly scaled and translated to fit snugly in this box.
# this value may be edited freely.
BOUNDING_BOX_WIDTH_CM  = 90
BOUNDING_BOX_HEIGHT_CM = 50

# the linear drive-speed used by the robot.
# this is a reasonably stable value. (ie, edit with care)
DRIVE_SPEED_CM_S       = 15

# the angular drive-speed used by the robot.
# this is a reasonably stable value. (ie, edit with care)
TURN_SPEED_DEG_S       = 20

# this is the number of centimeters per sample point.
# bigger numbers mean fewer way-points.
# this is a reasonably stable value. (ie, edit with care)
UNITS_PER_POINT        =  0.4


class MyClass(object):

    def start(self):
        parser = argparse.ArgumentParser(description='Options.')
        self.setup_argument_parser(parser)
        self.parse_args(parser)
        WonderPy.core.wwMain.start(self)

    def setup_argument_parser(_, parser):
        WonderPy.core.wwBTLEMgr.WWBTLEManager.setup_argument_parser(parser)
        parser.add_argument('--file', metavar='file.svg', type=str,
                                                help='an svg file for the robot to draw')
        parser.add_argument('--box', metavar='cm', type=float, nargs=2,
                                                help='horizontal and vertical centimeters. eg "90 60"')

    def parse_args(self, parser):
        args = parser.parse_args()

        if (args.file is not None):
            global FILENAME
            FILENAME = args.file
        print("attempting to sketch SVG file: %s" % (FILENAME))
        if not os.path.isfile(FILENAME):
            raise Exception("file not found: %s" % (FILENAME))

        if (args.box is not None):
            global BOUNDING_BOX_WIDTH_CM
            global BOUNDING_BOX_HEIGHT_CM
            BOUNDING_BOX_WIDTH_CM  = args.box[0]
            BOUNDING_BOX_HEIGHT_CM = args.box[1]
        print("Bounding box: %0.1fcm wide x %0.1f cm tall (robot at center)" %
              (BOUNDING_BOX_WIDTH_CM, BOUNDING_BOX_HEIGHT_CM))

    def on_connect(self, robot):
        Thread(target=self.async_1, args=(robot,)).start()

    def async_1(self, robot):

        robot.cmds.accessory.do_sketchkit_pen_up()

        while True:
            wwsvg = wwSVG.WWSVG()
            wwsvg.read_file(FILENAME)
            print("loaded '%s'" % FILENAME)

            wwsvg.fit_to_bbox(BOUNDING_BOX_WIDTH_CM * -0.5, BOUNDING_BOX_WIDTH_CM * 0.5,
                              BOUNDING_BOX_HEIGHT_CM * -0.5, BOUNDING_BOX_HEIGHT_CM * 0.5)

            lolop = wwsvg.convert_to_list_of_lists_of_robot_points(UNITS_PER_POINT)

            print("waiting for button..")
            robot.block_until_button_main_press_and_release()

            print("setting global pose to 0, 0, 0")
            self.stage_lights(robot, 0, 1, 0)

            robot.cmds.body.do_pose(0, 0, 0, 0, WWRobotConstants.WWPoseMode.WW_POSE_MODE_SET_GLOBAL)

            self.stage_lights(robot, 1, 1, 0)
            robot.block_until_sensors()
            robot.block_until_sensors()
            robot.block_until_sensors()

            self.stage_lights(robot, 0, 0, 0)
            path_count = 0
            for point_list in lolop.data:
                path_count += 1
                wp = wwPath.WWPath(point_list)
                wp.speed_linear_cm_s   = DRIVE_SPEED_CM_S
                wp.speed_angular_deg_s = TURN_SPEED_DEG_S
                sys.stdout.flush()
                sys.stdout.write("going to start of path %d of %d.\n" % (path_count, len(lolop.data)))
                wp.do_go_to_start(robot)
                sys.stdout.write("starting path %d of %d. %d points.." % (path_count, len(lolop.data), len(point_list)))
                self.stage_lights(robot, 0, 0, 1)
                robot.cmds.accessory.do_sketchkit_pen_down()
                # hm, twice.
                robot.cmds.accessory.do_sketchkit_pen_down()
                self.stage_lights(robot, 0, 1, 1)
                wp.do_continuous_watermark(robot)
                self.stage_lights(robot, 1, 1, 0)
                robot.cmds.accessory.do_sketchkit_pen_up()
                self.stage_lights(robot, 1, 0, 0)
                sys.stdout.write("done\n")

            robot.cmds.body.do_pose(0, 0, 180, 5, WWRobotConstants.WWPoseMode.WW_POSE_MODE_GLOBAL)
            self.stage_lights(robot, 0, 0, 0)

    def stage_lights(self, robot, r, g, b):
        robot.cmds.RGB.stage_ear_left (r, g, b)
        robot.cmds.RGB.stage_ear_right(r, g, b)
        robot.cmds.RGB.stage_top      (r, g, b)


if __name__ == "__main__":
    MyClass().start()
