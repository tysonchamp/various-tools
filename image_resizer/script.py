import os
import sys
from PIL import Image, ImageOps, ExifTags
from colorthief import ColorThief

# image size 600*400px
# default backgroud color is #000000
# image output format is jpg
# image output quality is 50%
# image should not be streached


def resize_image(image_path, output_path, size=(383, 243), format='JPEG', quality=80):
    image = Image.open(image_path)

    # Get the dominant color of the image
    dominant_color = image.resize((1, 1)).getpixel((0, 0))
    # dominant_color should be white
    # dominant_color = (255, 255, 255)

    # Fix orientation using EXIF data
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # In case the image doesn't have EXIF data
        pass

    # Resize the image without cropping
    image.thumbnail(size, Image.LANCZOS)

    # Create a new image with the desired size and dominant color background
    new_image = Image.new('RGB', size, dominant_color)

    # Calculate the position to paste the image onto the new image
    position = ((new_image.width - image.width) // 2, (new_image.height - image.height) // 2)

    # Paste the image onto the new image
    new_image.paste(image, position)

    # Convert RGBA images to RGB
    if new_image.mode in ('RGBA', 'LA'):
        background = Image.new(new_image.mode[:-1], new_image.size, dominant_color)
        background.paste(new_image, new_image.split()[-1])
        new_image = background

    new_image.save(output_path, format=format, quality=quality)



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
