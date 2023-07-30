import cv2
import json
import requests
import numpy as np
from pathlib import Path

DALLEE_IMAGE_URL = (
    "https://dgmd-s17-assets.s3.amazonaws.com"
)

def index_urls(index, num_read):

    with open(index, 'r') as rf:
        data = json.load(rf)

    sources = data["images"]
    subset = sources[:num_read]
    return sources if num_read < 0 else subset


def gen_images(src_subset, subpath):

    for src in src_subset:

        image_url = f'{DALLEE_IMAGE_URL}{subpath}' + src["file_name"]
        resp = requests.get(image_url, stream=True).raw
        arr = np.asarray(bytearray(resp.read()), dtype="uint8")
        decoded = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if decoded is None:
            print('Unable to load', image_url)
            continue
        yield decoded[:,:,::-1]

def index_classes(index):

    with open(index, 'r') as rf:
        data = json.load(rf)

    classes = set()
    for path in data[1:]:
        classes.add(Path(path).parent.name)

    return classes
