import sys
import WonderPy.core.wwMain


class MyClass(object):

    def on_sensors(self, robot):
        """
        Print the raw accelerometer data along each axis.
        Also the convenience rotation data.
        See the comments in wwSensorAccelerometer.py for details.
        """
        sensor = robot.sensors.accelerometer
        things = [
            ("x"   , sensor.x),
            ("y"   , sensor.y),
            ("z"   , sensor.z),
            ("z_yz", sensor.degrees_z_yz()),
            ("y_yz", sensor.degrees_y_yz()),
            ("z_xz", sensor.degrees_z_xz()),
            ("x_xz", sensor.degrees_x_xz()),
            ("x_xy", sensor.degrees_x_xy()),
            ("y_xy", sensor.degrees_y_xy()),
        ]
        s = ""
        for thing in things:
            s += "%s: %7.2f  " % (thing[0], thing[1])
        sys.stdout.write('\r%s' % (s))
        sys.stdout.flush()


if __name__ == "__main__":
    WonderPy.core.wwMain.start(MyClass())
