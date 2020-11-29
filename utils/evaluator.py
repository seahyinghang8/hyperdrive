from typing import List, Dict, Tuple, Any
from rapidfuzz import fuzz

from models.field import ExtractedField


def evaluate_output(
    extracted_fields: List[dict],
    ground_truths: List[dict],
    fields: List[str]
) -> Dict[str, List[Tuple[int, str, str]]]:
    # Return all the errors
    errors: Dict[str, List[Tuple[int, str, str]]] = {}

    for field in fields:
        outputs = [
            str(d[field][0].line) if field in d else ''
            for d in extracted_fields
        ]
        labels = [
            ' '.join(str(d[field]).split()) if field in d else ''
            for d in ground_truths
        ]
        mismatch = [
            (i, output, label)
            for i, (output, label) in enumerate(zip(outputs, labels))
            if output != label
        ]
        errors[field] = mismatch
        accuracy = 1 - (len(mismatch) / len(labels))
        print(f"Field: {field}\tAccuracy: {accuracy}")

    return errors
