class Speed:
    def __init__(self, straight_speed: float, rotate_speed: float = None):
        self.straight_speed = straight_speed
        # Use rotate speed. If none was given, use the straight speed as the rotate speed
        self.rotate_speed = straight_speed if rotate_speed is None else rotate_speed