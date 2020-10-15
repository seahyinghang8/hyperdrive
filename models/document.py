from typing import List, Tuple

from models.spatial_text import Page


# Definition of a Document class
class Document:
    def __init__(self, filename: str, pages: List[Page]):
        self._filename = filename
        self._pages = pages

    def __repr__(self) -> str:
        return f"<Document \'{self._filename}\' with {len(self)} page(s)>"

    def __len__(self) -> int:
        return len(self._pages)

    def __getitem__(self, key: int) -> Page:
        return self._pages[key]

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def pages(self) -> List[Page]:
        return self._pages
