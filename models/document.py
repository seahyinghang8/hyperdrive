from typing import List, Tuple
import os
import pdf2image
try:
    from PIL import Image
except ImportError:
    import Image

from utils.helpers import convert_to_b64_image
from models.spatial_text import Page


# Definition of a Document class
class Document:
    def __init__(self, pages: List[Page], path: str):
        self._path = path
        self._pages = pages
        self._filename = os.path.basename(path)

    def __repr__(self) -> str:
        return f"<Document \'{self._filename}\' with {len(self)} page(s)>"

    def __len__(self) -> int:
        return len(self._pages)

    def __getitem__(self, key: int) -> Page:
        return self._pages[key]

    def as_dict(self) -> dict:
        return {
            'path': self._path,
            'pages': [p.as_dict() for p in self._pages]
        }

    def as_dict_with_images(self) -> dict:
        return {
            'path': self._path,
            'pages': [p.as_dict() for p in self._pages],
            'images': self.b64_images
        }

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def pages(self) -> List[Page]:
        return self._pages

    @property
    def b64_images(self) -> List[str]:
        _, ext = os.path.splitext(self._filename)
        ext = ext[1:].lower()
        if ext in ['jpg', 'png']:
            image = Image.open(self._path)
            return [convert_to_b64_image(image)]
        elif ext in ['pdf']:
            images = pdf2image.convert_from_path(self._path)
            return [convert_to_b64_image(i) for i in images]
        else:
            raise ValueError(f'Extension {ext} should not exist.')
