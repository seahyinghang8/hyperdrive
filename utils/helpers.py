from typing import List, Any
try:
    from PIL import Image
except ImportError:
    import Image

import base64
from io import BytesIO

from models.field import ExtractedField


def flatten(lst: List[List[Any]]) -> List[Any]:
    return [item for sublist in lst for item in sublist]


# convert python image to b64 encoding
def convert_to_b64_image(image: Image) -> str:
    in_mem_file = BytesIO()
    image.save(in_mem_file, format="PNG")
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()
    base64_encoded_result_bytes = base64.b64encode(img_bytes)
    base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
    return base64_encoded_result_str


def extracted_fields_serialized(
    extracted_fields: List[ExtractedField]
) -> list:
    return [
        {
            k: [f.as_dict() for f in fl]
            for (k, fl) in fd.items()
        }
        for fd in extracted_fields
    ]
