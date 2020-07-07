import ffmpeg
from auto_editor.source.video_params import VideoParams


class VideoSource:
    def __init__(self, video_path: str, params: VideoParams):
        self.input = ffmpeg.input(video_path)
        self.params: VideoParams = params

        self.set_to_video_params(params)

    def trim(self, start: int, end: int) -> None:
        v = self.input.video.filter('trim', start=start, end=end)
        self.input.video = v

    def set_to_video_params(self, params: VideoParams):
        self.set_resolution(params.resolution[0], params.resolution[1])
        self.set_pixel_scale(1, 1)
        self.set_aspect_ratio(params.aspect_ratio[0], params.aspect_ratio[1])
        self.set_fps(params.fps)

    def set_resolution(self, width: int, height: int):
        v = self.input.video.filter('scale', width, height)
        self.input.video = v

    def set_pixel_scale(self, width: int, height: int):
        v = self.input.video.filter('setsar', width, height)
        self.input.video = v

    def set_aspect_ratio(self, width: int, height: int):
        v = self.input.video.filter('setdar', width, height)
        self.input.video = v

    def set_fps(self, fps: float):
        v = self.input.video.filter('fps', fps=fps)
        self.input.video = v
