from typing import List, Any
import numpy as np
from scipy import spatial
try:
    from PIL import Image
except ImportError:
    import Image

from models.spatial_text import Line, Word
from utils.helpers import flatten


# Cluster the text together
def cluster_text(lines: List[Line], image: Image) -> List[Line]:
    line_clusters: List[Line] = _cluster_words(lines, image)
    return line_clusters


# Break up each line into multiple clustered lines
def _cluster_words(lines: List[Line], image: Image) -> List[Line]:
    params = {
        'threshold': 0.7,
        'position_weight': 0.5,
        'font_size_weight': 0.5,
        'color_weight': 0.
    }

    new_lines: List[List[Line]] = [
        _split_line_into_clusters(line, image, params)
        for line in lines
    ]
    return flatten(new_lines)


# Break up the line into clusters
def _split_line_into_clusters(
    line: Line,
    image: Image,
    params: dict
) -> List[Line]:

    if len(line) == 1:
        return [line]

    first_words: List[Word] = line.words[:-1]
    second_words: List[Word] = line.words[1:]
    scores: List[float] = [
        _score_word_overall(w1, w2, image, params)
        for w1, w2 in zip(first_words, second_words)
    ]
    split_start: List[int] = [
        i + 1 for i, s in enumerate(scores) if s < params['threshold']
    ]
    split_end: List[int] = list(split_start)
    split_start.insert(0, 0)
    split_end.append(len(line))
    new_lines: List[Line] = [
        Line(line.words[start:end])
        for start, end in zip(split_start, split_end)
    ]

    return new_lines


# Score P(word1, word2) belong together from [0, 1]
def _score_word_overall(
    word1: Word,
    word2: Word,
    image: Image,
    params: dict
) -> float:
    pos_score = _score_word_position(word1, word2) * params['position_weight']
    font_size_score = _score_word_font_size(word1, word2) * \
        params['font_size_weight']
    # color_score = _score_word_color(word1, word2, image) * \
    #     params['color_weight']

    overall_score = pos_score + font_size_score
    return overall_score


# Score P(word1, word2) are together using position
def _score_word_position(word1: Word, word2: Word) -> float:
    # high likelihood that w1 and w2 are from
    # the same cluster if the dist < 2 * avg_width
    # likelihood linearly decreases from 2x to 6x
    avg_width: float = word1.mean_char_width
    dist = word2.left - word1.right
    if dist < 2 * avg_width:
        return 1.
    elif dist < 6 * avg_width:
        frac = (dist - 2 * avg_width) / (4 * avg_width)
        return 1. - frac
    else:
        return 0.


# Score P(word1, word2) are together using font size
def _score_word_font_size(word1: Word, word2: Word) -> float:
    # high likelihood if w1 and w2 share similar sizes
    width_ratio = word1.mean_char_width / word2.mean_char_width
    height_ratio = word1.height / word2.height

    if width_ratio > 1.:
        width_ratio = 1. / width_ratio
    if height_ratio > 1.:
        height_ratio = 1. / height_ratio

    return (width_ratio + height_ratio) / 2.


# Score P(word1, word2) are together using color
def _score_word_color(word1: Word, word2: Word, image: Image) -> float:
    return 1. - spatial.distance.cosine(
        _get_color_hist(
            image, word1.left, word1.top,
            word1.height, word1.width),
        _get_color_hist(
            image, word2.left, word2.top,
            word2.height, word2.width)
    )


def _get_color_hist(
    image: Image,
    left: int,
    top: int,
    height: int,
    width: int
) -> Any:
    mask = np.zeros((int(image.size[1]), int(image.size[0])))
    mask[top: top + height, left: left + width] = np.ones((height, width))
    return image.histogram(Image.fromarray(np.uint8(255 * mask)))
