import os
from PIL import Image

def compress_images(input_dir):
    output_dir = input_dir + '_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    total_files = 0
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            total_files += 1

    processed_count = 0
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            img = Image.open(os.path.join(input_dir, filename))
            output_filename = os.path.splitext(filename)[0] + '.jpg'
            img.save(os.path.join(output_dir, output_filename), optimize=True, quality=60)

            processed_count += 1
            progress = (processed_count / total_files) * 100
            print(f"Processing... {int(progress)}% complete", end='\r')
    print("\nImages compression completed!")
    print(f"Output files are saved in {output_dir}")

input_directory = input("Enter the directory path: ")
if not os.path.exists(input_directory):
    print(f"Directory '{input_directory}' not found. Please try again.")
else:
    compress_images(input_directory)