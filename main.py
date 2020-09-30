import pdf2image

from utils.parser import process_image
from utils.cluster import cluster_text
from utils.extract import extract_fields

from models.document import Document, Page
from models.spatial_text import Line


if __name__ == "__main__":
    pdf_path = "data/w2/W2_Multi_Sample_Data_input_IRS2_clean_10414.pdf"
    pdf_images = pdf2image.convert_from_path(pdf_path)
    pdf_pages = [
        Page(
            lines=cluster_text(process_image(page_image), page_image),
            image=page_image
        )
        for page_image in pdf_images
    ]
    pdf_doc = Document(pdf_pages)
    fields = extract_fields(pdf_doc)

    print("---- Extracted Fields ----")
    for name, val_list in fields.items():
        print(f"{name}: {val_list}")
