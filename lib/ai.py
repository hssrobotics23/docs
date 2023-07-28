import cv2
import requests
from .util import to_ai_url

def gen_results(use_aws_ai, images):
    ai_server_url = to_ai_url(use_aws_ai)
    print(f'Classifier and OCR: {ai_server_url}')

    for (i, img) in enumerate(images):
       bytes = bytearray(cv2.imencode('.png', img)[1])
       files = {'file': ('image.png', bytes, 'image/png', {'Expires': '0'})}
       endpoint = f'{ai_server_url}predict'
       response = requests.post(endpoint, files=files)
       yield response.json()

    print('Done with classifier and OCR!')
