try:
    from PIL import Image
except ImportError:
    import Image
import os
import glob
import yaml

from models.document import Document
from models.spatial_text import Word, Line, Page


# convert the bbox into a document YAML in the destination dir
def convert_bbox_to_yaml(
    bbox_dir: str,
    dst_dir: str
) -> None:
    bbox_paths = glob.glob(os.path.join(bbox_dir, '*'))

    for bbox_path in bbox_paths:
        basename, _ = os.path.splitext(os.path.basename(bbox_path))
        image_path = os.path.join(dst_dir, basename + '.jpg')
        yaml_path = os.path.join(dst_dir, basename + '.yaml')

        bbox_lines = []
        with open(bbox_path, 'r') as f:
            bbox_lines = f.readlines()

        lines = []
        for li in bbox_lines:
            line_list = li.rstrip().split(',')
            pos = line_list[0:8]
            text = ','.join(line_list[8:])
            left = int(pos[0])
            right = int(pos[2])
            top = int(pos[1])
            bottom = int(pos[5])
            height = bottom - top

            # assume each character has the same width, estimate the left position for each word
            mean_char_width: float = float(right - left) / len(text)

            words = []
            cumulative_left: float = float(left)

            for word_text in text.split(' '):
                width = mean_char_width * len(word_text)
                new_word = Word(
                    text=word_text,
                    left=int(cumulative_left),
                    top=top,
                    width=int(width),
                    height=height
                )
                words.append(new_word)
                # add the width and the width for one space
                cumulative_left += width + mean_char_width

            lines.append(Line(words))

        image = Image.open(image_path)
        page = Page(lines, image.width, image.height)
        doc = Document([page], image_path, [])

        with open(yaml_path, 'w') as f:
            yaml.dump(doc.as_dict(), f)
