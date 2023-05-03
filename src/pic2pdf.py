# -*- coding: utf-8 -*-
# Copyright (c) 2023 mashu3
# This software is released under the MIT License, see LICENSE.

import io
import os
import re
import sys
import zlib
import pikepdf
import argparse
from PIL import Image
import concurrent.futures

class PdfConverter():
    def add_image_page(self, params):
        (pdf, image_file) = params
        image = Image.open(image_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        page = pdf.add_blank_page(page_size=(image.width, image.height))
        stream = pikepdf.Stream(pdf, zlib.compress(image.tobytes()))
        stream.Type = pikepdf.Name.XObject
        stream.Subtype = pikepdf.Name.Image
        stream.ColorSpace = pikepdf.Name.DeviceRGB
        stream.BitsPerComponent = 8
        stream.Width = image.width
        stream.Height = image.height
        stream.Filter = pikepdf.Name.FlateDecode

        page.Resources.XObject = pikepdf.Dictionary(Im0=stream)
        contents = f"q {image.width} 0 0 {image.height} 0 0 cm /Im0 Do Q".encode()
        page.Contents = pdf.make_indirect(pikepdf.Stream(pdf, contents))
        pdf.pages.remove(p=1)
        return page

    def display_progress_bar(self, file_count, total_count, bar_length=35):
        filled = int(round(bar_length * file_count / float(total_count)))
        remaining = bar_length - filled
        progress_bar = "█" * filled + " " * remaining
        percent = round(100.0 * file_count / float(total_count), 1)
        text = f"|{progress_bar}| {percent}% ({file_count}/{total_count})\r"
        if file_count != total_count:
            sys.stdout.write(text)
        else:
            sys.stdout.write(text[:-1]+'\n')

    def to_pdf_bytes(self, image_files):
        pdf_bytes = io.BytesIO()
        with pikepdf.new() as pdf:
            futures = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                params = map(lambda image_file: (pdf, image_file), image_files)
                for i, future in enumerate(executor.map(self.add_image_page, params)):
                    futures.append(future)
                    self.display_progress_bar(i+1, len(image_files))
            for future in futures:
                pdf.pages.append(future)
            pdf.save(pdf_bytes)
            pdf_bytes.seek(0)
        return pdf_bytes.read()

    def is_image_file(self, filename):
        supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        return any(filename.lower().endswith(ext) for ext in supported_extensions)

    def sort_key(self, filename):
        filename = filename.lower()
        key = []
        if 'cover' in filename:
            key.append(True)
        else:
            key.append(False)
        for s in re.split(r'(\d+)', filename):
            if s.isdigit():
                key.append(int(s))
            else:
                key.append(s)
        if 'copyright' in filename:
            key.append(True)
        else:
            key.append(False)
        return tuple(key)

    def find_image_files(self, input_path):
        img_files = []
        if os.path.isdir(input_path):
            for root, _, files in os.walk(input_path):
                for file in files:
                    if self.is_image_file(file):
                        img_files.append(os.path.join(root, file))
        elif os.path.isfile(input_path) and self.is_image_file(input_path):
            img_files.append(input_path)
        img_files.sort(key=self.sort_key)
        return img_files
    
class HelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog, indent_increment=2, max_help_position=6, width=None):
        super().__init__(prog, indent_increment, max_help_position, width)
    def _split_lines(self, text, _):
        return text.splitlines()

def convert(image_files, output_path):
    pic2pdf = PdfConverter()
    with open(output_path, "wb") as f:
        f.write(pic2pdf.to_pdf_bytes(image_files))

def main():
    parser = argparse.ArgumentParser(description='This program converts an entire directory of images into a single PDF file.')
    parser.add_argument('input_path', metavar='input_path', type=str,
                        help='input file path or directory path')
    parser.add_argument('-o', '--output', dest='output_path', type=str, default=None,
                        help='output PDF file path. If not specified, the output file name is generated from the input file or directory name.')
    args = parser.parse_args()

    if args.input_path is None:
        parser.print_usage()
        parser.print_help()
        sys.exit(1)
    else:
        input_path = args.input_path
        if os.path.isdir(input_path):
            image_files = PdfConverter().find_image_files(input_path)
        else:
            image_files = [input_path]

        if not (PdfConverter().is_image_file(f) for f in image_files):
            print('Error: All inputs should be image files (jpg, png, etc.)')
            sys.exit(1)

    if args.output_path is None:
        if os.path.isdir(input_path):
            pdf_filename = os.path.basename(input_path) + '.pdf'
            output_path = os.path.join(input_path, pdf_filename).replace(os.sep, '/')
        else:
            pdf_filename = os.path.basename(os.path.dirname(input_path)) + '.pdf'
            output_path = os.path.join(os.path.dirname(input_path), pdf_filename).replace(os.sep, '/')
    else:
        if not args.output_path.endswith('.pdf'):
            print('Error: The output file must be a PDF file.')
            sys.exit(1)
        output_path = args.output_path

    try:
        convert(image_files, output_path)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()