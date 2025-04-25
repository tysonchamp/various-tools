# create a program to split a video into multiple parts based on user input (seconds)
# Usage: python script.py video.mp4 60
# Output: video_1.mp4, video_2.mp4, video_3.mp4, ...

import os
import sys
from tqdm import tqdm
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def split_video(video_file, duration):
    clip = VideoFileClip(video_file)
    video_duration = int(clip.duration)
    parts = video_duration // duration
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    for i in tqdm(range(parts), desc="Splitting video", unit="part"):
        start_time = i * duration
        end_time = (i + 1) * duration
        if i == parts - 1:  # If it's the last part
            end_time = video_duration  # Set end time to the end of the video
        output_file = f"{output_dir}/{video_file.split('.')[0]}_{i+1}.mp4"
        ffmpeg_extract_subclip(video_file, start_time, end_time, targetname=output_file)

if __name__ == "__main__":
    video_file = sys.argv[1]
    duration = int(sys.argv[2])
    split_video(video_file, duration)