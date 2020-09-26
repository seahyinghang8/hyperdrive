# Definition of a line class
from typing import List, Optional

from models.spatial_text import SpatialText
from models.word import Word


class Line(SpatialText):
    def __init__(self, words: List[Word]):
        super().__init__(0, 0, 0, 0)
        self._words: List[Word] = words
        self._compute_spatial_metadata()

    def append(self, new_word: Word) -> None:
        self._words.append(new_word)
        self._compute_spatial_metadata(new_word)

    def __str__(self) -> str:
        return ' '.join(self._word_to_str_list())

    def __repr__(self) -> str:
        return ' '.join(self._word_to_str_list())

    def __len__(self) -> int:
        return len(self._words)

    def _word_to_str_list(self) -> List[str]:
        return [str(w) for w in self._words]

    def _compute_spatial_metadata(
        self,
        new_word: Optional[Word] = None
    ) -> None:
        if len(self._words) == 0:
            return

        # ensure that all the spatial metadata are initialized
        if new_word and len(self._words) > 1:
            self._left = min(self._left, new_word.left)
            self._top = min(self._top, new_word.top)
            self._width = max(self._width, new_word.right - self.left)
            self._height = max(self._height, new_word.bottom - self.top)
        else:
            self._left = min([w.left for w in self._words])
            self._top = min([w.top for w in self._words])
            self._width = max([w.right - self.left for w in self._words])
            self._height = max([w.bottom - self.top for w in self._words])


    @property
    def words(self) -> List[Word]:
        return self._words
