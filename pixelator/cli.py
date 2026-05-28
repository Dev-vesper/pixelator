import argparse
from pixelator import Pixelator, PixelatorSettings

def parse_palette(palette_str: str):
    colors = []
    for part in palette_str.split(';'):
        try:
            r, g, b = map(int, part.split(','))
            colors.append((r, g, b))
        except Exception:
            raise argparse.ArgumentTypeError(f"Invalid color format: {part}. Use R,G,B")
    return colors

def main():
    parser = argparse.ArgumentParser(description='Pixelate images into pixel art.')
    parser.add_argument('input', help='Input image path')
    parser.add_argument('output', help='Output image path')
    parser.add_argument('--pixel-size', type=int, default=8,
                        help='Size of each pixel block (default: 8)')
    parser.add_argument('--algorithm', choices=['average', 'median_cut', 'kmeans'],
                        default='average', help='Pixelation algorithm (default: average)')
    parser.add_argument('--palette', type=parse_palette,
                        help='Palette colors as R,G,B;R,G,B;... (e.g., 255,0,0;0,255,0)')
    parser.add_argument('--dither', action='store_true',
                        help='Apply Floyd-Steinberg dithering')
    args = parser.parse_args()

    settings = PixelatorSettings(
        pixel_size=args.pixel_size,
        algorithm=args.algorithm,
        palette=args.palette,
        dither=args.dither
    )
    pixelator = Pixelator(settings)
    pixelator.pixelate(args.input, args.output)

if __name__ == '__main__':
    main()