from utils.parser import process_image
from utils.cluster import cluster_text
from utils.extract import extract_fields
from utils.dataloader import Dataloader
from utils.evaluator import evaluate_output

import os


if __name__ == "__main__":
    w2_sample_dir = os.path.join('data', 'sample', 'w2')
    data_dir = os.path.join(w2_sample_dir, 'single_clean')
    label_path = os.path.join(w2_sample_dir, 'single_label.csv')

    dl = Dataloader(data_dir, label_path)
    field_queries = [
        {   # Field 1
            "name": "EIN",
            "arguments": {
                "x-position": 0.1,
                "y-position": 0.1,
                "entity": "EIN",
                "word-neighbors": ["Employer", "Identification", "Number"],
                "word-neighbor-top-thres": 0.05,
                "word-neighbor-left-thres": 0.1,
            },
            "weights": {
                "x-position": 0.25,
                "y-position": 0.25,
                "entity": 0.25,
                "word-neighbors": 0.25,
            }
        },
        {   # Field 2
            "name": "Medicare Tax withheld",
            "arguments": {
                "x-position": 0.9,
                "y-position": 0.1,
                "entity": "CARDINAL",
                "word-neighbors": ["Medicare", "Tax", "Withheld"],
                "word-neighbor-top-thres": 0.05,
                "word-neighbor-left-thres": 0.1,
            },
            "weights": {
                "x-position": 0.25,
                "y-position": 0.25,
                "entity": 0.25,
                "word-neighbors": 0.25,
            }
        }
    ]

    num_docs = 9
    extracted_fields = [
        extract_fields(dl.get_document(i), field_queries)
        for i in range(num_docs)
    ]
    labels = [dl.get_label(i) for i in range(num_docs)]
    evaluate_output(extracted_fields,
                    labels, ['EIN', 'Medicare Tax withheld'])
