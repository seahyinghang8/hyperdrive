import os
import pandas as pd
from typing import Any, List, Dict
import pdf2image

try:
    from PIL import Image
except ImportError:
    import Image

from models.document import Document
from models.spatial_text import Page

from utils.cluster import cluster_text
from utils.parser import process_image


# Dataloader employs lazy loading
class Dataloader:
    def __init__(self, data_dir: str, label_path: str,
                 extensions: List[str] = ['jpg']):
        # data_dir is the directory containing all the images
        # label_path is the path to the csv file
        # extensions is a list of the formats of the input data
        if not os.path.exists(data_dir):
            raise ValueError(f'data_dir \'{data_dir}\' does not exist')
        if not os.path.exists(label_path):
            raise ValueError('label_path provided is not valid')
        if len(extensions) == 0:
            raise ValueError('At least 1 extension is expected')

        self._data_dir = data_dir
        self._label = pd.read_csv(label_path)
        self._extensions = [ext.lower() for ext in extensions]
        self._cache: Dict[int, dict] = {}

    def _load_data(self, idx: int) -> dict:
        label = self._label.iloc[idx].to_dict()
        basename = label['basename']

        for ext in self._extensions:
            path = os.path.join(self._data_dir, basename + '.' + ext)
            if os.path.exists(path):
                images = []
                # image types
                if ext in ['jpg', 'png']:
                    images = [Image.open(path)]
                elif ext in ['pdf']:
                    images = pdf2image.convert_from_path(path)
                else:
                    raise ValueError(f'Extension {ext} is not accepted.')
                return {'images': images, 'label': label}

        raise ValueError(f'file with basename {basename}\
            ({"|".join(self._extensions)}) cannot be found')

    def get_document(self, idx: int) -> Document:
        if idx in self._cache:
            return self._cache[idx]['document']

        data = self._load_data(idx)
        pdf_pages = [
            Page(
                lines=cluster_text(process_image(page_image), page_image),
                image=page_image
            ) for page_image in data['images']
        ]

        data['document'] = Document(pdf_pages)
        self._cache[idx] = data

        return data['document']

    def get_label(self, idx: int) -> dict:
        if idx in self._cache:
            return self._cache[idx]['label']

        return self._label.iloc[idx].to_dict()

    def __len__(self) -> int:
        return len(self._label)
