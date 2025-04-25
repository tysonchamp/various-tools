import csv
import requests
import os

def download_thumbnails(input_csv, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the input CSV file
    with open(input_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for index, row in enumerate(reader, start=1):
            thumbnail_url = row[0]
            # Renaming the file to a simple numeric sequence
            filename = f"{index}.webp"
            output_path = os.path.join(output_dir, filename)

            # Downloading the thumbnail
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                with open(output_path, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Downloaded {filename}")
            else:
                print(f"Failed to download {filename}")

# Replace 'youtube-imgs.csv' with your input file name
download_thumbnails('youtube-imgs.csv', 'downloaded_thumbnails')