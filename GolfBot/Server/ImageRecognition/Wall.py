from GolfBot.Server.Basics import Box, Vector


class Wall(Box):
    def __init__(self, name, start_position: Vector, end_position: Vector):
        self.name = name
        self.is_left_wall = False
        self.is_right_wall = False
        super().__init__(start_position, end_position)

    @property
    def is_goal_wall(self):
        return self.is_left_wall or self.is_right_wall
