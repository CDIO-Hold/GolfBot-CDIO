from Vector import Vector

# Just for typehints
from Driver import Driver
from Collector import Collector


class Robot:
    def __init__(self, driver: Driver, collector: Collector, speaker):
        self.driver = driver
        self.collector = collector
        self.speaker = speaker

        # TODO
        self.size = 10

        # Default values, which can be changed with the setters
        self.position = Vector(0, 0)
        self.facing = 0

    def set_rotation(self, angle: float):
        self.facing = angle % 360

    def set_position(self, position):
        self.position = position

    def set_coordinates(self, x: float, y: float):
        self.position = Vector(x, y)

    def turn_to(self, target_degrees: float):
        print("Turning to:", target_degrees)
        turn_angle = target_degrees - self.facing
        self.driver.turn(turn_angle)
        self.facing = target_degrees

    def drive_to(self, target: Vector):
        drive_vector = Vector.from_points(self.position, target)
        print("Drive vector: {} ({} degrees)".format(drive_vector, drive_vector.angle))

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

    def speak(self, phrase: str, volume: int = 100):
        self.speaker.speak(phrase, volume=volume, play_type=1)

    def follow_path(self, path: list):
        for position in path:
            self.drive_to(position)
