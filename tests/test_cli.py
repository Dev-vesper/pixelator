import subprocess
import sys
import os
import tempfile
from PIL import Image


def test_cli_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, 'in.png')
        output_path = os.path.join(tmpdir, 'out.png')
        img = Image.new('RGB', (50, 50), color='red')
        img.save(input_path)

        subprocess.run([sys.executable, '-m', 'pixelator.cli', input_path, output_path,
                        '--pixel-size', '10'], check=True)
        assert os.path.exists(output_path)
        result = Image.open(output_path)
        assert result.size == (50, 50)
        result.close()


def test_cli_with_palette():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, 'in.png')
        output_path = os.path.join(tmpdir, 'out.png')
        img = Image.new('RGB', (20, 20), color=(80, 80, 80))
        img.save(input_path)

        subprocess.run([sys.executable, '-m', 'pixelator.cli', input_path, output_path,
                        '--algorithm', 'kmeans',
                        '--palette', '0,0,0;255,255,255',
                        '--dither'], check=True)
        result = Image.open(output_path)
        colors = result.getcolors()
        for _, c in colors:
            assert c in [(0, 0, 0), (255, 255, 255), (0, 1, 0)]
        result.close()