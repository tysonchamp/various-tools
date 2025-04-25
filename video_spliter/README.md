
# Video Processing Scripts

This repository contains two Python scripts for video processing:

1. `video_splitter.py`: Splits a video into multiple parts based on a specified duration.
2. `video_cutter.py`: Cuts a video from a specified start time to an end time.

## Requirements

- Python 3
- moviepy library: Install it using pip with `pip install moviepy`
- tqdm library: Install it using pip with `pip install tqdm`

## Usage

### Video Splitter

To use the `video_splitter.py` script, you need to provide two command line arguments:

1. The name (and path, if not in the same directory as the script) of the video file.
2. The duration (in seconds) of each part.

The command to run the script should look like this:


`python video_splitter.py video.mp4 60`

In this example, video.mp4 is the video file and 60 is the duration of each part. The script will split the video into parts of 60 seconds each, and the output files will be named video_1.mp4, video_2.mp4, video_3.mp4, and so on.

### Video Cutter

To use the `video_cutter.py` script, you need to provide three command line arguments:

1. The name (and path, if not in the same directory as the script) of the video file.
2. The start time (in seconds) from where you want to cut the video.
3. The end time (in seconds) where you want to stop cutting the video.

The command to run the script should look like this:

`python video_cutter.py video.mp4 60 120`

In this example, video.mp4 is the video file, 60 is the start time, and 120 is the end time. The script will cut the video from 60 seconds to 120 seconds, and the output file will be named video_cut.mp4.

Progress
While the scripts are running, they will display a progress bar in the terminal showing the percentage of the video that has been processed.

