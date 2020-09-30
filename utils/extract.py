from typing import List, Tuple, Dict

from models.spatial_text import Page, Line
from models.document import Document
from models.field import FieldScore, ExtractedField
from utils.helpers import flatten


def extract_fields(doc: Document) -> Dict[str, List[ExtractedField]]:
    field_queries = [
        {   # Field 1
            "name": "Employer Identification Number",
            "arguments": {
                "x-position": 0.1,
                "y-position": 0.1
            },
            "weights": {
                "x-position": 0.5,
                "y-position": 0.2
            }
        },
        {   # Field 2
            "name": "Medicare Tax Witheld",
            "arguments": {
                "x-position": 0.9,
                "y-position": 0.1
            },
            "weights": {
                "x-position": 0.2,
                "y-position": 0.4
            }
        },
    ]
    # TODO: will be replaced from a hardcoded variable
    #       to an argument to the function
    # TODO: maybe replace the field query to be an object

    # iterate through all the pages
    top_k_fields_from_pages = [
        _get_top_k_fields_from_page(pg, field_queries, 2)
        for pg in doc.pages
    ]
    top_fields_from_doc = flatten(top_k_fields_from_pages)
    extracted_fields = {
        str(query['name']): fields
        for query, fields in zip(field_queries, top_fields_from_doc)
    }
    return extracted_fields


def _get_top_k_fields_from_page(
    page: Page,
    field_queries: List[dict],
    k: int = 1
) -> List[List[ExtractedField]]:
    # outer dict will be the various fields
    # inner list will be the top k lines
    fields_lines_scores = [
        sorted(
            [
                ExtractedField(i, page[i], score)
                for i, score in enumerate(field_scores)
            ],
            key=lambda x: x.score.total_score,
            reverse=True
        )[:k]
        for field_scores in _score_page(page, field_queries)
    ]

    return fields_lines_scores


def _score_page(
    page: Page,
    field_queries: List[dict]
) -> List[List[FieldScore]]:
    # outer list will be the various fields
    # inner list will be the various lines
    lines_fields_scores = [
        _score_line(line, field_queries, page)
        for line in page.lines
    ]
    transposed_scores = [
        list(x) for x in zip(*lines_fields_scores)
    ]
    return transposed_scores


def _score_line(
    line: Line,
    field_queries: List[dict],
    page: Page
) -> List[FieldScore]:
    line_scores = [
        FieldScore(
            weights={
                "x-position": query["weights"]["x-position"],
                "y-position": query["weights"]["y-position"]
            },
            scores={
                "x-position": _score_x_position(
                    line,
                    query["arguments"]["x-position"],
                    page
                ),
                "y-position": _score_y_position(
                    line,
                    query["arguments"]["y-position"],
                    page
                )
            }
        ) for query in field_queries
    ]
    return line_scores


def _score_x_position(
    line: Line,
    position: float,
    page: Page
) -> float:
    line_x = (line.center_left - page.left) / page.width
    return 1. - abs(line_x - position)


def _score_y_position(
    line: Line,
    position: float,
    page: Page
) -> float:
    line_y = (line.center_top - page.top) / page.height
    return 1. - abs(line_y - position)
