import ffmpeg
from auto_editor.source.video_params import VideoParams
from auto_editor.utils import Utils


class VideoSource:
    def __init__(self, video_path: str, params: VideoParams):
        self.video = ffmpeg.input(video_path).video
        self.params: VideoParams = params

    def trim(self, start_frame: float, end_frame: float):
        start_sec = Utils.video_frames_to_seconds(start_frame, self.params)
        end_sec = Utils.video_frames_to_seconds(end_frame, self.params)
        v = self.video.filter('trim', start=start_sec, end=end_sec)
        self.video = v

    def set_to_video_params(self, params: VideoParams):
        self.set_resolution(params.resolution[0], params.resolution[1])
        self.set_aspect_ratio(params.aspect_ratio[0], params.aspect_ratio[1])
        self.set_pixel_scale(1, 1)

    def set_resolution(self, width: int, height: int):
        v = self.video.filter('scale', width, height)
        self.video = v

    def set_pixel_scale(self, width: int, height: int):
        v = self.video.filter('setsar', width, height)
        self.video = v

    def set_aspect_ratio(self, width: int, height: int):
        v = self.video.filter('setdar', width, height)
        self.video = v

    def set_fps(self, fps: float):
        v = self.video.filter('fps', fps=fps)
        self.video = v
