from typing import List, Optional


# Definition of a Spatial Text class
# Spatial text are text that contains information
# about their spatial positioning in the document
class SpatialText:
    def __init__(self, left: int, top: int,
                 width: int, height: int):
        self._left: int = left
        self._top: int = top
        self._width: int = width
        self._height: int = height

    @property
    def left(self) -> int:
        return self._left

    @property
    def top(self) -> int:
        return self._top

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width


# Definition of a Word class
class Word(SpatialText):
    def __init__(self, text: str = '', confidence: int = 0,
                 left: int = 0, top: int = 0,
                 width: int = 0, height: int = 0):
        if (left < 0):
            raise ValueError(NEGATIVE_VAL_ERROR.format('left', left))
        if (top < 0):
            raise ValueError(NEGATIVE_VAL_ERROR.format('top', top))
        if (width < 0):
            raise ValueError(NEGATIVE_VAL_ERROR.format('width', width))
        if (height < 0):
            raise ValueError(NEGATIVE_VAL_ERROR.format('height', height))

        super().__init__(left, top, width, height)
        self._text: str = text
        self._confidence: int = confidence

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return "word(" + self.text + ")"

    def __len__(self) -> int:
        return len(self.text)

    @property
    def text(self) -> str:
        return self._text


# Definition of a Line class
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
        return "line(" + ' '.join(self._word_to_str_list()) + ")"

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
