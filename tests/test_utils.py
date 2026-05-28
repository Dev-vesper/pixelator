import io
from PIL import Image
from pixelator.utils import load_image, save_image, closest_color, apply_palette


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


def test_save_image_to_bytesio():
    img = Image.new('RGB', (3, 3), color=(0, 255, 0))   # full green
    buf = io.BytesIO()
    save_image(img, buf)
    buf.seek(0)
    result = Image.open(buf)
    assert result.getpixel((0, 0)) == (0, 255, 0)


def test_closest_color():
    palette = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    assert closest_color((200, 10, 10), palette) == (255, 0, 0)
    assert closest_color((0, 200, 0), palette) == (0, 255, 0)
    assert closest_color((0, 0, 150), palette) == (0, 0, 255)


def test_apply_palette():
    img = Image.new('RGB', (2, 2), color=(200, 0, 0))   # closer to red
    palette = [(255, 0, 0), (0, 0, 0)]
    result = apply_palette(img, palette)
    assert result.getpixel((0, 0)) == (255, 0, 0)


def test_load_rgba_image():
    img = Image.new('RGBA', (5, 5), color=(10, 20, 30, 128))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    loaded = load_image(buf)
    assert loaded.mode == 'RGBA'
    assert loaded.getpixel((0, 0)) == (10, 20, 30, 128)