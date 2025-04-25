import csv
from collections import OrderedDict

def remove_duplicates(input_csv, output_csv):
    # Using OrderedDict to preserve the order of insertion and remove duplicates
    videos = OrderedDict()

    # Reading the input CSV file
    with open(input_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            url, title = row
            videos[url] = title  # This will overwrite duplicate URLs

    # Writing to the output CSV file
    with open(output_csv, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for url, title in videos.items():
            writer.writerow([url, title])

# Replace 'youtube.csv' with your input file name and 'youtube_unique.csv' with your desired output file name
remove_duplicates('youtube.csv', 'youtube_unique.csv')