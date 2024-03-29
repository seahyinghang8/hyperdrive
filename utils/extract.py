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
    field_queries: List[dict],
    k: int = 1,
    nlp: English = None,
) -> Dict[str, List[ExtractedField]]:
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")
    # iterate through all the pages
    top_k_fields_from_pages = [
        _get_top_k_fields_from_page(pg, field_queries, nlp, k)
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
                    query["arguments"]["word-neighbor-max-top-dist"],
                    query["arguments"]["word-neighbor-max-left-dist"],
                    query["arguments"]["word-neighbor-max-bottom-dist"],
                    query["arguments"]["word-neighbor-max-right-dist"],
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
    line_x = (line.center_left - page.left) / page.text_width
    return 1. - abs(line_x - position)


def _score_y_position(
    line: Line,
    position: float,
    page: Page
) -> float:
    line_y = (line.center_top - page.top) / page.text_height
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
    line: Line,
    line_idxs: Set[int],
    lines: List[Line],
    word_neighbors: List[str],
    page: Page,
    fuzzy_thres: int = 0.8
) -> float:
    word_scores = [0. for _ in range(len(word_neighbors))]
    for line_idx in line_idxs:
        neighboring_line_str = str(lines[line_idx])
        for i, wn in enumerate(word_neighbors):
            word_score = 0.
            if (wn.lower() in neighboring_line_str.lower()):
                word_score = 1.
            else:
                word_score = fuzzy_word_equal(
                    wn, neighboring_line_str)
                if (word_score < fuzzy_thres):
                    word_score = 0.
            cur_score = (
                word_score *
                _dist_word_score(lines[line_idx], line, page)
            )
            word_scores[i] = max(word_scores[i], cur_score)
    return sum(word_scores) / len(word_scores)


def _dist_word_score(
    line_a: Line,
    line_b: Line,
    page: Page,
) -> float:
    y_score = 1. - abs(line_a.center_top - line_b.center_top) / page.text_height
    x_score = 1. - abs(line_a.center_left - line_b.center_left) / page.text_width
    return (x_score + y_score) / 2.


def _score_near_words(
    line: Line,
    page: Page,
    word_neighbors: List[str],
    max_top_dist: float,
    max_left_dist: float,
    max_bottom_dist: float,
    max_right_dist: float
) -> float:
    valid_line_idxs = get_nearby_words(
        line, page, max_top_dist, max_left_dist, max_bottom_dist,
        max_right_dist)
    return _get_word_scores(
        line, valid_line_idxs, page.lines, word_neighbors, page)


def get_nearby_words(
    line: Line,
    page: Page,
    max_top_dist: float,
    max_left_dist: float,
    max_bottom_dist: float,
    max_right_dist: float
) -> Set[int]:
    x_idx = bisect(page.center_left_pos, (line.center_left,))
    y_idx = bisect(page.center_top_pos, (line.center_top,))
    valid_left_lines = set([])
    valid_top_lines = set([])
    j = 1

    def _get_x_dist(idx: int) -> int:
        comp = page.lines[page.center_left_pos[idx][1]]
        return abs(line.center_left - comp.center_left)

    def _get_y_dist(idx: int) -> int:
        comp = page.lines[page.center_top_pos[idx][1]]
        return abs(line.center_top - comp.center_top)

    while True:
        lower_idx = x_idx - j
        upper_idx = x_idx + j
        exceeded = True
        if (lower_idx >= 0 and
                _get_x_dist(lower_idx) < max_left_dist):
            valid_left_lines.add(page.center_left_pos[lower_idx][1])
            exceeded = False
        if (upper_idx < len(page.lines) and
                _get_x_dist(upper_idx) < max_right_dist):
            valid_left_lines.add(page.center_left_pos[upper_idx][1])
            exceeded = False
        if exceeded:
            break
        j += 1

    j = 1
    while True:
        lower_idx = y_idx - j
        upper_idx = y_idx + j
        exceeded = True
        if (lower_idx >= 0 and
                _get_y_dist(lower_idx) < max_top_dist):
            valid_top_lines.add(page.center_top_pos[lower_idx][1])
            exceeded = False
        if (upper_idx < len(page.lines) and
                _get_y_dist(upper_idx) < max_bottom_dist):
            valid_top_lines.add(page.center_top_pos[upper_idx][1])
            exceeded = False
        if exceeded:
            break
        j += 1
    valid_lines = valid_left_lines & valid_top_lines
    valid_lines = {
        vl
        for vl in valid_lines
        if str(page.lines[vl]) != str(line)
    }
    return valid_lines
