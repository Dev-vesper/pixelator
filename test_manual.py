from pixelator import Pixelator, PixelatorSettings

settings = PixelatorSettings(
    pixel_size=4,          # اندازه‌ی هر بلوک پیکسل (هرچه بزرگتر، پیکسل‌ها درشت‌تر)
    algorithm='average',   # الگوریتم: 'average' یا 'median_cut'
    dither=False           # فعال‌سازی دیترینگ (True/False)
)
p = Pixelator(settings)
p.pixelate('original.png', 'output_pixel.png')