from pixelator import PixelatorSettings


def test_default_settings():
    s = PixelatorSettings()
    assert s.pixel_size == 8
    assert s.palette is None
    assert s.algorithm == "average"
    assert s.dither is False


def test_custom_settings():
    palette = [(255, 0, 0), (0, 255, 0)]
    s = PixelatorSettings(pixel_size=16, palette=palette, algorithm='median_cut', dither=True)
    assert s.pixel_size == 16
    assert s.palette == palette
    assert s.algorithm == 'median_cut'
    assert s.dither is True