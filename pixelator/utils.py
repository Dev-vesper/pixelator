from PIL import Image
from typing import Union, IO, List, Tuple, Optional


def load_image(source: Union[str, IO]) -> Image.Image:
    img = Image.open(source)
    if img.mode in ('RGBA', 'LA', 'PA'):
        img = img.convert('RGBA')
    elif img.mode == 'P':
        img = img.convert('RGBA' if 'transparency' in img.info else 'RGB')
    else:
        img = img.convert('RGB')
    return img


def save_image(image: Image.Image, destination: Union[str, IO],
               format: Optional[str] = None) -> None:
    if format:
        image.save(destination, format=format)
    elif isinstance(destination, str):
        image.save(destination)
    else:
        image.save(destination, format='PNG')


def closest_color(pixel: Tuple[int, ...], palette: List[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    r, g, b = pixel[:3]
    min_dist = float('inf')
    best = palette[0]
    for pr, pg, pb in palette:
        dr = r - pr
        dg = g - pg
        db = b - pb
        dist = dr * dr + dg * dg + db * db
        if dist < min_dist:
            min_dist = dist
            best = (pr, pg, pb)
    return best


def apply_palette(image: Image.Image, palette: List[Tuple[int, int, int]]) -> Image.Image:
    if image.mode == 'RGBA':
        rgb = image.convert('RGB')
        alpha = image.split()[-1]
        mapped = rgb.copy()
        px = mapped.load()
        for y in range(mapped.height):
            for x in range(mapped.width):
                px[x, y] = closest_color(rgb.getpixel((x, y)), palette)
        mapped.putalpha(alpha)
        return mapped
    else:
        mapped = image.copy()
        px = mapped.load()
        for y in range(mapped.height):
            for x in range(mapped.width):
                px[x, y] = closest_color(image.getpixel((x, y)), palette)
        return mapped


def pixelate_alpha_channel(alpha: Image.Image, pixel_size: int) -> Image.Image:
    small = alpha.resize(
        (alpha.width // pixel_size, alpha.height // pixel_size),
        Image.NEAREST
    )
    return small.resize(alpha.size, Image.NEAREST)