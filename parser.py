from typing import List, Tuple

import pytesseract
import pdf2image
import pandas as pd

try:
    from PIL import Image
except ImportError:
    import Image


def process_image(image: Image):
    tesseract_out = pytesseract.image_to_data(image)
    return parse_tesseract_data(tesseract_out)


def parse_tesseract_data(str) -> pd.DataFrame:
    # first line is a header, last line is empty
    lines = str.split('\n')[1:-1]
    lines = [line.split('\t') for line in lines]
    lines = [(line[11], int(line[10]), int(line[6]),
              int(line[7]), int(line[8]), int(line[9]),
              line[1:5]) for line in lines if len(line[11].strip()) > 0]
    word, confidence, left, top, width, height, line_info_list = zip(*lines)
    # iterate through the lines with a different counter
    line_num = []
    line_counter = -1
    prev_line_info = None
    for curr_line_info in line_info_list:
        if prev_line_info != curr_line_info:
            line_counter += 1
            prev_line_info = curr_line_info
        line_num.append(line_counter)

    return pd.DataFrame(
        {
            'word': word,
            'confidence': confidence,
            'left': left,
            'top': top,
            'width': width,
            'height': height,
            'line_num': line_num
        }
    )



if __name__ == "__main__":
    pdf_path = 'data/b.pdf'
    image_path = 'data/w2.jpg'
    process_image(Image.open(image_path))
    # process_image(pdf2image.convert_from_path(pdf_path)[0])
