from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from PIL import Image
from .utils import apply_palette, get_pixels
import random


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
        if palette:
            small = apply_palette(small, palette)
        return small.resize(image.size, Image.NEAREST)


class MedianCutAlgorithm(PixelationAlgorithm):
    def apply(self, image: Image.Image, pixel_size: int,
              palette: Optional[List[Tuple[int, int, int]]]) -> Image.Image:
        small = image.resize(
            (image.width // pixel_size, image.height // pixel_size),
            Image.BOX
        )
        if palette:
            small = apply_palette(small, palette)
        else:
            small = small.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
        return small.resize(image.size, Image.NEAREST)


class KMeansAlgorithm(PixelationAlgorithm):
    def apply(self, image: Image.Image, pixel_size: int,
              palette: Optional[List[Tuple[int, int, int]]]) -> Image.Image:
        small = image.resize(
            (image.width // pixel_size, image.height // pixel_size),
            Image.NEAREST
        )
        k = len(palette) if palette else 8
        quantized = self._kmeans_quantize(small, k)
        if palette:
            quantized = apply_palette(quantized, palette)
        return quantized.resize(image.size, Image.NEAREST)

    def _kmeans_quantize(self, image: Image.Image, k: int) -> Image.Image:
        pixels = get_pixels(image)
        if image.mode == 'RGBA':
            rgb_pixels = [p[:3] for p in pixels]
            alpha = [p[3] for p in pixels]
        else:
            rgb_pixels = list(pixels)
            alpha = None

        if len(rgb_pixels) <= k:
            return image

        random.seed(42)
        centroids = random.sample(rgb_pixels, k)
        for _ in range(10):
            clusters = [[] for _ in range(k)]
            for p in rgb_pixels:
                best_idx = 0
                best_dist = float('inf')
                for i, c in enumerate(centroids):
                    dr = p[0] - c[0]
                    dg = p[1] - c[1]
                    db = p[2] - c[2]
                    dist = dr*dr + dg*dg + db*db
                    if dist < best_dist:
                        best_dist = dist
                        best_idx = i
                clusters[best_idx].append(p)
            new_centroids = []
            for cluster in clusters:
                if cluster:
                    r = sum(p[0] for p in cluster) // len(cluster)
                    g = sum(p[1] for p in cluster) // len(cluster)
                    b = sum(p[2] for p in cluster) // len(cluster)
                    new_centroids.append((r, g, b))
                else:
                    new_centroids.append((0, 0, 0))
            if new_centroids == centroids:
                break
            centroids = new_centroids

        quantized_rgb = []
        for p in rgb_pixels:
            best_idx = 0
            best_dist = float('inf')
            for i, c in enumerate(centroids):
                dr = p[0] - c[0]
                dg = p[1] - c[1]
                db = p[2] - c[2]
                dist = dr*dr + dg*dg + db*db
                if dist < best_dist:
                    best_dist = dist
                    best_idx = i
            quantized_rgb.append(centroids[best_idx])

        out_img = Image.new('RGB', image.size)
        out_img.putdata(quantized_rgb)
        if alpha is not None:
            out_img.putalpha(Image.new('L', image.size))
            out_img.getchannel('A').putdata(alpha)
        return out_img


class AlgorithmFactory:
    _algorithms = {
        "average": AverageColorAlgorithm,
        "median_cut": MedianCutAlgorithm,
        "kmeans": KMeansAlgorithm,
    }

    @classmethod
    def get_algorithm(cls, name: str) -> PixelationAlgorithm:
        if name not in cls._algorithms:
            raise ValueError(f"Unknown algorithm: {name}. Available: {list(cls._algorithms.keys())}")
        return cls._algorithms[name]()