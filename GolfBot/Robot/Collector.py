class Collector:
    def __init__(self, collection_steering, collection_speed: float):
        self.steering = collection_steering
        self.speed = collection_speed
        self.loading = False
        self.unloading = False

    def start_loading(self):
        if self.loading:
            return
        self.steering.on(100, self.speed)
        self.loading = True
        self.unloading = False

    def start_unloading(self):
        if self.unloading:
            return
        self.steering.on(-100, self.speed)
        self.loading = False
        self.unloading = True

    def stop(self):
        if not self.loading and not self.unloading:
            return
        self.steering.stop()
        self.loading = False
        self.unloading = False
