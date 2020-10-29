import itertools
import spacy
from spacy.lang.en import English

from typing import List, Tuple, Dict

from models.spatial_text import Page, Line
from models.document import Document

from utils.nlu import get_entity_scores
from utils.extract import get_nearby_words


def generate_query(
    name: str,
    line: Line,
    page: Page,
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
    query["arguments"]["entity"] = _gen_entity(line, nlp)
    x_pos, y_pos = _gen_position(line, page)
    query["arguments"]["x-position"] = x_pos
    query["arguments"]["y-position"] = y_pos
    query["arguments"]['word-neighbors'] = _gen_word_neighbors(
        line, page)
    return query


def _gen_entity(
    line: Line,
    nlp: English
) -> str:
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
    return best_label


def _gen_position(
    line: Line,
    page: Page
) -> Tuple[float, float]:
    return (
        line.center_left / page.width,
        line.center_top / page.height
    )


def _gen_word_neighbors(
    line: Line,
    page: Page,
    top_thres: float = 0.05,
    left_thres: float = 0.1,
) -> List[str]:
    line_idxs = get_nearby_words(line, page, top_thres, left_thres)
    line_strs = [str(page.lines[i]).split(' ') for i in line_idxs]
    return list(itertools.chain(*line_strs))
