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
    query = {
        "name": name,
        "arguments": {
            "x-position": 0.0,
            "y-position": 0.0,
            "entity": None,
            "word-neighbors": [],
            "word-neighbor-top-thres": 0.05,
            "word-neighbor-left-thres": 0.1,
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
    top_thres: float = 0.05,
    left_thres: float = 0.1,
) -> List[str]:
    line_str_sets = []
    for i in range(len(lines)):
        line, page = lines[i], pages[i]
        line_idxs = get_nearby_words(line, page, top_thres, left_thres)
        line_strs = set(
            itertools.chain(
                *[str(page.lines[i]).split(' ')
                  for i in line_idxs]
            )
        )
        line_str_sets.append(line_strs)
    return list(set.intersection(*line_str_sets))
