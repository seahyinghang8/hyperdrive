from collections import defaultdict
from typing import DefaultDict, Tuple

import spacy
from spacy.lang.en import English
from rapidfuzz import fuzz


def get_entity_scores(
    nlp: English,
    doc: spacy.tokens.doc.Doc,
    beam_width: int = 16,
    beam_density: float = 0.0001
) -> DefaultDict[Tuple[int, int, str], float]:
    # calculate NER confidence score using method in this discussion:
    # https://support.prodi.gy/t/displaying-a-confidence-score-next-to-a-user-defined-entity/403/6
    beams = nlp.entity.beam_parse([doc],
                                  beam_width=beam_width,
                                  beam_density=beam_density)
    entity_scores: defaultdict = defaultdict(float)
    for score, ents in nlp.entity.moves.get_beam_parses(beams[0]):
        for start, end, label in ents:
            entity_scores[(start, end, label)] += score
    return entity_scores


def fuzzy_word_equal(
    word1: str,
    word2: str
) -> float:
    return fuzz.ratio(word1.lower(), word2.lower()) / 100.
