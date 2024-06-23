from Circle import Circle


class Driver:
    def __init__(self,
                 move_steering,
                 straight_speed,
                 turn_speed,
                 wheel: Circle,
                 turn_circle: Circle):
        self.steering = move_steering
        self.straight_speed = straight_speed
        self.turn_speed = turn_speed
        self.wheel = wheel
        self.turn_circle = turn_circle

    def turn(self, degrees):
        print("Turning:", degrees)
        if degrees < 0:
            self.turn_right(degrees)
        else:
            self.turn_left(degrees)

    def turn_left(self, degrees):
        print("Turning left")
        # self._turn_with_gyro(angle, "left")
        self._turn_with_geometry(degrees, "left")

    def turn_right(self, degrees):
        print("Turning right")
        # self._turn_with_gyro(angle, "right")
        self._turn_with_geometry(degrees, "right")

    def _turn_with_gyro(self, degrees, direction: str):
        if direction == "right":
            self.steering.turn_right(self.turn_speed, degrees)
        else:
            self.steering.turn_left(self.turn_speed, degrees)

    def _turn_with_geometry(self, degrees, direction: str):
        turn_percent = degrees / 360.0

        wheel_travel_distance = self.turn_circle.circumference * turn_percent
        wheel_rotations = wheel_travel_distance / self.wheel.circumference

        if direction == "left":
            left_speed = -self.turn_speed
        else:
            left_speed = self.turn_speed
        right_speed = left_speed * -1

        self.steering.on_for_rotations(
            left_speed,
            right_speed,
            wheel_rotations
        )

    def forward(self, distance: float):
        rotations = distance / self.wheel.circumference

        self.steering.on_for_rotations(
            self.straight_speed,
            self.straight_speed,
            rotations
        )

    def backward(self, distance: float):
        rotations = distance / self.wheel.circumference

        self.steering.on_for_rotations(
            -self.straight_speed,
            -self.straight_speed,
            rotations
        )

    def stop(self):
        self.steering.off()
