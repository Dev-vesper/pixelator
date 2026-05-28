from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class PixelatorSettings:
    pixel_size: int = 8
    palette: Optional[List[Tuple[int, int, int]]] = None
    algorithm: str = "average"
    dither: bool = False