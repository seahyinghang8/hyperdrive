import pdf2image
from PIL import Image, ImageDraw, ImageFont

from utils.parser import process_image
from utils.cluster import cluster_text
from utils.extract import extract_fields

from models.document import Document

from models.spatial_text import Page, Line

TEXT_OFFSET = 0.1


def get_ocr_viz(
    page: Page
) -> Image:
    ocr_img = Image.new("RGBA", page.image.size, (255, 255, 255))
    canvas = ImageDraw.Draw(ocr_img)
    for line in page.lines:
        line_txt = str(line)
        canvas.rectangle(
            [line.left, line.top, line.right, line.bottom], outline=(0, 0, 0))
        font_size = min(line.height, int(line.width / len(line_txt)))
        canvas.text(
            (
                line.left + TEXT_OFFSET * line.width,
                line.center_top - font_size / 2
            ),
            line_txt,
            font=ImageFont.truetype(
                "/Library/Fonts/Arial.ttf",
                font_size,
                encoding='UTF-8'
            ),
            fill=(0, 0, 0)
        )
    ocr_img.show()


if __name__ == "__main__":
    pdf_path = "../w2/w2.pdf"
    pdf_images = pdf2image.convert_from_path(pdf_path)
    pdf_pages = [
        Page(
            lines=cluster_text(process_image(page_image), page_image),
            image=page_image
        )
        for page_image in pdf_images
    ]
    get_ocr_viz(pdf_pages[0])
