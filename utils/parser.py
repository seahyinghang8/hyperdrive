from typing import List
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

from models.spatial_text import Line, Word
from utils.img_preprocess import ocr_preprocess


# Process image using Tesseract OCR to get a list of Lines
def process_image(image: Image) -> List[Line]:
    tesseract_out = pytesseract.image_to_data(
        ocr_preprocess(image))
    return _parse_tesseract_data(tesseract_out)


def _parse_tesseract_data(data_str: str) -> List[Line]:
    # first line is a header, last line is empty
    output_lines = data_str.split('\n')[1:-1]

    lines: List[Line] = [Line([])]
    curr_line: Line = lines[-1]
    prev_word_metadata: str = ""
    for output_line in output_lines:
        word_info_split = output_line.split('\t')
        text = word_info_split[11]
        # skip words where the text are just spaces
        if text.strip() == '':
            continue
        # mismatch in metadata means it is a newline
        curr_word_metadata = ' '.join(word_info_split[1:5])
        if prev_word_metadata != curr_word_metadata:
            prev_word_metadata = curr_word_metadata
            if len(curr_line) > 0:
                lines.append(Line([]))
                curr_line = lines[-1]
        new_word = Word(
            text=text,
            confidence=int(word_info_split[10]),
            left=int(word_info_split[6]),
            top=int(word_info_split[7]),
            width=int(word_info_split[8]),
            height=int(word_info_split[9])
        )
        curr_line.append(new_word)
    return lines
