class Collector:
    def __init__(self, collection_steering, collection_speed: float):
        self.steering = collection_steering
        self.speed = collection_speed

    def start_loading(self):
        self.steering.on(100, self.speed)

    def start_unloading(self):
        self.steering.on(-100, self.speed)

    def stop(self):
        self.steering.stop()
