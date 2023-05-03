# pic2pdf
## Overview
This Python script converts multiple images into a single PDF file, inspired by **[img2pdf](https://pypi.org/project/img2pdf/)**.

Unlike the `img2pdf` library, `pic2pdf` is primarily focused on converting images within a given directory or a single image file. The code is simpler compared to `img2pdf`, but the optimization of the conversion process might not be as advanced, potentially resulting in slower processing times.

## Requirement
The script uses the Python libraries **[Pillow](https://pypi.org/project/Pillow/)** and **[pikepdf](https://pypi.org/project/pikepdf/)** to do the conversion.

## Features
- Convert multiple images within a specified directory into a single PDF file.
- Simpler code compared to `img2pdf`.

## Usage
To use `pic2pdf`, simply execute the script and provide the input file path or directory path containing the images. Optionally, you can also specify the output PDF file path. If not specified, the output file name will be generated based on the input file or directory name.
```
$ python pic2pdf.py input_directory -o output.pdf
```

## Author
[mashu3](https://github.com/mashu3)