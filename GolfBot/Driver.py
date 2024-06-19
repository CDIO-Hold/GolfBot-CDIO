from Basics import Circle, DriveSpeed, Angle, degrees, percent


class Driver:
    def __init__(self,
                 move_tank,
                 speed: DriveSpeed,
                 wheel: Circle,
                 turn_circle: Circle):
        self.tank = move_tank
        self.speed = speed
        self.wheel = wheel
        self.turn_circle = turn_circle

    def turn(self, angle: Angle):
        print("Turning:", angle)

        degree_value = abs(angle.get_value(signed=True, unit=degrees))
        short_angle = Angle(degree_value, degrees)

        if angle.signed_value < 0:
            self.turn_right(short_angle)
        else:
            self.turn_left(short_angle)

    def turn_left(self, angle: Angle):
        print("Turning left")
        # self._turn_with_gyro(angle, "left")
        self._turn_with_geometry(angle, "left")

    def turn_right(self, angle: Angle):
        print("Turning right")
        # self._turn_with_gyro(angle, "right")
        self._turn_with_geometry(angle, "right")

    def _turn_with_gyro(self, angle: Angle, direction: str):
        if direction == "right":
            self.tank.turn_right(self.speed.rotate_speed, angle.get_value(signed=False, unit=degrees))
        else:
            self.tank.turn_left(self.speed.rotate_speed, angle.get_value(signed=False, unit=degrees))

    def _turn_with_geometry(self, angle: Angle, direction: str):
        turn_percent = angle.get_value(signed=False, unit=percent) / 100.0

        wheel_travel_distance = self.turn_circle.circumference * turn_percent
        wheel_rotations = wheel_travel_distance / self.wheel.circumference

        if direction == "left":
            left_speed = -self.speed.rotate_speed
        else:
            left_speed = self.speed.rotate_speed
        right_speed = left_speed * -1

        self.tank.on_for_rotations(
            left_speed,
            right_speed,
            wheel_rotations
        )

    def forward(self, distance: float):
        rotations = distance / self.wheel.circumference

        self.tank.on_for_rotations(
            self.speed.straight_speed,
            self.speed.straight_speed,
            rotations
        )

    def backward(self, distance: float):
        rotations = distance / self.wheel.circumference

        self.tank.on_for_rotations(
            -self.speed.straight_speed,
            -self.speed.straight_speed,
            rotations
        )

    def stop(self):
        self.tank.off()
