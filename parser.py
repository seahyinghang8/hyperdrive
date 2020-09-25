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
    lines = [(line[11], line[10], line[6],
              line[7], line[8], line[9]) for line in lines]
    word, confidence, left, top, width, height = zip(*lines)
    df = pd.DataFrame({
        'word': word,
        'confidence': confidence,
        'left': left,
        'top': top,
        'width': width,
        'height': height
    })
    df[["left", "top", "width", "height"]] = (
        df[["left", "top", "width", "height"]].apply(pd.to_numeric)
    )
    return df


if __name__ == "__main__":
    pdf_path = '../w2/w2.pdf'
    process_image(pdf2image.convert_from_path(pdf_path)[0])
