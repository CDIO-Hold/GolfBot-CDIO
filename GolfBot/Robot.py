import rpyc
from GolfBot.Basics import ConnectionInfo, Circle, DriveSpeed, Vector, Angle, degrees
from GolfBot import Collector, Driver


class Robot:
    def __init__(self,
                 connection_info: ConnectionInfo,
                 drive_speed: DriveSpeed,
                 collection_speed: float,
                 starting_rotation=None,
                 starting_position=None
                 ):
        self.connection = rpyc.classic.connect(connection_info.ip_address, connection_info.port)

        ev3_motors = self.connection.modules['ev3dev2.motor']

        left_wheel = ev3_motors.OUTPUT_B
        right_wheel = ev3_motors.OUTPUT_C
        left_conveyor = ev3_motors.OUTPUT_D
        right_conveyor = ev3_motors.OUTPUT_A

        drive_steering = ev3_motors.MoveSteering(left_wheel, right_wheel, motor_class=ev3_motors.LargeMotor)

        wheel = Circle(diameter=68.8)
        wheel_distance = 111
        turn_circle = Circle(diameter=wheel_distance)
        self.driver = Driver(drive_steering, drive_speed, wheel, turn_circle)

        conveyor_steering = ev3_motors.MoveSteering(left_conveyor, right_conveyor, motor_class=ev3_motors.MediumMotor)
        self.collector = Collector(conveyor_steering, collection_speed)

        # TODO
        self.size = 10

        if type(starting_rotation) is Angle:
            self.facing = starting_rotation.with_unit(degrees)
        else:
            self.facing = Angle(90, degrees)

        if type(starting_position) is Vector:
            self.position = starting_position.__copy__()
        elif type(starting_position) is tuple and len(starting_position) == 2:
            self.position = Vector.from_tuple(starting_position)
        else:
            self.position = Vector(0, 0)

    def set_rotation(self, angle: Angle):
        self.facing = angle

    def set_coordinates(self, x: float, y: float):
        self.position = Vector(x, y)

    def turn_to(self, target: Angle):
        print("Turning to:", target.with_unit(degrees))
        turn_angle = target - self.facing
        self.driver.turn(turn_angle)
        self.facing = target.with_unit(degrees)

    def drive_to(self, target: Vector):
        drive_vector = Vector.from_points(self.position, target)
        # print("Drive vector:", drive_vector, drive_vector.angle.with_unit(degrees))

        if drive_vector.length == 0:
            print("Skipping driving")
            return

        # Perform the actions
        self.turn_to(drive_vector.angle)
        self.driver.forward(drive_vector.length)

        # Update state
        self.position.x += drive_vector.x
        self.position.y += drive_vector.y

    def reverse_to(self, target: Vector):
        drive_vector = Vector.from_points(self.position, target)
        # print("Drive vector:", drive_vector, drive_vector.angle.with_unit(degrees))

        if drive_vector.length == 0:
            print("Skipping driving")
            return

        # Perform the actions
        self.turn_to(drive_vector.angle * -1)
        self.driver.backward(drive_vector.length)

        # Update state
        self.position.x += drive_vector.x
        self.position.y += drive_vector.y

    def follow_path(self, path: list):
        for position in path:
            self.drive_to(position)
