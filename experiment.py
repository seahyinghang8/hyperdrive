import os

import utils
from utils.dataloader import Dataloader
from utils.extract import extract_fields
from utils.evaluator import evaluate_output

import spacy
import pickle
from iterextras import par_for

import argparse

parser = argparse.ArgumentParser(description='Run some experiments')
parser.add_argument('--num-workers', type=int, required=True)
parser.add_argument('--error-path', type=str, required=True)
parser.add_argument('--position-off', action='store_true', default=False)
parser.add_argument('--entity-off', action='store_true', default=False)
parser.add_argument('--neighbor-off', action='store_true', default=False)

args = parser.parse_args()
nlp = spacy.load("en_core_web_sm")


def get_w2_train_dataloader(doc_type: str):
    main_dir = os.path.join('data', 'full', 'w2', 'train')
    data_dir = os.path.join(main_dir, doc_type)
    label_path = os.path.join(main_dir, f'{doc_type}_label.csv')
    return Dataloader(data_dir, label_path,
                      concatenate_pages=True, cache_to_disk=True)


dl = get_w2_train_dataloader('single')
single_field_queries = [
    {   # Field 1
        "name": "EIN",
        "arguments": {
            "x-position": 0.10,
            "y-position": 0.05,
            "entity": "EIN",
            "word-neighbors": ["Employer Identification Number"],
            "word-neighbor-max-top-dist": 13,
            "word-neighbor-max-left-dist": 15,
            "word-neighbor-max-bottom-dist": 0,
            "word-neighbor-max-right-dist": 0,
        },
        "weights": {
            "x-position": 0.25,
            "y-position": 0.25,
            "entity": 0.25,
            "word-neighbors": 0.25,
        }
    },
    {   # Field 2
        "name": "Employer's Name",
        "arguments": {
            "x-position": 0.22,
            "y-position": 0.09,
            "entity": "",
            "word-neighbors": ["Employer's name, address, and ZIP code"],
            "word-neighbor-max-top-dist": 15,
            "word-neighbor-max-left-dist": 150,
            "word-neighbor-max-bottom-dist": 0,
            "word-neighbor-max-right-dist": 0,
        },
        "weights": {
            "x-position": 0.33,
            "y-position": 0.33,
            "entity": 0.,
            "word-neighbors": 0.33,
        }
    },
    {   # Field 3
        "name": "Employer's Street Address",
        "arguments": {
            "x-position": 0.22,
            "y-position": 0.16,
            "entity": "",
            "word-neighbors": ["Control number", "Employer's name, address, and ZIP code"],
            "word-neighbor-max-top-dist": 30,
            "word-neighbor-max-left-dist": 150,
            "word-neighbor-max-bottom-dist": 50,
            "word-neighbor-max-right-dist": 0,
        },
        "weights": {
            "x-position": 0.25,
            "y-position": 0.30,
            "entity": 0.,
            "word-neighbors": 0.45,
        }
    },
    {   # Field 4
        "name": "Employer's City-State-Zip",
        "arguments": {
            "x-position": 0.22,
            "y-position": 0.2,
            "entity": "",
            "word-neighbors": ["Control number", "Employer's name, address, and ZIP code"],
            "word-neighbor-max-top-dist": 50,
            "word-neighbor-max-left-dist": 150,
            "word-neighbor-max-bottom-dist": 30,
            "word-neighbor-max-right-dist": 0,
        },
        "weights": {
            "x-position": 0.25,
            "y-position": 0.30,
            "entity": 0.,
            "word-neighbors": 0.45,
        }
    },
    {   # Field 5
        "name": "Employee Social Security Number",
        "arguments": {
            "x-position": 0.36,
            "y-position": 0.08,
            "entity": "SSN",
            "word-neighbors": ["Employee's social security number"],
            "word-neighbor-max-top-dist": 20,
            "word-neighbor-max-left-dist": 30,
            "word-neighbor-max-bottom-dist": 0,
            "word-neighbor-max-right-dist": 0,
        },
        "weights": {
            "x-position": 0.25,
            "y-position": 0.25,
            "entity": 0.25,
            "word-neighbors": 0.25,
        }
    },
    {   # Field 6
        "name": "Social Security Wages",
        "arguments": {
            "x-position": 0.66,
            "y-position": 0.09,
            "entity": "DOLLAR_AMOUNT",
            "word-neighbors": [""],
            "word-neighbor-max-top-dist": 20,
            "word-neighbor-max-left-dist": 15,
            "word-neighbor-max-bottom-dist": 10,
            "word-neighbor-max-right-dist": 0,
        },
        "weights": {
            "x-position": 0.25,
            "y-position": 0.25,
            "entity": 0.25,
            "word-neighbors": 0.25,
        }
    },
    {   # Field 7
        "name": "Medicare Tax Withheld",
        "arguments": {
            "x-position": 0.88,
            "y-position": 0.12,
            "entity": "DOLLAR_AMOUNT",
            "word-neighbors": ["Medicare tax withheld"],
            "word-neighbor-max-top-dist": 20,
            "word-neighbor-max-left-dist": 20,
            "word-neighbor-max-bottom-dist": 20,
            "word-neighbor-max-right-dist": 0,
        },
        "weights": {
            "x-position": 0.25,
            "y-position": 0.25,
            "entity": 0.25,
            "word-neighbors": 0.25,
        }
    },
    {   # Field 8
        "name": "Locality Name_1",
        "arguments": {
            "x-position": 0.96,
            "y-position": 0.37,
            "entity": "",
            "word-neighbors": ["Locality name"],
            "word-neighbor-max-top-dist": 20,
            "word-neighbor-max-left-dist": 10,
            "word-neighbor-max-bottom-dist": 0,
            "word-neighbor-max-right-dist": 0,
        },
        "weights": {
            "x-position": 0.33,
            "y-position": 0.33,
            "entity": 0.,
            "word-neighbors": 0.33,
        }
    },
    {   # Field 9
        "name": "Locality Name_2",
        "arguments": {
            "x-position": 0.96,
            "y-position": 0.4,
            "entity": "",
            "word-neighbors": ["Locality name", "Department of the Treasury--Internal Revenue Service"],
            "word-neighbor-max-top-dist": 40,
            "word-neighbor-max-left-dist": 70,
            "word-neighbor-max-bottom-dist": 20,
            "word-neighbor-max-right-dist": 0,
        },
        "weights": {
            "x-position": 0.25,
            "y-position": 0.25,
            "entity": 0.,
            "word-neighbors": 0.50,
        }
    },
]

if args.position_off:
    for query in single_field_queries:
        query['weights']['x-position'] = 0.
        query['weights']['y-position'] = 0.
if args.entity_off:
    for query in single_field_queries:
        query['weights']['entity'] = 0.
if args.neighbor_off:
    for query in single_field_queries:
        query['weights']['word-neighbors'] = 0.

field_queries = single_field_queries
fields = [f["name"] for f in field_queries]

num_docs = len(dl)
extracted_fields = par_for(
    lambda i: extract_fields(dl.get_document(i), field_queries, 1000, nlp),
    list(range(num_docs)),
    workers=args.num_workers,
)
labels = [dl.get_label(i) for i in range(num_docs)]

errors = evaluate_output(extracted_fields, labels, fields)
pickle.dump(errors, open(args.error_path, "wb"))
