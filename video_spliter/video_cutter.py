# uses: python video_cutter.py video.mp4 <start second> <end second>

import sys
from tqdm import tqdm
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

# Function to cut a video from a start time to an end time
def cut_video(video_file, start_time, end_time):
    # Load the video file
    clip = VideoFileClip(video_file)
    
    # Define the output file name
    output_file = f"{video_file.split('.')[0]}_cut.mp4"
    
    # Create a progress bar with tqdm
    with tqdm(total=end_time-start_time, desc="Cutting video", unit="sec") as pbar:
        # Update the progress bar for each second in the range
        for i in range(start_time, end_time):
            pbar.update()
        
        # Cut the video from start_time to end_time and save it as output_file
        ffmpeg_extract_subclip(video_file, start_time, end_time, targetname=output_file)

# Main function
if __name__ == "__main__":
    # Get the video file name from command line arguments
    video_file = sys.argv[1]
    
    # Get the start time from command line arguments
    start_time = int(sys.argv[2])
    
    # Get the end time from command line arguments
    end_time = int(sys.argv[3])
    
    # Call the cut_video function
    cut_video(video_file, start_time, end_time)