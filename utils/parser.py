from typing import List
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine, LTChar
from pdfminer.layout import LTRect, LTLine, LTFigure

from models.spatial_text import Line, Word, Page
from models.document import Document
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
            confidence=float(word_info_split[10]),
            left=int(word_info_split[6]),
            top=int(word_info_split[7]),
            width=int(word_info_split[8]),
            height=int(word_info_split[9])
        )
        curr_line.append(new_word)
    return lines


# Process pdf using pdfminer
def process_pdf(path: str) -> Document:
    pages = []
    for page_layout in extract_pages(path):
        lines = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                lines += _get_lines(element, page_layout.height)
            elif isinstance(element, LTRect):
                pass    # For the future Rectangles
            elif isinstance(element, LTLine):
                pass    # For the future Lines
            elif isinstance(element, LTFigure):
                pass    # For the future Figures
        pages.append(Page(lines, page_layout.width, page_layout.height))

    return Document(pages, path)


def _get_lines(text_box: LTTextContainer, page_height: int) -> List[Line]:
    return [_convert_to_spatial_line(tl, page_height) for tl in text_box]


def _convert_to_spatial_line(text_line: LTTextLine, page_height: int) -> Line:
    curr = _empty_curr_word()
    words = []

    for char in text_line:
        char_text = char.get_text() if isinstance(char, LTChar) else ' '

        if char_text == ' ':
            if curr['started']:
                new_word = _convert_curr_to_word(curr, page_height)
                words.append(new_word)
                curr = _empty_curr_word()
        else:
            if not curr['started']:
                curr['left'] = char.x0
                curr['bottom'] = char.y0
                curr['started'] = True
            curr['top'] = max(curr['top'], char.y1)
            curr['right'] = max(curr['right'], char.x1)
            curr['bottom'] = min(curr['bottom'], char.y0)
            curr['text'] += char_text
            curr['font'] = char.fontname

    if curr['started']:
        new_word = _convert_curr_to_word(curr, page_height)
        words.append(new_word)
    return Line(words)


def _convert_curr_to_word(curr: dict, page_height: int) -> Word:
    width = int(curr['right'] - curr['left'])
    height = int(curr['top'] - curr['bottom'])
    return Word(
        text=curr['text'],
        confidence=1.,
        left=int(curr['left']),
        top=int(page_height - curr['top']),
        width=width,
        height=height,
        font=curr['font']
    )


def _empty_curr_word() -> dict:
    return {
        'text': '',
        'font': '',
        'left': 0.,
        'right': 0.,
        'top': 0.,
        'bottom': 0.,
        'started': False
    }
