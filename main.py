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
            "name": "Medicare Tax withheld",
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

    num_docs = 4
    extracted_fields = [
        extract_fields(dl.get_document(i), field_queries)
        for i in range(num_docs)
    ]
    labels = [dl.get_label(i) for i in range(num_docs)]
    evaluate_output(extracted_fields,
                    labels, ['EIN', 'Medicare Tax withheld'], 0.2)
