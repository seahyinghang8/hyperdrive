import itertools
import operator
import spacy
from spacy.lang.en import English

from typing import List, Tuple, Dict

from models.spatial_text import Page, Line
from models.document import Document

from utils.nlu import get_entity_scores
from utils.extract import get_nearby_words


def generate_query(
    name: str,
    lines: List[Line],
    pages: List[Page],
    nlp: English = None
) -> Dict:
    if not nlp:
        nlp = spacy.load("en_core_web_sm")
    wn_dist = _gen_word_neighbor_dist(pages)
    query = {
        "name": name,
        "arguments": {
            "x-position": 0.0,
            "y-position": 0.0,
            "entity": None,
            "word-neighbors": [],
            "word-neighbor-max-top-dist": wn_dist,
            "word-neighbor-max-left-dist": wn_dist,
            "word-neighbor-max-bottom-dist": wn_dist,
            "word-neighbor-max-right-dist": wn_dist,
        },
        "weights": {
            "x-position": 0.25,
            "y-position": 0.25,
            "entity": 0.25,
            "word-neighbors": 0.25,
        }
    }
    query["arguments"]["entity"] = _gen_entity(lines, nlp)
    x_pos, y_pos = _gen_position(lines, pages)
    query["arguments"]["x-position"] = x_pos
    query["arguments"]["y-position"] = y_pos
    query["arguments"]['word-neighbors'] = _gen_word_neighbors(
        lines, pages)
    return query

def _gen_word_neighbor_dist(
    pages: List[Page],
    multiplier: int = 3,
) -> float:
    all_lines = sum(page.lines for page in pages)
    summed_line_heights = sum(line.height for line in all_lines)
    return summed_line_heights / len(all_lines) * multiplier

def _gen_entity(
    lines: List[Line],
    nlp: English
) -> str:
    score_dict = {}
    for line in lines:
        doc = nlp(str(line))
        entity_scores = get_entity_scores(nlp, doc)
        max_score = 0
        best_label = ""
        for key in entity_scores:
            entity_score = entity_scores[key]
            _, _, cur_label = key
            if entity_score > max_score:
                max_score = entity_score
                best_label = cur_label
        if best_label not in score_dict:
            score_dict[best_label] = 0
        score_dict[best_label] += max_score
    best_scoring_label = max(score_dict.items(), key=operator.itemgetter(1))[0]
    return best_scoring_label


def _gen_position(
    lines: List[Line],
    pages: List[Page]
) -> Tuple[float, float]:
    x_pos = sum([
        lines[i].center_left / pages[i].width for i in range(len(lines))
    ])
    y_pos = sum([
        lines[i].center_top / pages[i].height for i in range(len(lines))
    ])
    return (x_pos / len(pages), y_pos / len(pages))


def _gen_word_neighbors(
    lines: List[Line],
    pages: List[Page],
    max_top_dist: float,
    max_left_dist: float,
    max_bottom_dist: float,
    max_right_dist: float
) -> List[str]:
    line_str_sets = []
    for i in range(len(lines)):
        line, page = lines[i], pages[i]
        line_idxs = get_nearby_words(
            line, page, max_top_dist, max_left_dist,
            max_bottom_dist, max_right_dist)
        line_strs = set([str(page.lines[i]) for i in line_idxs])
        line_str_sets.append(line_strs)
    return list(set.intersection(*line_str_sets))
