from typing import Dict

from models.spatial_text import Line


class FieldScore:
    def __init__(self, weights: Dict[str, float], scores: Dict[str, float]):
        self._weights = weights
        self._scores = scores

    def set_score(self, keyword: str, score: float) -> None:
        self._scores[keyword] = score

    def get_score(self, keyword: str) -> float:
        if keyword in self._scores:
            return self._scores[keyword]
        return 0.

    @property
    def total_score(self) -> float:
        return sum(
            self._weights[key] * self._scores.get(key, 0)
            for key in self._weights
        )


class ExtractedField:
    def __init__(self, index: int, line: Line, score: FieldScore):
        self.index = index
        self.line = line
        self.score = score

    def __repr__(self) -> str:
        out_str = (
            f"field(idx={self.index}, line=\"{self.line}\", "
            f"score={self.score.total_score:.2f})"
        )
        return out_str

    def as_dict(self) -> dict:
        return {
            'line': self.line.as_dict(),
            'index': self.index,
            'scores': self.score._scores,
            'weights': self.score._weights
        }
