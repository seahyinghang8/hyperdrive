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
