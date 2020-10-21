from typing import List
from rapidfuzz import fuzz

from models.field import ExtractedField


def evaluate_output(
    extracted_fields: List[dict],
    ground_truths: List[dict],
    fields: List[str]
) -> None:
    # error_tolerance [0., 1.] where 0. means no room for error
    # 0.5 means 50% of the algorithm have to match the true label
    for field in fields:
        outputs = [
            str(d[field][0].line) if field in d else ''
            for d in extracted_fields
        ]
        labels = [str(d[field]) if field in d else '' for d in ground_truths]
        accuracy = compute_accuracy(outputs, labels)
        print(f"Field: {field}\tAccuracy: {accuracy}")


def compute_accuracy(
    outputs: List[str],
    labels: List[str]
) -> float:
    match = [
        output == label
        for output, label in zip(outputs, labels)
    ]
    return sum(match) / len(labels)
