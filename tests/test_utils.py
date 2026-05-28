import io
from PIL import Image
from pixelator.utils import load_image, save_image


def test_load_image_from_path(tmp_path):
    img = Image.new('RGB', (10, 10), color='red')
    path = tmp_path / "test.png"
    img.save(path)
    loaded = load_image(str(path))
    assert loaded.size == (10, 10)
    assert loaded.mode == 'RGB'


def test_save_image(tmp_path):
    img = Image.new('RGB', (5, 5), color='blue')
    path = tmp_path / "out.png"
    save_image(img, str(path))
    assert path.exists()
    reloaded = Image.open(path)
    assert reloaded.getpixel((0, 0)) == (0, 0, 255)