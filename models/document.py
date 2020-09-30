from typing import List, Tuple

from models.spatial_text import Page


# Definition of a Document class
class Document:
    def __init__(self, pages: List[Page]):
        self._pages = pages

    def __repr__(self) -> str:
        return f"<Document with {len(self)} page(s)>"

    def __len__(self) -> int:
        return len(self._pages)

    def __getitem__(self, key: int) -> Page:
        return self._pages[key]

    @property
    def pages(self) -> List[Page]:
        return self._pages
