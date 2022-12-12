class Robot():
    import sys
    from time import sleep
    from xarm.wrapper import XArmAPI
    def __init__(self, ip='192.168.1.207', speed=500):
        print('Robot class __init__()')

        self.arm = self.XArmAPI(ip)
        self.global_speed = speed
        self.plane = 'top'
        self.locations = {
            # [x, y, z, roll, pitch, yaw]
            'frontPrinter': [50, 400, 50, -90, 90, 90],
            'topPrinter': [-220, 465, 235, -180, 0, 0],
            'dropOff': [5, 330, 10, 0, 0, 0]
        }
        self.reset()
        self.arm.set_gripper_enable(True)


    def move2target(self, x, y, z):
        self.arm.set_position(x=x, y=y, z=z, relative=False, speed=self.global_speed/3, wait=True)

    def grab(self, startPos=800, endPos=150, angle=0):
        self.arm.set_servo_angle(servo_id=6, angle=angle, relative=True, is_radian=False, speed=50, wait=True)
        self.arm.set_position(z=-50, relative=True, speed=50, wait=True)
        self.arm.set_gripper_position(endPos, wait=True)

    def dropOff(self):
        '''
        location_values = self.locations['dropOff']
        [x_i, y_i, z_i, roll_i, pitch_i, yaw_i] = location_values

        self.arm.set_position(x=x_i, y=y_i, z=z_i, roll=roll_i, pitch=pitch_i, yaw=yaw_i, speed=self.global_speed,
                              wait=True)
        '''
        location_values = self.locations['dropOff']
        [x_i, y_i, z_i, roll_i, pitch_i, yaw_i] = location_values

        self.arm.set_position(z=+100, relative=True, speed=self.global_speed/3, wait=True)
        self.arm.set_position(x=x_i, y=y_i, z=z_i, yaw=yaw_i, speed=self.global_speed/3,
                              wait=True)
        self.arm.set_gripper_position(800, wait=False)
        self.arm.set_position(z=+100, relative=True, speed=self.global_speed/3, wait=True)

    def view_frontPrinter(self):
        location_values = self.locations['frontPrinter']
        [x_i, y_i, z_i, roll_i, pitch_i, yaw_i] = location_values
        self.arm.set_position(x=x_i, y=y_i, z=z_i, roll=roll_i, pitch=pitch_i, yaw=yaw_i, speed=self.global_speed,
                              wait=True)

    def view_topPrinter(self):
        location_values = self.locations['topPrinter']
        [x_i, y_i, z_i, roll_i, pitch_i, yaw_i] = location_values
        self.arm.set_position(y=y_i, relative=True, speed=self.global_speed, wait=True)
        self.arm.set_position(z=z_i, relative=True, speed=self.global_speed, wait=True)
        self.arm.set_position(x=x_i, y=y_i, z=z_i, roll=roll_i, pitch=pitch_i, yaw=yaw_i, speed=self.global_speed,
                              wait=True)

    def wait(self, time=10):
        self.sleep(time)

    def home(self, speed=100):
        self.arm.move_gohome(speed=speed)

    def reset(self):
        self.arm.clean_warn()
        self.arm.clean_gripper_error()
        self.arm.clean_error()
        self.sleep(1)
        self.arm.reset()

    def disconnect(self):
        self.arm.disconnect()


if __name__ == '__main__':
    obj = Robot()
