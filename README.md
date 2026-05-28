# Pixelator

یه کتابخونهٔ کوچیک و ساده برای تبدیل عکس‌های معمولی به هنر پیکسلی (Pixel Art).  
با چند خط کد می‌تونی عکست رو پیکسلی کنی، اندازهٔ پیکسل‌ها رو تعیین کنی و حتی با الگوریتم‌های مختلف یا دیترینگ ظاهر خروجی رو تغییر بدی.

این کتابخونه روی PyPI منتشر نشده و قرار هم نیست بشه؛ برای همین باید به‌صورت دستی از سورس نصبش کنی.  
پروژه کاملاً اوپن‌سورسه و هر کسی می‌تونه توسعه‌اش بده یا الگوریتم جدید بهش اضافه کنه.

## نیازمندی‌ها

- پایتون ۳.۸ به بالا
- Pillow (خودکار نصب می‌شه، ولی می‌تونی جداگانه هم نصب کنی)

## نصب

۱. مخزن پروژه رو کلون کن یا فایل‌هاش رو دانلود کن و برو توی پوشهٔ اصلی.

۲. یه محیط مجازی بساز (توصیه می‌شه) و فعالش کن:
```bash
python -m venv venv
venv\Scripts\activate   # ویندوز
source venv/bin/activate   # لینوکس/مک
```

۳. اگه اینترنتت محدودیت داره یا از ایران وصل می‌شی، از یه آینه (mirror) مثل `https://mirror-pypi.runflare.com/simple` استفاده کن.  
اول وابستگی‌های اصلی رو با آینه نصب کن:
```bash
pip install --index-url https://mirror-pypi.runflare.com/simple Pillow setuptools wheel
```

۴. حالا خود کتابخونه رو به‌صورت editable نصب کن تا تغییرات بعدی روش اعمال بشه:
```bash
pip install -e . --no-build-isolation
```
گزینهٔ `--no-build-isolation` باعث می‌شه از همون بسته‌هایی که قبلاً در محیط مجازی نصب کردی استفاده کنه و دوباره از اینترنت چیزی دانلود نکنه.

اگه اینترنتت بدون مشکله، کافیه مستقیم بزنی:
```bash
pip install -e .
```
تا هم Pillow و هم setuptools رو از PyPI بگیره.

## استفادهٔ سریع

### تنظیمات (PixelatorSettings)
تنظیمات با یه دیتاکلَس ساده مدیریت می‌شن:

- `pixel_size` (int): اندازهٔ هر بلوک پیکسل (پیش‌فرض ۸). عدد بزرگتر مساوی پیکسل‌های درشت‌تر.
- `palette` (list یا None): یه لیست از رنگ‌های RGB مثل `[(255,0,0), (0,255,0)]`. اگه `None` باشه از همهٔ رنگ‌های تصویر استفاده می‌کنه (الان فقط تو الگوریتم median_cut به‌صورت محدود استفاده می‌شه).
- `algorithm` (str): اسم الگوریتم پیکسلی‌سازی. فعلاً دو تا گزینه داریم: `'average'` و `'median_cut'`.
- `dither` (bool): فعال/غیرفعال کردن دیترینگ Floyd‑Steinberg. وقتی `True` باشه، تغییر رنگ‌ها نرم‌تر دیده می‌شه.

### مثال مینیمال
```python
from pixelator import Pixelator, PixelatorSettings

p = Pixelator()   # با تنظیمات پیش‌فرض (pixel_size=8, algorithm='average', dither=False)
p.pixelate('عکس.jpg', 'خروجی.png')
```

### مثال با تنظیمات دلخواه
```python
settings = PixelatorSettings(
    pixel_size=12,
    algorithm='median_cut',
    dither=True
)
p = Pixelator(settings)
p.pixelate('ورودی.jpg', 'پیکسلی.png')
```

### استفاده با بافرهای حافظه (BytesIO)
متد `pixelate` می‌تونه به‌جای مسیر فایل، از اشیای فایل (مثل `BytesIO`) هم ورودی بگیره و خروجی بده.  
وقتی خروجی رو روی `BytesIO` می‌ریزی، کتابخونه خودش حدس می‌زنه که فرمت PNG می‌خوای (اگه نام فایل نداشته باشه).  
برای اطمینان می‌تونی به بافر یه اسم با پسوند `.png` بدی:
```python
import io
from PIL import Image
from pixelator import Pixelator, PixelatorSettings

# ساخت یک تصویر نمونه در حافظه
img = Image.new('RGB', (100, 100), color='red')
in_buf = io.BytesIO()
img.save(in_buf, format='PNG')
in_buf.seek(0)

out_buf = io.BytesIO()
out_buf.name = "result.png"   # اختیاری، ولی کمکت می‌کنه

p = Pixelator(PixelatorSettings(pixel_size=20))
p.pixelate(in_buf, out_buf)

out_buf.seek(0)
result = Image.open(out_buf)
result.save('از-بافر.png')
```

## ساختار پروژه و توسعه

پروژه طوری طراحی شده که اضافه کردن قابلیت جدید خیلی راحت باشه:

```
pixelator/
├── pixelator/
│   ├── __init__.py
│   ├── core.py
│   ├── settings.py
│   ├── algorithms.py
│   └── utils.py
├── setup.py
└── README.md
```

- **settings.py:** کلاس `PixelatorSettings` رو نگه می‌داره که مثل یک قرارداد بین کاربر و منطق داخلی عمل می‌کنه.
- **algorithms.py:** الگوریتم‌های پیکسلی‌سازی. هر الگوریتم یک کلاس جدا داره که از `PixelationAlgorithm` ارث‌بری می‌کنه.  
  کارخانهٔ `AlgorithmFactory` اسم الگوریتم رو می‌گیره و نمونهٔ مناسب رو می‌سازه.
- **core.py:** کلاس `Pixelator` تنظیمات و الگوریتم رو به هم وصل می‌کنه و عملیات تبدیل رو انجام می‌ده.
- **utils.py:** توابع کمکی برای بارگذاری و ذخیرهٔ تصویر.

### اضافه کردن یک الگوریتم جدید
۱. یه کلاس جدید داخل `algorithms.py` بساز که از `PixelationAlgorithm` ارث‌بری کنه و متد `apply` رو پیاده‌سازی کنه:
```python
class MyCoolAlgorithm(PixelationAlgorithm):
    def apply(self, image, pixel_size, palette):
        # منطق تو...
        return processed_image
```
۲. اسم و کلاس رو به دیکشنری `_algorithms` در `AlgorithmFactory` اضافه کن:
```python
_algorithms = {
    "average": AverageColorAlgorithm,
    "median_cut": MedianCutAlgorithm,
    "cool": MyCoolAlgorithm,
}
```
۳. حالا کاربر می‌تونه توی تنظیمات بنویسه `algorithm='cool'`.

### تست‌ها
پروژه شامل تست‌های خودکار با pytest هست. برای اجرای تست‌ها:
```bash
pip install pytest
pytest tests/
```
تست‌ها موارد زیر رو بررسی می‌کنن:
- درستی تنظیمات پیش‌فرض و سفارشی.
- اجرای هر دو الگوریتم با و بدون پالت.
- تبدیل تصویر از/به فایل و بافر.
- عملکرد کلی `Pixelator` با تنظیمات مختلف (از جمله دیترینگ).

اگه تغییری دادی، حتماً تست‌ها رو دوباره اجرا کن.

## نکات اضافی

- دیترینگ (dither=True) روی تصویر نهایی یه عملیات کوانتیزه و پخش خطا انجام می‌ده که باعث می‌شه پیکسلی‌سازی طبیعی‌تر به نظر برسه، مخصوصاً برای عکس‌های واقعی.
- پالت رنگ هنوز به‌صورت کامل در الگوریتم average پشتیبانی نمی‌شه. می‌تونی این قابلیت رو خودت اضافه کنی.
- کتابخونه هیچ وابستگی سنگینی نداره و فقط از Pillow استفاده می‌کنه.

## مجوز
این پروژه تحت مجوز MIT منتشر شده. هر جور دوست داری استفاده کن، تغییر بده و به اشتراک بذار. مشارکت‌ها با آغوش باز پذیرفته می‌شن.