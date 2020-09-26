# Definition of a Word class
from models.spatial_text import SpatialText

NEGATIVE_VAL_ERROR = "Expected attribute '{}' to be >= 0. Actual value: {}"


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
        return self.text

    def __len__(self) -> int:
        return len(self.text)

    @property
    def text(self) -> str:
        return self._text
