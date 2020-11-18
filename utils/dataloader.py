import os
import pandas as pd
import yaml
from typing import Any, List, Dict, Tuple
from functools import lru_cache

try:
    from PIL import Image
except ImportError:
    import Image

from models.document import Document
from models.spatial_text import Page

from utils.cluster import cluster_text
from utils.parser import process_image, process_pdf


# Dataloader employs lazy loading
class Dataloader:
    def __init__(self, data_dir: str, label_path: str,
                 concatenate_pages: bool = False,
                 cache_to_disk: bool = False,
                 extensions: List[str] = ['pdf', 'jpg']):
        # param: data_dir - directory containing all the images
        # param: label_path - path to the csv file
        # param: concatenate_pages - if true will combine the non-empty
        #        pages in a single doc into one long page doc
        # param: cache_to_disk - if true will cache document obj in yaml
        # param: extensions is a list of the formats of the input data
        if not os.path.exists(data_dir):
            raise ValueError(f'data_dir \'{data_dir}\' does not exist')
        if not os.path.exists(label_path):
            raise ValueError('label_path provided is not valid')
        if len(extensions) == 0:
            raise ValueError('At least 1 extension is expected')

        self._data_dir = data_dir
        self._label = pd.read_csv(label_path)
        self._extensions = [ext.lower() for ext in extensions]
        self._concatenate_pages = concatenate_pages
        self._cache_to_disk = cache_to_disk

    def _load_data(self, idx: int) -> Tuple[Document, bool, str]:
        # returns the document and a boolean indicating if
        # the document was loaded from a yaml cache
        # and the path of the yaml cache
        label = self._label.iloc[idx].to_dict()
        basename = label['basename']

        yaml_path = os.path.join(self._data_dir, basename + '.yaml')
        if os.path.exists(yaml_path):
            with open(yaml_path) as f:
                doc_dict = yaml.full_load(f)
                doc = Document.from_dict(doc_dict)
            return (doc, True, yaml_path)

        for ext in self._extensions:
            path = os.path.join(self._data_dir, basename + '.' + ext)
            if os.path.exists(path):
                filename = basename + '.' + ext
                doc = None
                # image types
                if ext in ['jpg', 'png']:
                    page_image = Image.open(path)
                    pdf_pages = [
                        Page(
                            lines=cluster_text(
                                process_image(page_image),
                                page_image
                            ),
                            width=page_image.width,
                            height=page_image.height
                        )
                    ]
                    doc = Document(pdf_pages, path, [])
                elif ext in ['pdf']:  # pdf type
                    doc = process_pdf(path)
                    if self._concatenate_pages:
                        doc.concatenate_pages()
                else:
                    raise ValueError(f'Extension {ext} is not accepted.')
                return (doc, False, yaml_path)

        raise ValueError(f'file with basename {basename}\
            ({"|".join(self._extensions)}) cannot be found')

    @lru_cache(maxsize=128)
    def get_document(self, idx: int) -> Document:
        data, from_cache, yaml_path = self._load_data(idx)
        if not from_cache and self._cache_to_disk:
            # cache data to disk
            with open(yaml_path, 'w') as f:
                yaml.dump(data.as_dict(), f)
        return data

    def get_label(self, idx: int) -> dict:
        return self._label.iloc[idx].to_dict()

    def __len__(self) -> int:
        return len(self._label)
