from PIL import Image
from pixelator.algorithms import AlgorithmFactory


def test_average_algorithm():
    img = Image.new('RGB', (40, 40), color=(100, 150, 200))
    algo = AlgorithmFactory.get_algorithm('average')
    result = algo.apply(img, pixel_size=10, palette=None)
    assert result.size == (40, 40)
    assert result.getpixel((0, 0)) == (100, 150, 200)


def test_median_cut_with_palette():
    img = Image.new('RGB', (20, 20), color=(50, 50, 50))
    algo = AlgorithmFactory.get_algorithm('median_cut')
    result = algo.apply(img, pixel_size=5, palette=[(0, 0, 0), (100, 100, 100)])
    assert result.size == (20, 20)
    pixel = result.getpixel((0, 0))
    assert pixel in [(0, 0, 0), (100, 100, 100)]