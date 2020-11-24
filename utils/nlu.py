import re
from collections import defaultdict
from typing import DefaultDict, Tuple

import spacy
from spacy.lang.en import English
from rapidfuzz import fuzz

from utils.regex_entities import REGEX_ENTITIES


def get_entity_scores(
    nlp: English,
    doc: spacy.tokens.doc.Doc,
    beam_width: int = 16,
    beam_density: float = 0.0001,
    length_thres: float = 0.7,
) -> DefaultDict[Tuple[int, int, str], float]:
    # calculate NER confidence score using method in this discussion:
    # https://support.prodi.gy/t/displaying-a-confidence-score-next-to-a-user-defined-entity/403/6
    doclen = len(doc)
    beams = nlp.entity.beam_parse([doc],
                                  beam_width=beam_width,
                                  beam_density=beam_density)
    entity_scores: defaultdict = defaultdict(float)
    for score, ents in nlp.entity.moves.get_beam_parses(beams[0]):
        for start, end, label in ents:
            if ((end - start) / doclen <  length_thres):
                continue
            entity_scores[(start, end, label)] += score
    for regex_label in REGEX_ENTITIES:
        doc_text = doc.text
        regex_res = re.search(
            REGEX_ENTITIES[regex_label], doc_text)
        if (regex_res):
            start, end = regex_res.span()
            if ((end - start) / doclen <  length_thres):
                continue
            entity_scores[(start, end, regex_label)] += 1
    return entity_scores


def fuzzy_word_equal(
    word1: str,
    word2: str
) -> float:
    return fuzz.ratio(word1.lower(), word2.lower()) / 100.
