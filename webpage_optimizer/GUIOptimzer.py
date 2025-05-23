import tkinter as tk
from tkinter import font
from tkinter import filedialog, ttk
import os
import argparse
from PIL import Image
from tqdm import tqdm
import re
import csscompressor
import shutil
from bs4 import BeautifulSoup


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.grid_columnconfigure(1, weight=1)  # Make the second column expandable
        self.root.geometry('500x400')  # Set default window size
        self.root.configure(bg='white')  # Set background color

        self.input_dir = ''
        self.output_dir = ''
        self.combined_css_file_list = []  # List to store combined CSS files
        self.list_of_css_for_html_header = [] # list of css files which has been combined and will be removed from html header

        # Create a canvas
        self.canvas = tk.Canvas(root, width=200, height=50, bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Create a button
        self.bold_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.button = tk.Button(self.canvas, text="Select Directory", bg='blue', fg='white', font=self.bold_font, command=self.select_directory)
        self.button.pack()

        # Bind mouse events for hover effect
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)        

        tk.Label(root, text="Optimizing Image Files:", bg='lightgrey', anchor='e').grid(row=1, column=0, sticky='e')  # Align the label to the right
        self.progress1 = ttk.Progressbar(root, length=100, mode='determinate')
        self.progress1.grid(row=1, column=1, sticky='we')  # Make the progress bar full width

        tk.Label(root, text="Combining CSS Files:", bg='lightgrey', anchor='e').grid(row=2, column=0, sticky='e')  # Align the label to the right
        self.progress2 = ttk.Progressbar(root, length=100, mode='determinate')
        self.progress2.grid(row=2, column=1, sticky='we')  # Make the progress bar full width

        tk.Label(root, text="Optimizing CSS Files:", bg='lightgrey', anchor='e').grid(row=3, column=0, sticky='e')  # Align the label to the right
        self.progress3 = ttk.Progressbar(root, length=100, mode='determinate')
        self.progress3.grid(row=3, column=1, sticky='we')  # Make the progress bar full width

        tk.Label(root, text="Updating HTML Files:", bg='lightgrey', anchor='e').grid(row=4, column=0, sticky='e')  # Align the label to the right
        self.progress4 = ttk.Progressbar(root, length=100, mode='determinate')
        self.progress4.grid(row=4, column=1, sticky='we')  # Make the progress bar full width


    def on_enter(self, event):
        self.button.config(bg='dark blue')


    def on_leave(self, event):
        self.button.config(bg='blue')


    def select_directory(self):
        self.input_dir = filedialog.askdirectory(title='Select the input directory with images')
        if self.input_dir:
            self.output_dir = self.input_dir + '_output'
            self.convert_to_webp()
            self.combine_css()
            self.update_css()
            self.update_html()
            # self.select_button['state'] = 'normal'
        else:
            print("No directory selected.")

    # Convert images to webp
    def convert_to_webp(self):
        # self.select_button['state'] = 'disabled'
        files_to_convert = []
        files_to_copy = []

        for root, dirs, files in os.walk(self.input_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    files_to_convert.append((root, file))
                else:
                    files_to_copy.append((root, file))

        self.progress1['maximum'] = len(files_to_convert)
        self.progress1['value'] = 0

        for root, file in files_to_convert:
            image_path = os.path.join(root, file)
            img = Image.open(image_path)
            relative_path = os.path.relpath(root, self.input_dir)
            new_dir = os.path.join(self.output_dir, relative_path)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            webp_path = os.path.join(new_dir, os.path.splitext(file)[0] + '.webp')
            img.save(webp_path, 'webp')

            self.progress1['value'] += 1
            self.root.update()

        # New code to copy other files
        for root, file in files_to_copy:
            src_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, self.input_dir)
            new_dir = os.path.join(self.output_dir, relative_path)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            dest_path = os.path.join(new_dir, file)
            shutil.copy2(src_path, dest_path)

        # self.select_button['state'] = 'normal'


    # combine all css style into one
    def combine_css(self):
        import_commands = set()
        styles = ""

        # Regular expression to match import commands
        import_regex = re.compile(r'@import url\([^)]+\);')

        # Regular expression to match comments
        comment_regex = re.compile(r'/\*.*?\*/', re.DOTALL)

        # Regular expression to match font-face rules with relative paths
        font_face_regex = re.compile(r'(@font-face\s*{[^}]*src:\s*url\(["\']?)(\.\./[^)"\']+)')

        css_files = []
        font_dir = None
        for root, dirs, files in os.walk(self.input_dir):
            if 'fonts' in dirs:
                font_dir = os.path.relpath(os.path.join(root, 'fonts'), self.input_dir)
            for file in files:
                if file.lower().endswith('.css'):
                    css_files.append((root, file))

        self.progress2['maximum'] = len(css_files)
        self.progress2['value'] = 0

        for root, file in css_files:
            css_path = os.path.join(root, file)
            with open(css_path, 'r') as f:
                contents = f.read()

            # Extract import commands
            for match in import_regex.findall(contents):
                import_commands.add(match)

            # Replace relative font paths with paths relative to font directory
            if font_dir is not None:
                while font_face_regex.search(contents):
                    contents = font_face_regex.sub(lambda m: m.group(1) + os.path.join(font_dir, os.path.basename(m.group(2))), contents)

            # Remove import commands and comments, and add styles
            contents = import_regex.sub('', contents)
            contents = comment_regex.sub('', contents)
            styles += contents

            # Update progress bar
            self.progress2['value'] += 1
            self.root.update_idletasks()

        # Write import commands and styles to new CSS file
        output_file = os.path.join(self.input_dir, 'default-css.min.css')
        with open(output_file, 'w') as f:
            for command in import_commands:
                f.write(command + '\n')
            f.write(styles)


    # Update CSS
    def update_css(self):
        # self.select_button['state'] = 'disabled'
        input_dir = self.input_dir
        output_dir = self.output_dir

        css_files = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith('.css'):
                    css_files.append((root, file))

        self.progress3['maximum'] = len(css_files)
        self.progress3['value'] = 0

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

            self.progress3['value'] += 1
            self.root.update()


    # Update HTML
    def update_html(self):
        # self.select_button['state'] = 'disabled'
        input_dir = self.input_dir
        output_dir = self.output_dir

        html_files = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith('.html'):
                    html_files.append((root, file))

        self.progress4['maximum'] = len(html_files)
        self.progress4['value'] = 0

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

            # Remove existing CSS links that are not CDN or external URL based
            for link in soup.find_all('link', rel='stylesheet'):
                try:
                    if link is not None and link.name is not None:
                        href = link.get('href', '')
                        if href and not href.startswith(('http://', 'https://', '//')):
                            link.decompose()
                except Exception as e:
                    print(f"Error processing link: {link}")
                    print(f"Exception: {e}")

            # Add new default CSS
            new_css_link = soup.new_tag('link', rel='stylesheet', href='default-css.min.css')
            soup.head.append(new_css_link)

            html_content = str(soup)

            relative_path = os.path.relpath(root, input_dir)
            new_dir = os.path.join(output_dir, relative_path)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            new_html_path = os.path.join(new_dir, file)

            with open(new_html_path, 'w') as f:
                f.write(html_content)

            self.progress4['value'] += 1
            self.root.update()


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()