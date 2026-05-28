from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from PIL import Image


class PixelationAlgorithm(ABC):
    @abstractmethod
    def apply(self, image: Image.Image, pixel_size: int,
              palette: Optional[List[Tuple[int, int, int]]]) -> Image.Image:
        pass


class AverageColorAlgorithm(PixelationAlgorithm):
    def apply(self, image: Image.Image, pixel_size: int,
              palette: Optional[List[Tuple[int, int, int]]]) -> Image.Image:
        small = image.resize(
            (image.width // pixel_size, image.height // pixel_size),
            Image.NEAREST
        )
        return small.resize(image.size, Image.NEAREST)


class MedianCutAlgorithm(PixelationAlgorithm):
    def apply(self, image: Image.Image, pixel_size: int,
              palette: Optional[List[Tuple[int, int, int]]]) -> Image.Image:
        small = image.resize(
            (image.width // pixel_size, image.height // pixel_size),
            Image.BOX
        )
        if palette:
            small = small.quantize(colors=len(palette), palette=Image.new(
                'P', (1, 1)).quantize(colors=len(palette)))
            small = small.convert('RGB')
        return small.resize(image.size, Image.NEAREST)


class AlgorithmFactory:
    _algorithms = {
        "average": AverageColorAlgorithm,
        "median_cut": MedianCutAlgorithm,
    }

    @classmethod
    def get_algorithm(cls, name: str) -> PixelationAlgorithm:
        return cls._algorithms[name]()