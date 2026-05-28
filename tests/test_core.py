import io
from PIL import Image
from pixelator import Pixelator, PixelatorSettings


def test_pixelate_with_default_settings():
    img = Image.new('RGB', (30, 30), color=(10, 20, 30))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    out_buf = io.BytesIO()
    out_buf.name = "output.png"
    p = Pixelator()
    p.pixelate(buf, out_buf)

    out_buf.seek(0)
    result = Image.open(out_buf)
    assert result.size == (30, 30)
    assert result.mode == 'RGB'


def test_pixelate_with_dither():
    img = Image.new('RGB', (16, 16), color=(128, 128, 128))
    in_buf = io.BytesIO()
    img.save(in_buf, format='PNG')
    in_buf.seek(0)

    out_buf = io.BytesIO()
    settings = PixelatorSettings(pixel_size=4, dither=True)
    out_buf.name = "output.png"
    p = Pixelator(settings)
    p.pixelate(in_buf, out_buf)

    out_buf.seek(0)
    result = Image.open(out_buf)
    assert result.size == (16, 16)