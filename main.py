from utils.parser import process_image
from utils.cluster import cluster_text
from utils.extract import extract_fields
from utils.dataloader import Dataloader

from models.document import Document, Page
from models.spatial_text import Line

import os


if __name__ == "__main__":
    w2_sample_dir = os.path.join('data', 'sample', 'w2')
    data_dir = os.path.join(w2_sample_dir, 'single_clean')
    label_path = os.path.join(w2_sample_dir, 'single_label.csv')
    dl = Dataloader(data_dir, label_path)
    page_data = dl[0]
    page_image = page_data['image']
    pdf_pages = [
        Page(
            lines=cluster_text(process_image(page_image), page_image),
            image=page_image
        )
    ]
    pdf_doc = Document(pdf_pages)
    fields = extract_fields(pdf_doc)

    print("---- Extracted Fields ----")
    for name, val_list in fields.items():
        print(f"{name}: {val_list}")
