import numpy as np


class Utils:
    @staticmethod
    def sample_to_video_frames(inp, audio_params, video_params):
        return np.divide(inp, (audio_params.sampling_rate / video_params.fps))

    @staticmethod
    def video_frames_to_sample(inp, audio_params, video_params):
        return np.multiply(inp, (audio_params.sampling_rate / video_params.fps))

    @staticmethod
    def video_frames_to_seconds(inp, video_params):
        return np.divide(inp, video_params.fps)