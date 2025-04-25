import os
import sys
import random
from moviepy.editor import concatenate_videoclips, VideoFileClip, ImageClip, CompositeVideoClip

# Function to join videos in a directory with a logo and banner
def join_videos(directory, logo_file, banner_file):
    # Get a sorted list of all video files in the directory
    video_files = sorted([f for f in os.listdir(directory) if f.endswith('.mp4')])

    # Load the logo and banner images
    logo = ImageClip(logo_file).set_duration(10).resize(height=50) # adjust duration as needed
    banner = ImageClip(banner_file).set_duration(10).resize(width=720) # adjust duration and width as needed

    # Load and process each video
    clips = []
    for video_file in video_files:
        clip = VideoFileClip(os.path.join(directory, video_file))
        # Add the logo and banner to the video
        video = CompositeVideoClip([clip, logo.set_position(("left","top")), banner.set_position(("center","bottom"))])
        # Add a random duration crossfade transition
        video = video.crossfadein(random.randint(1, 3))
        clips.append(video)

    # Concatenate all videos
    final_clip = concatenate_videoclips(clips)

    # Write the result to a file
    final_clip.write_videofile("output.mp4")


# Usage: python video_joiner.py videos_dir logo.png banner.png
if __name__ == "__main__":
    directory = sys.argv[1]
    logo_file = sys.argv[2]
    banner_file = sys.argv[3]
    join_videos(directory, logo_file, banner_file)