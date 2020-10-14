from utils.parser import process_image
from utils.cluster import cluster_text
from utils.extract import extract_fields
from utils.dataloader import Dataloader

import os


if __name__ == "__main__":
    w2_sample_dir = os.path.join('data', 'sample', 'w2')
    data_dir = os.path.join(w2_sample_dir, 'single_clean')
    label_path = os.path.join(w2_sample_dir, 'single_label.csv')

    dl = Dataloader(data_dir, label_path)
    pdf_doc = dl.get_document(0)
    field_queries = [
        {   # Field 1
            "name": "Employer Identification Number",
            "arguments": {
                "x-position": 0.1,
                "y-position": 0.1,
                "entity": "CARDINAL",
                "word-neighbors": ["Employer", "Identification", "Number"],
                "word-neighbor-top-thres": 50,
                "word-neighbor-left-thres": 200,
            },
            "weights": {
                "x-position": 0.5,
                "y-position": 0.2,
                "entity": 0.5,
                "word-neighbors": 0.2,
            }
        },
        {   # Field 2
            "name": "Medicare Tax Witheld",
            "arguments": {
                "x-position": 0.9,
                "y-position": 0.1,
                "entity": "CARDINAL",
                "word-neighbors": ["Medicare", "Tax", "Withheld"],
                "word-neighbor-top-thres": 50,
                "word-neighbor-left-thres": 200,
            },
            "weights": {
                "x-position": 0.2,
                "y-position": 0.4,
                "entity": 0.5,
                "word-neighbors": 0.2,
            }
        },
    ]
    fields = extract_fields(pdf_doc, field_queries)

    print("---- Extracted Fields ----")
    for name, val_list in fields.items():
        print(f"{name}: {val_list}")
