class Driver:
    def __init__(self, left_motor, right_motor, is_moving: bool =False):
        self.leftMotor = left_motor
        self.rightMotor = right_motor
        self.isMoving = is_moving

    def drive(self):
        self.isMoving = True

    # TODO

    def stop(self):
        self.isMoving = False

    # TODO

    def turn(self):
        self.isMoving = True
        
    # TODO
