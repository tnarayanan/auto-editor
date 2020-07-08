import numpy as np
import ffmpeg
from typing import List
from auto_editor.source.video_source import VideoSource
from auto_editor.source.video_params import VideoParams
from auto_editor.source.audio_source import AudioSource
from auto_editor.timeline.clip_adjustment import ClipAdjustment
from auto_editor.utils import Utils

class Timeline:
    def __init__(self, video_inputs: List[VideoSource], video_params: VideoParams, audio_input: AudioSource, beat_frames: np.ndarray):
        self.video_inputs = video_inputs
        self.video_params = video_params
        self.audio_input = audio_input
        self.beat_frames = beat_frames

    def split_clips(self) -> List[ClipAdjustment]:
        adjustments = []

        for i in range(1, len(self.beat_frames)):
            start = 0
            end = int(self.beat_frames[i] - self.beat_frames[i - 1])
            adjustments.append(ClipAdjustment(trim_start=start, trim_end=end))

        return adjustments

    def assemble(self, clip_adjustments: List[ClipAdjustment], output_file_name: str):
        joined = None

        for i in range(len(self.video_inputs)):
            print("trimming ", i, " at ", clip_adjustments[i].trim_start, " to ", clip_adjustments[i].trim_end)
            self.video_inputs[i].trim(start_frame=clip_adjustments[i].trim_start, end_frame=clip_adjustments[i].trim_end)
            self.video_inputs[i].set_to_video_params(self.video_params)

            if joined is None:
                joined = ffmpeg.concat(self.video_inputs[i].video).node
            else:
                joined = ffmpeg.concat(joined[0], self.video_inputs[i].video).node

        self.audio_input.trim(0, Utils.video_frames_to_sample(self.beat_frames[-1], self.audio_input.params, self.video_params))

        return ffmpeg.output(joined[0], self.audio_input.audio, output_file_name)