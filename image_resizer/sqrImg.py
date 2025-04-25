import os
import sys
from PIL import Image, ImageOps, ExifTags
from colorthief import ColorThief

# image size 600*400px
# default backgroud color is #000000
# image output format is jpg
# image output quality is 50%
# image should not be streached


def resize_image(image_path, output_path, size=(200, 200), format='JPEG', quality=100):
    image = Image.open(image_path)

    # Get dimensions
    width, height = image.size

    # Determine the aspect ratio
    aspect = width / float(height)

    # Calculate the new dimensions
    ideal_width, ideal_height = size
    ideal_aspect = ideal_width / float(ideal_height)

    if aspect > ideal_aspect:
        # Then crop the left and right edges:
        new_width = int(ideal_aspect * height)
        offset = (width - new_width) / 2
        resize = (offset, 0, width - offset, height)
    else:
        # ... crop the top and bottom:
        new_height = int(width / ideal_aspect)
        offset = (height - new_height) / 2
        resize = (0, offset, width, height - offset)

    # Crop the image to a square (if necessary)
    cropped = image.crop(resize)

    # Resize the image
    thumbnail = cropped.resize(size, Image.LANCZOS)

    thumbnail.save(output_path, format=format, quality=quality)



# Usage: python script.py <input_folder> <output_folder>
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python script.py <input_folder> <output_folder>')
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.JPG'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resize_image(input_path, output_path)
            print(f'{filename} resized successfully')
