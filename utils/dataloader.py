import os
import pandas as pd
from typing import Any, List
import pdf2image

try:
    from PIL import Image
except ImportError:
    import Image


# Dataloader employs lazy loading
class Dataloader:
    def __init__(self, data_dir: str, label_path: str,
                 extensions: List[str] = ['jpg']):
        # data_dir is the directory containing all the images
        # label_path is the path to the csv file
        # extensions is a list of the formats of the input data
        if not os.path.exists(data_dir):
            raise ValueError('data_dir provided is not valid')
        if not os.path.exists(label_path):
            raise ValueError('label_path provided is not valid')
        if len(extensions) == 0:
            raise ValueError('extensions need to have at least 1 extension')

        self._data_dir = data_dir
        self._label = pd.read_csv(label_path)
        self._extensions = extensions

    def get_image(self, idx: int) -> Any:
        label_dict = self._label.iloc[idx].to_dict()
        basename = label_dict['basename']

        for ext in self._extensions:
            path = os.path.join(self._data_dir, basename + '.' + ext)
            if os.path.exists(path):
                return (Image.open(path), label_dict)

        raise ValueError(f'file with basename {basename}\
            ({"|".join(self._extensions)}) cannot be found')

    def __getitem__(self, idx: int) -> Any:
        return self.get_image(idx)
