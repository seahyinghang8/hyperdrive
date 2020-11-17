from typing import List, Tuple
import os
import pdf2image
try:
    from PIL import Image
except ImportError:
    import Image

from utils.helpers import convert_to_b64_image
from models.spatial_text import Page, Line, Word


# Definition of a Document class
class Document:
    def __init__(self, pages: List[Page], path: str):
        self._path = path
        self._filename = os.path.basename(path)
        self._pages = pages
        self._pages_concatenated = False

    def __repr__(self) -> str:
        return f"<Document \'{self._filename}\' with {len(self)} page(s)>"

    def __len__(self) -> int:
        return len(self._pages)

    def __getitem__(self, key: int) -> Page:
        return self._pages[key]

    def as_dict(self) -> dict:
        my_dict = {
            'path': self._path,
            'pages': [p.as_dict() for p in self._pages],
            'pages_concatenated': self._pages_concatenated
        }
        if self._pages_concatenated:
            my_dict['concatenated_indices'] = self._concatenated_indices
        return my_dict

    def as_dict_with_images(self) -> dict:
        my_dict = self.as_dict()
        my_dict['images'] = self.b64_images
        return my_dict

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
            if self._pages_concatenated:
                images = self._concatenate_images(images)
            return [convert_to_b64_image(i) for i in images]
        else:
            raise ValueError(f'Extension {ext} should not exist.')

    def _concatenate_images(self, all_images: list) -> list:
        images = [all_images[i] for i in self._concatenated_indices]
        width = images[0].width
        new_height = sum([im.height for im in images])
        new_image = Image.new(images[0].mode, (width, new_height))
        cumulative_height = 0
        for im in images:
            new_image.paste(im, (0, cumulative_height))
            cumulative_height += im.height
        return [new_image]

    def concatenate_pages(self) -> None:
        # if there is only one page, then do not bother
        if len(self._pages) <= 1:
            return
        pages_to_combine = [
            (i, p) for i, p in enumerate(self._pages) if len(p) > 0
        ]
        num_empty_pages = len(pages_to_combine)
        # no point concatenating if all pages are empty
        if num_empty_pages == 0:
            return
        width = pages_to_combine[0][1].width
        pages_to_combine = [
            (i, p) for i, p in pages_to_combine if width == p.width
        ]
        # if any of the non-empty page have different width, then do not concat
        if num_empty_pages != len(pages_to_combine):
            return
        # concat pages
        page_indices = []
        cumulative_height = 0
        lines = []
        for i, page in pages_to_combine:
            lines += [
                Line([
                    word.update_top(word.top + cumulative_height)
                    for word in line.words
                ])
                for line in page.lines
            ]
            cumulative_height += page.height
            page_indices.append(i)

        self._pages = [Page(lines, width, cumulative_height)]
        self._pages_concatenated = True
        self._concatenated_indices = page_indices
