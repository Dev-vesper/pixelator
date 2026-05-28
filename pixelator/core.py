from .settings import PixelatorSettings
from .algorithms import AlgorithmFactory
from .utils import load_image, save_image, pixelate_alpha_channel
from PIL import Image
from typing import Union, IO


class Pixelator:
    def __init__(self, settings: PixelatorSettings = PixelatorSettings()):
        self.settings = settings

    def pixelate(self, source: Union[str, IO],
                 destination: Union[str, IO]) -> None:
        img = load_image(source)
        has_alpha = img.mode == 'RGBA'

        if has_alpha:
            rgb = img.convert('RGB')
            alpha = img.getchannel('A')
        else:
            rgb = img
            alpha = None

        algorithm = AlgorithmFactory.get_algorithm(self.settings.algorithm)
        result_rgb = algorithm.apply(rgb, self.settings.pixel_size,
                                     self.settings.palette)

        if self.settings.dither:
            pal_img = None
            if self.settings.palette:
                pal_img = Image.new('P', (1, 1))
                flat_palette = [c for color in self.settings.palette for c in color]
                while len(flat_palette) < 768:
                    flat_palette.extend(flat_palette[:3])
                pal_img.putpalette(flat_palette)
            result_rgb = result_rgb.convert('P', dither=Image.Dither.FLOYDSTEINBERG,
                                            palette=pal_img.palette if pal_img else Image.Palette.ADAPTIVE).convert('RGB')

        if has_alpha:
            alpha_pixelated = pixelate_alpha_channel(alpha, self.settings.pixel_size)
            result_rgb.putalpha(alpha_pixelated)

        save_image(result_rgb, destination)