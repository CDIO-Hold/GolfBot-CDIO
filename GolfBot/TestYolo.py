import unittest
from unittest.mock import patch, MagicMock
from ultralytics import YOLO
from GolfBot.Robot import Robot
from GolfBot.Server.Basics import CardinalDirection, Egg, Ball, Wall
from GolfBot.Server.ImageRecognition.YOLO import Yolo


class TestYolo(unittest.TestCase):

    @patch('cv2.VideoCapture')
    @patch('ultralytics.YOLO')
    def setUp(self, MockYOLO, MockVideoCapture):
        self.mock_video_capture = MockVideoCapture.return_value
        self.mock_video_capture.read.return_value = (True, MagicMock())

        self.yolo = Yolo()
        self.yolo.model = YOLO('Server/YOLO_FINAL_MODEL.pt')
        self.robot = self.yolo.robot

    def test_detect_ball(self):
        ball = self.yolo.detect_ball('orange-ball', 0, 10, 0, 10)
        self.assertIsInstance(ball, Ball)
        self.assertEqual(ball.name, 'orange-ball')
        self.assertNotEqual(ball.name, 'white-ball')
        self.assertEqual(ball.position.x, 5)
        self.assertEqual(ball.position.y, 5)

    def test_detect_wall(self):
        wall = self.yolo.detect_wall('wall', 5, 10, 10, 0)
        self.assertIsInstance(wall, Wall)
        self.assertEqual(wall.name, 'wall')
        self.assertEqual(wall.start_position.x, 5)
        self.assertEqual(wall.start_position.y, 10)
        self.assertEqual(wall.end_position.x, 10)
        self.assertEqual(wall.end_position.y, 0)
        self.assertTrue(wall.is_left_wall, True)
        self.assertFalse(wall.is_right_wall, False)

    def test_detect_robot(self):
        self.robot = self.yolo.detect_robot(self.robot, 5, 10, 5, 10)
        self.assertIsInstance(self.robot, Robot)
        self.assertEqual(self.robot.facing, CardinalDirection.NORTH)
        self.assertEqual(self.robot.position.top_left.x, 5)
        self.assertEqual(self.robot.position.top_left.y, 5)
        self.assertEqual(self.robot.position.bottom_right.x, 10)
        self.assertEqual(self.robot.position.bottom_right.y, 10)

    def test_detect_robot_facing_north(self):
        #Setup:
        self.robot = self.yolo.detect_robot(self.robot, 5, 10, 5, 10)
        self.assertIsInstance(self.robot, Robot)
        self.assertEqual(self.robot.facing, CardinalDirection.NORTH)
        self.assertEqual(self.robot.position.top_left.x, 5)
        self.assertEqual(self.robot.position.top_left.y, 5)
        self.assertEqual(self.robot.position.bottom_right.x, 10)
        self.assertEqual(self.robot.position.bottom_right.y, 10)

        #direction
        self.robot = self.yolo.detect_robot_front(self.robot, 5, 10, 10, 15)
        self.assertIsInstance(self.robot, Robot)
        self.assertEqual(self.robot.facing, CardinalDirection.NORTH)

    def test_detect_robot_facing_east(self):
        # Setup:
        self.robot = self.yolo.detect_robot(self.robot, 5, 10, 5, 10)
        self.assertIsInstance(self.robot, Robot)
        self.assertEqual(self.robot.facing, CardinalDirection.NORTH)
        self.assertEqual(self.robot.position.top_left.x, 5)
        self.assertEqual(self.robot.position.top_left.y, 5)
        self.assertEqual(self.robot.position.bottom_right.x, 10)
        self.assertEqual(self.robot.position.bottom_right.y, 10)

        # direction
        self.robot = self.yolo.detect_robot_front(self.robot, 10, 15, 5, 10)
        self.assertIsInstance(self.robot, Robot)
        self.assertEqual(self.robot.facing, CardinalDirection.EAST)

    def test_detect_egg(self):
        egg = self.yolo.detect_egg('egg', 0, 5, 5, 10)
        self.assertIsInstance(egg, Egg)
        self.assertEqual(egg.name, 'egg')
        self.assertEqual(egg.bounding_box.x, 2.5)
        self.assertEqual(egg.bounding_box.y, 7.5)

    #def test_goal_on_wall(self):
