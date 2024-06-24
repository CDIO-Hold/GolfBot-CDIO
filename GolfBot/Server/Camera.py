from cv2 import VideoCapture


class Image:
    def __init__(self, data, width: int, height: int):
        self.data = data
        self.width = width
        self.height = height

    @classmethod
    def empty(cls):
        return cls(data=None, width=0, height=0)


class Camera:
    def __init__(self, camera_index: int = 1, image_dimensions: (int, int) = (1280, 720)):
        self.capture = VideoCapture(camera_index)
        self.image_width, self.image_height = image_dimensions
        self.capture.set(3, self.image_width)
        self.capture.set(4, self.image_height)

    def take_picture(self) -> Image:
        success, image_data = self.capture.read()
        if not success:
            return Image.empty()
        else:
            return Image(image_data, self.image_width, self.image_height)
