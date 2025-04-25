import os
import argparse
from PIL import Image
from tqdm import tqdm
import re
import csscompressor
import shutil
from bs4 import BeautifulSoup

def convert_to_webp(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files_to_convert = []
    files_to_copy = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                files_to_convert.append((root, file))
            else:
                files_to_copy.append((root, file))

    with tqdm(total=len(files_to_convert), desc="Converting images", unit="file") as pbar:
        for root, file in files_to_convert:
            image_path = os.path.join(root, file)
            img = Image.open(image_path)
            relative_path = os.path.relpath(root, input_dir)
            new_dir = os.path.join(output_dir, relative_path)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            webp_path = os.path.join(new_dir, os.path.splitext(file)[0] + '.webp')
            img.save(webp_path, 'webp')
            pbar.update()

    with tqdm(total=len(files_to_copy), desc="Copying other files", unit="file") as pbar:
        for root, file in files_to_copy:
            src_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, input_dir)
            new_dir = os.path.join(output_dir, relative_path)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            dst_path = os.path.join(new_dir, file)
            shutil.copy2(src_path, dst_path)
            pbar.update()


def update_css(input_dir, output_dir):
    css_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.css'):
                css_files.append((root, file))

    with tqdm(total=len(css_files), desc="Updating CSS files", unit="file") as pbar:
        for root, file in css_files:
            css_path = os.path.join(root, file)
            with open(css_path, 'r') as f:
                css_content = f.read()

            # replace .png, .jpg, .jpeg with .webp
            css_content = re.sub(r'\.(png|jpg|jpeg)', '.webp', css_content, flags=re.IGNORECASE)

            # minify CSS
            css_content = csscompressor.compress(css_content)

            relative_path = os.path.relpath(root, input_dir)
            new_dir = os.path.join(output_dir, relative_path)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            new_css_path = os.path.join(new_dir, file)

            with open(new_css_path, 'w') as f:
                f.write(css_content)

            pbar.update()


def update_html(input_dir, output_dir):
    html_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.html'):
                html_files.append((root, file))

    with tqdm(total=len(html_files), desc="Updating HTML files", unit="file") as pbar:
        for root, file in html_files:
            html_path = os.path.join(root, file)
            with open(html_path, 'r') as f:
                html_content = f.read()

            # replace .png, .jpg, .jpeg with .webp
            html_content = re.sub(r'\.(png|jpg|jpeg)', '.webp', html_content, flags=re.IGNORECASE)

            # update img alt tag value to webpage title
            soup = BeautifulSoup(html_content, 'html.parser')
            title_text = soup.title.string if soup.title else ''
            for img in soup.find_all('img'):
                img['alt'] = title_text

            html_content = str(soup)

            relative_path = os.path.relpath(root, input_dir)
            new_dir = os.path.join(output_dir, relative_path)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            new_html_path = os.path.join(new_dir, file)

            with open(new_html_path, 'w') as f:
                f.write(html_content)

            pbar.update()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert images to WebP format.')
    parser.add_argument('input_dir', type=str, help='The input directory with images.')
    args = parser.parse_args()

    output_dir = args.input_dir + '_output'
    convert_to_webp(args.input_dir, output_dir)
    update_css(args.input_dir, output_dir)
    update_html(args.input_dir, output_dir)