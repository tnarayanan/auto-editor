class VideoParams:
    def __init__(self, resolution: tuple, aspect_ratio: tuple, fps: float):
        self.resolution: tuple = resolution
        self.aspect_ratio: tuple = aspect_ratio
        self.fps: float = fps
