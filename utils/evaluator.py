from typing import List, Dict
from rapidfuzz import fuzz

from models.field import ExtractedField


def evaluate_output(
    extracted_fields: List[dict],
    ground_truths: List[dict],
    fields: List[str]
) -> Dict[str, List[tuple]]:
    # Return all the errors
    errors: Dict[str, List[tuple]] = {}

    for field in fields:
        outputs = [
            str(d[field][0].line) if field in d else ''
            for d in extracted_fields
        ]
        labels = [str(d[field]) if field in d else '' for d in ground_truths]
        mismatch = [
            (i, output, label)
            for i, (output, label) in enumerate(zip(outputs, labels))
            if output != label
        ]
        errors[field] = mismatch
        accuracy = 1 - (len(mismatch) / len(labels))
        print(f"Field: {field}\tAccuracy: {accuracy}")

    return errors
