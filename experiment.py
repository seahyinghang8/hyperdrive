import os

import utils
from utils.dataloader import Dataloader
from utils.extract import extract_fields
from utils.evaluator import evaluate_output

import spacy
import yaml
from iterextras import par_for

import argparse

parser = argparse.ArgumentParser(description='Run some experiments')
parser.add_argument('--config-path', type=str, required=True)

args = parser.parse_args()
cfg = yaml.load(open(args.config_path))
print(cfg)

nlp = spacy.load("en_core_web_sm")
dl = Dataloader(cfg["data_dir"], cfg["label_path"],
                concatenate_pages=True, cache_to_disk=True)
field_queries = yaml.load(open(cfg["queries_path"]))

if cfg["position_off"]:
    for query in field_queries:
        query['weights']['x-position'] = 0.
        query['weights']['y-position'] = 0.
if cfg["entity_off"]:
    for query in field_queries:
        query['weights']['entity'] = 0.
if cfg["neighbor_off"]:
    for query in field_queries:
        query['weights']['word-neighbors'] = 0.

fields = [f["name"] for f in field_queries]

num_docs = len(dl)
extracted_fields = par_for(
    lambda i: extract_fields(dl.get_document(i), field_queries, 1000, nlp),
    list(range(num_docs)),
    workers=1,
)
labels = [dl.get_label(i) for i in range(num_docs)]

errors = evaluate_output(extracted_fields, labels, fields)
yaml.dump(errors, open(cfg["error_path"], "w"))
