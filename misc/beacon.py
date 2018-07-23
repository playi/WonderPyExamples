import sys
import WonderPy.core.wwMain
from WonderPy.core.wwConstants import WWRobotConstants


class MyClass(object):

    def on_connect(self, robot):
        if not robot.has_ability(WWRobotConstants.WWRobotAbilities.BEACON_SENSE, True):
            exit(1)

        # a rolling number of sensor-events from the robot we'll analyze.
        # smaller values here lead to less latency in reporting "no robot", but also more false-negatives.
        robot.sensors.beacon.data_window_size = 25

    def on_sensors(self, robot):
        b = robot.sensors.beacon

        # filtered value is the 'mode' of the data window.
        nl_filtered = WWRobotConstants.RobotTypeNames[b.robot_type_left ] if b.robot_type_left  else 'None'
        nr_filtered = WWRobotConstants.RobotTypeNames[b.robot_type_right] if b.robot_type_right else 'None'

        # filtered value is the most recent data (likely None)
        nl_raw      = WWRobotConstants.RobotTypeNames[b.robot_type_left_raw ] if b.robot_type_left_raw   else 'None'
        nr_raw      = WWRobotConstants.RobotTypeNames[b.robot_type_right_raw] if b.robot_type_right_raw  else 'None'
        sys.stdout.write('\rLeft: %15s (%15s)   Right: %15s (%15s)' % (nl_filtered, nl_raw, nr_filtered, nr_raw))
        sys.stdout.flush()


if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
