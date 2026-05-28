from PIL import Image
from typing import Union, IO


def load_image(source: Union[str, IO]) -> Image.Image:
    return Image.open(source).convert('RGB')


def save_image(image: Image.Image, destination: Union[str, IO]) -> None:
    image.save(destination)