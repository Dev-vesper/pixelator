from .settings import PixelatorSettings
from .algorithms import AlgorithmFactory
from .utils import load_image, save_image
from PIL import Image
from typing import Union, IO


class Pixelator:
    def __init__(self, settings: PixelatorSettings = PixelatorSettings()):
        self.settings = settings

    def pixelate(self, source: Union[str, IO],
                 destination: Union[str, IO]) -> None:
        img = load_image(source)
        algorithm = AlgorithmFactory.get_algorithm(self.settings.algorithm)
        result = algorithm.apply(img, self.settings.pixel_size,
                                self.settings.palette)
        if self.settings.dither:
            result = result.convert('P', dither=Image.FLOYDSTEINBERG,
                                    palette=Image.ADAPTIVE).convert('RGB')
        save_image(result, destination)