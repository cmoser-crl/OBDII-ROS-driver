import argparse
import obd
import rclpy
from rclpy.node import Node
from rclpy.exceptions import ROSInterruptException
from std_msgs.msg import Float64


class OBD_Node(Node):
    def __init__(self, port):
        super().__init__('OBDII_ROS_driver')

        connection = obd.Async(portstr=port)
        connection.watch(obd.commands.RPM, callback=self.new_rpm)
        connection.watch(obd.commands.SPEED, callback=self.new_speed)
        connection.watch(obd.commands.THROTTLE_POS, callback=self.new_throt)
        connection.watch(obd.commands.RELATIVE_THROTTLE_POS, callback=self.new_relthrot)
        connection.watch(obd.commands.ACCELERATOR_POS_D, callback=self.new_accd)
        connection.watch(obd.commands.ACCELERATOR_POS_E, callback=self.new_acce)
        connection.watch(obd.commands.THROTTLE_ACTUATOR, callback=self.new_throtact)
        connection.watch(obd.commands.ENGINE_LOAD, callback=self.new_engine)
        connection.watch(obd.commands.BAROMETRIC_PRESSURE, callback=self.new_pressure)
        connection.watch(obd.commands.FUEL_STATUS, callback=self.new_fuel)

        self.connection = connection
        self.pubrpm = self.create_publisher(Float64, 'rpm', 10)
        self.pubspeed = self.create_publisher(Float64, 'speed', 10)
        self.pubthrottle = self.create_publisher(Float64, 'throttle', 10)
        self.pubrelthrot = self.create_publisher(Float64, 'rel_throttle', 10)
        self.pubaccd = self.create_publisher(Float64, 'acc_pedal_d',  10)
        self.pubacce = self.create_publisher(Float64, 'acc_pedal_e', 10)
        self.pubthrotact = self.create_publisher(Float64, 'throttle_act', 10)
        self.pubengine = self.create_publisher(Float64, 'engine_load', 10)
        self.pubpressure = self.create_publisher(Float64, 'pressure', 10)
        self.pubfuel = self.create_publisher(Float64, 'fuel', 10)

    def __enter__(self):
        self.connection.start()
        return self

    def __exit__(self):
        self.connection.stop()

    def new_rpm(self, v):
        value = float(str(v).split(':')[-1].split(' ')[0])
        self.pubrpm.publish(value)

    def new_speed(self, v):
        value = float(str(v).split(':')[-1].split(' ')[0])
        self.pubspeed.publish(value)

    def new_relthrot(self, v):
        value = float(str(v).split(':')[-1].split(' ')[0])
        self.pubrelthrot.publish(value)

    def new_throt(self, v):
        value = float(str(v).split(':')[-1].split(' ')[0])
        self.pubthrottle.publish(value)

    def new_accd(self, v):
        value = float(str(v).split(':')[-1].split(' ')[0])
        self.pubaccd.publish(value)

    def new_acce(self, v):
        value = float(str(v).split(':')[-1].split(' ')[0])
        self.pubacce.publish(value)

    def new_throtact(self, v):
        value = float(str(v).split(':')[-1].split(' ')[0])
        self.pubthrotact.publish(value)

    def new_engine(self, v):
        value = float(str(v).split(':')[-1].split(' ')[0])
        self.pubengine.publish(value)

    def new_pressure(self, v):
        value = float(str(v).split(':')[-1].split(' ')[0])
        self.pubpressure.publish(value)

    def new_fuel(self, v):
        value = float(str(v).split(':')[-1].split(' ')[0])
        self.pubfuel.publish(value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='obdii create_publisher')
    parser.add_argument('--port', default='/dev/ttyUSB0')
    args = parser.parse_args()

    try:
        rclpy.init()

        with OBD_Node(args.port) as node:
            rclpy.spin(node)

        rclpy.shutdown()
    except ROSInterruptException:
        pass
