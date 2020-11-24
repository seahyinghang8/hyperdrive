from typing import List, Tuple, Optional, Dict, Any


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

    @property
    def center_left(self) -> int:
        return int(self.left + self.width / 2)

    @property
    def center_top(self) -> int:
        return int(self.top + self.height / 2)


NEGATIVE_VAL_ERROR = "Expected attribute '{}' to be >= 0. Actual value: {}"


# Definition of a Word class
class Word(SpatialText):
    def __init__(self, text: str = '', c: float = 1.,
                 left: int = 0, top: int = 0,
                 width: int = 0, height: int = 0,
                 ft: int = -1):
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
        self._font_type: int = ft
        self._confidence: float = c

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return "word(" + self.text + ")"

    def __len__(self) -> int:
        return len(self.text)

    def as_dict(self) -> dict:
        return {
            'text': self.text,
            'left': self.left,
            'top': self.top,
            'width': self.width,
            'height': self.height,
            'c': self._confidence,
            'ft': self._font_type,
        }

    @classmethod
    def from_dict(cls, word_dict: dict):  # type: ignore
        return cls(**word_dict)

    def update_top(self, new_top: int):  # type: ignore
        self._top = new_top
        return self

    @property
    def text(self) -> str:
        return self._text

    @property
    def mean_char_width(self) -> float:
        return float(self.width) / len(self)


class LineIterator:
    def __init__(self, words: List[Word]):
        self._words = words
        self._index = 0

    def __next__(self) -> Word:
        if self._index >= len(self._words):
            raise StopIteration

        next_word = self._words[self._index]
        self._index += 1
        return next_word


# Definition of a Line class
class Line(SpatialText):
    def __init__(self, words: List[Word]):
        super().__init__(0, 0, 0, 0)
        self._words: List[Word] = words
        self._compute_spatial_metadata()

    def append(self, new_word: Word) -> None:
        self._words.append(new_word)
        self._compute_spatial_metadata(new_word)

    def as_dict(self) -> dict:
        return {'words': [w.as_dict() for w in self.words]}

    @classmethod
    def from_dict(cls, line_dict: dict):  # type: ignore
        return cls([Word.from_dict(w) for w in line_dict['words']])

    def __str__(self) -> str:
        return ' '.join(self._word_to_str_list())

    def __repr__(self) -> str:
        return "line(" + ' '.join(self._word_to_str_list()) + ")"

    def __len__(self) -> int:
        return len(self._words)

    def __getitem__(self, key: int) -> Word:
        return self._words[key]

    def __iter__(self) -> LineIterator:
        return LineIterator(self._words)

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


class BlockIterator:
    def __init__(self, lines: List[Line]):
        self._lines = lines
        self._index = 0

    def __next__(self) -> Line:
        if self._index >= len(self._lines):
            raise StopIteration

        next_line = self._lines[self._index]
        self._index += 1
        return next_line


# Definition of a Block class
class Block(SpatialText):
    def __init__(self, lines: List[Line]):
        super().__init__(0, 0, 0, 0)
        self._lines: List[Line] = lines
        self._compute_spatial_metadata()

    def append(self, new_line: Line) -> None:
        self._lines.append(new_line)
        self._compute_spatial_metadata(new_line)

    def __str__(self) -> str:
        return ' '.join(self._line_to_str_list())

    def __repr__(self) -> str:
        return "block(" + ' '.join(self._line_to_str_list()) + ")"

    def __len__(self) -> int:
        return len(self._lines)

    def __getitem__(self, key: int) -> Line:
        return self._lines[key]

    def __iter__(self) -> BlockIterator:
        return BlockIterator(self._lines)

    def _line_to_str_list(self) -> List[str]:
        return [str(line) for line in self._lines]

    def _compute_spatial_metadata(
        self,
        new_line: Optional[Line] = None
    ) -> None:
        if len(self._lines) == 0:
            return

        # ensure that all the spatial metadata are initialized
        if new_line and len(self._lines) > 1:
            self._left = min(self._left, new_line.left)
            self._top = min(self._top, new_line.top)
            self._width = max(self._width, new_line.right - self.left)
            self._height = max(self._height, new_line.bottom - self.top)
        else:
            self._left = min([w.left for w in self._lines])
            self._top = min([w.top for w in self._lines])
            self._width = max([w.right - self.left for w in self._lines])
            self._height = max([w.bottom - self.top for w in self._lines])

    @property
    def lines(self) -> List[Line]:
        return self._lines


# Definition of a Page class
class Page(SpatialText):
    def __init__(self, lines: List[Line], width: int, height: int):
        super().__init__(0, 0, width, height)
        self._lines = lines
        self._compute_page_metadata()
        self._compute_spatial_metadata()

    def _compute_spatial_metadata(self) -> None:
        if len(self._lines) == 0:
            return

        # ensure that all the spatial metadata are initialized
        self._left = min([ln.left for ln in self._lines])
        self._top = min([ln.top for ln in self._lines])
        self._text_width = max([ln.right - self.left for ln in self._lines])
        self._text_height = max([ln.bottom - self.top for ln in self._lines])

    def _compute_page_metadata(self) -> None:
        if len(self._lines) == 0:
            return

        self._left_pos: List[Tuple[int, int]]
        self._top_pos: List[Tuple[int, int]]

        self._center_left_pos: List[Tuple[int, int]]
        self._center_top_pos: List[Tuple[int, int]]


        line_pos = [
            ((line.left, i),
             (line.top, i),
             (line.center_left, i),
             (line.center_top, i)
            )
            for i, line in enumerate(self._lines)
        ]
        left_pos_t, top_pos_t, center_left_t, center_top_t = zip(*line_pos)

        self._left_pos = sorted(left_pos_t, key=lambda x: x[0])
        self._top_pos = sorted(top_pos_t, key=lambda x: x[0])
        self._center_left_pos = sorted(center_left_t, key=lambda x: x[0])
        self._center_top_pos = sorted(center_top_t, key=lambda x: x[0])

    def __getitem__(self, key: int) -> Line:
        return self._lines[key]

    def __repr__(self) -> str:
        return f"<Page with {len(self)} line(s)>"

    def __len__(self) -> int:
        return len(self._lines)

    def as_dict(self) -> dict:
        return {
            'lines': [
                line.as_dict()
                for line in self.lines
            ],
            'width': self.width,
            'height': self.height
        }

    @classmethod
    def from_dict(cls, page_dict: dict):  # type: ignore
        return cls(
            lines=[Line.from_dict(li) for li in page_dict['lines']],
            width=page_dict['width'],
            height=page_dict['height']
        )

    @property
    def lines(self) -> List[Line]:
        return self._lines

    @property
    def left_pos(self) -> List[Tuple[int, int]]:
        return self._left_pos

    @property
    def top_pos(self) -> List[Tuple[int, int]]:
        return self._top_pos

    @property
    def center_left_pos(self) -> List[Tuple[int, int]]:
        return self._center_left_pos

    @property
    def center_top_pos(self) -> List[Tuple[int, int]]:
        return self._center_top_pos

    @property
    def text_width(self) -> int:
        return self._text_width

    @property
    def text_height(self) -> int:
        return self._text_height
