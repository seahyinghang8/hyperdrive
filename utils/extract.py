import spacy
from spacy.lang.en import English

from bisect import bisect
from typing import List, Tuple, Dict, Set

from models.spatial_text import Page, Line
from models.document import Document
from models.field import FieldScore, ExtractedField
from utils.helpers import flatten
from utils.nlu import get_entity_scores, fuzzy_word_equal


def extract_fields(
    doc: Document,
    field_queries: List[dict]
) -> Dict[str, List[ExtractedField]]:

    nlp = spacy.load("en_core_web_sm")
    # iterate through all the pages
    top_k_fields_from_pages = [
        _get_top_k_fields_from_page(pg, field_queries, nlp, 2)
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
    nlp: English,
    k: int = 1,
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
        for field_scores in _score_page(page, field_queries, nlp)
    ]

    return fields_lines_scores


def _score_page(
    page: Page,
    field_queries: List[dict],
    nlp: English
) -> List[List[FieldScore]]:
    # outer list will be the various fields
    # inner list will be the various lines
    lines_fields_scores = [
        _score_line(line, field_queries, page, nlp)
        for line in page.lines
    ]
    transposed_scores = [
        list(x) for x in zip(*lines_fields_scores)
    ]
    return transposed_scores


def _score_line(
    line: Line,
    field_queries: List[dict],
    page: Page,
    nlp: English,
) -> List[FieldScore]:
    line_scores = [
        FieldScore(
            weights={
                "x-position": query["weights"]["x-position"],
                "y-position": query["weights"]["y-position"],
                "entity": query["weights"]["entity"],
                "word-neighbors": query["weights"]["word-neighbors"],
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
                ),
                "entity": _score_entity(
                    line,
                    nlp,
                    query["arguments"]["entity"]
                ),
                "word-neighbors": _score_near_words(
                    line,
                    page,
                    query["arguments"]["word-neighbors"],
                    query["arguments"]["word-neighbor-top-thres"],
                    query["arguments"]["word-neighbor-left-thres"]
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


def _score_entity(
    line: Line,
    nlp: English,
    entity: str
) -> float:
    if (not entity):
        return 0.0
    doc = nlp(str(line))
    score = 0.0
    entity_scores = get_entity_scores(nlp, doc)
    for key in entity_scores:
        entity_score = entity_scores[key]
        _, _, cur_label = key
        if cur_label == entity:
            score = max(score, entity_score)
    return score


def _get_word_scores(
    line_idxs: Set[int],
    lines: List[Line],
    word_neighbors: List[str]
) -> float:
    word_scores = [0. for _ in range(len(word_neighbors))]
    for line_idx in line_idxs:
        for i, wn in enumerate(word_neighbors):
            word_scores[i] = max(
                word_scores[i], fuzzy_word_equal(wn, str(lines[line_idx])))
    return sum(word_scores) / len(word_scores)


def _score_near_words(
    line: Line,
    page: Page,
    word_neighbors: List[str],
    top_thres: float,
    left_thres: float
) -> float:
    left_idx = bisect(page.left_pos, (line.left,))
    top_idx = bisect(page.top_pos, (line.top,))
    valid_left_lines = set([])
    valid_top_lines = set([])
    j = 1

    def _get_comp_left_dist(
        idx: int
    ) -> int:
        return abs(line.left - page.left_pos[idx][0])

    def _get_comp_top_dist(
        idx: int
    ) -> int:
        return abs(line.top - page.top_pos[idx][0])

    while True:
        lower_idx = left_idx - j
        upper_idx = left_idx + j
        exceeded = True
        if (lower_idx > 0 and
                _get_comp_left_dist(lower_idx) < left_thres):
            valid_left_lines.add(page.left_pos[lower_idx][1])
            exceeded = False
        if (upper_idx < len(page.lines) and 
                _get_comp_left_dist(upper_idx) < left_thres):
            valid_left_lines.add(page.left_pos[upper_idx][1])
            exceeded = False
        if exceeded:
            break
        j += 1

    j = 1
    while True:
        lower_idx = top_idx - j
        upper_idx = top_idx + j
        exceeded = True
        if (lower_idx > 0 and
                _get_comp_top_dist(lower_idx) < top_thres):
            valid_top_lines.add(page.top_pos[lower_idx][1])
            exceeded = False
        if (upper_idx < len(page.lines) and
                _get_comp_top_dist(upper_idx) < top_thres):
            valid_top_lines.add(page.top_pos[upper_idx][1])
            exceeded = False
        if exceeded:
            break
        j += 1

    valid_line_idxs = valid_left_lines & valid_top_lines
    return _get_word_scores(valid_line_idxs, page.lines, word_neighbors)
