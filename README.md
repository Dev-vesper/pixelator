# Pixelator

یه کتابخونهٔ کوچیک و باحال برای تبدیل عکس‌ها به هنر پیکسلی (Pixel Art).  
با چند خط کد ساده می‌تونی هر عکسی رو به سبک بازی‌های قدیمی دربیاری، اندازهٔ پیکسل‌ها رو تنظیم کنی، از پالت رنگ دلخواه استفاده کنی و حتی با الگوریتم‌های مختلف یا دیترینگ ظاهر خروجی رو شخصی‌سازی کنی.

این کتابخونه روی PyPI نیست و قرار هم نیست بشه؛ بنابراین برای استفاده باید مخزن رو کلون کنی و به‌صورت دستی نصب کنی.  
پروژه کاملاً اوپن‌سورسه و هر کسی می‌تونه الگوریتم جدید بهش اضافه کنه یا بهبودش بده.

## فیچرهای اصلی

- سه الگوریتم پیکسلی‌سازی:
  - `average` – سریع و ساده، با میانگین‌گیری رنگ‌ها.
  - `median_cut` – کاهش هوشمند رنگ‌ها با Median Cut.
  - `kmeans` – خوشه‌بندی K‑Means برای ترکیب‌های هنری‌تر.
- پشتیبانی از **پالت رنگ دلخواه** در همهٔ الگوریتم‌ها (مثلاً پالت Game Boy).
- **دیترینگ Floyd‑Steinberg** برای طبیعی‌تر شدن خروجی (مخصوص عکس‌های واقعی).
- پشتیبانی کامل از تصاویر **RGBA** (شفافیت) تا پیکسلی‌سازی با حفظ کانال آلفا.
- **رابط خط فرمان (CLI)** با دستور `pixelate` برای تبدیل مستقیم از ترمینال.
- **تست‌های خودکار** با pytest برای اطمینان از سلامت کد.
- بدون وابستگی سنگین – فقط به Pillow نیاز داره.

## نیازمندی‌ها

- پایتون ۳.۸ به بالا
- Pillow (خودکار نصب می‌شه)

## نصب

۱. مخزن رو کلون کن یا سورس رو دانلود کن و برو توی پوشهٔ اصلی.

۲. یه محیط مجازی بساز و فعالش کن:
```bash
python -m venv venv
venv\Scripts\activate   # ویندوز
source venv/bin/activate   # لینوکس/مک
```

۳. اگه اینترنتت محدودیت داره یا از ایران وصل می‌شی، از یه آینه (mirror) مثل `https://mirror-pypi.runflare.com/simple` استفاده کن و اول پیش‌نیازها رو نصب کن:
```bash
pip install --index-url https://mirror-pypi.runflare.com/simple Pillow setuptools wheel
```

۴. حالا کتابخونه رو به‌صورت editable نصب کن (تا تغییرات بعدی روش اعمال بشه):
```bash
pip install -e . --no-build-isolation
```
اگه اینترنتت بدون مشکله، مستقیم `pip install -e .` کافیه.

## استفاده در کد (Python API)

### تنظیمات
تنظیمات رو با کلاس `PixelatorSettings` مشخص می‌کنی:

| پارامتر      | نوع          | توضیح                                                                 |
|--------------|--------------|-----------------------------------------------------------------------|
| `pixel_size` | `int`        | اندازهٔ هر بلوک پیکسل (پیش‌فرض ۸). عدد بزرگتر مساوی پیکسل‌های درشت‌تر. |
| `palette`    | `list[tuple]` or `None` | لیست رنگ‌های RGB مثل `[(255,0,0), (0,255,0)]`. اگه `None` باشه از رنگ‌های خود تصویر استفاده می‌کنه. |
| `algorithm`  | `str`        | یکی از `'average'`، `'median_cut'` یا `'kmeans'`.                      |
| `dither`     | `bool`       | فعال کردن دیترینگ Floyd‑Steinberg.                                    |

### مثال ساده
```python
from pixelator import Pixelator

p = Pixelator()  # تنظیمات پیش‌فرض (pixel_size=8, algorithm='average', dither=False)
p.pixelate('عکس.jpg', 'خروجی.png')
```

### مثال با پالت و دیترینگ
```python
from pixelator import Pixelator, PixelatorSettings

settings = PixelatorSettings(
    pixel_size=10,
    algorithm='kmeans',
    palette=[(255, 255, 255), (0, 0, 0), (255, 0, 0)],
    dither=True
)
p = Pixelator(settings)
p.pixelate('ورودی.jpg', 'پیکسلی.png')
```

### کار با بافرهای حافظه (BytesIO)
```python
import io
from PIL import Image
from pixelator import Pixelator, PixelatorSettings

img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
in_buf = io.BytesIO()
img.save(in_buf, format='PNG')
in_buf.seek(0)

out_buf = io.BytesIO()
out_buf.name = "output.png"

p = Pixelator(PixelatorSettings(pixel_size=20))
p.pixelate(in_buf, out_buf)

out_buf.seek(0)
result = Image.open(out_buf)
result.save('از-بافر.png')
```

## استفاده از خط فرمان (CLI)

بعد از نصب، دستور `pixelate` در ترمینال در دسترس قرار می‌گیره. می‌تونی مستقیم مسیر عکس رو بدی و تنظیمات رو با پارامترها مشخص کنی.

```bash
pixelate input.jpg output.png --pixel-size 12 --algorithm kmeans --palette 255,0,0;0,255,0;0,0,255 --dither
```

### پارامترهای CLI
- `input` : مسیر عکس ورودی.
- `output` : مسیر عکس خروجی.
- `--pixel-size` : اندازهٔ هر بلوک (پیش‌فرض ۸).
- `--algorithm` : الگوریتم (`average`, `median_cut`, `kmeans`).
- `--palette` : پالت به‌صورت `R,G,B;R,G,B;...` (مثال: `255,0,0;0,255,0`).
- `--dither` : فعال‌سازی دیترینگ (بدون این پرچم غیرفعاله).

اگه `--palette` رو ندی، رنگ‌ها خودکار انتخاب می‌شن.

## ساختار پروژه و توسعه

پروژه با معماری ماژولار طراحی شده تا بتونی راحت الگوریتم جدید اضافه کنی:

```
pixelator/
├── pixelator/
│   ├── __init__.py
│   ├── core.py          # کلاس اصلی Pixelator
│   ├── settings.py      # تنظیمات (PixelatorSettings)
│   ├── algorithms.py    # الگوریتم‌های پیکسلی‌سازی + کارخانه
│   ├── utils.py         # توابع کمکی (بارگذاری، ذخیره، پالت، K‑Means)
│   └── cli.py           # رابط خط فرمان
├── tests/               # تست‌های pytest
├── setup.py
└── README.md
```

### اضافه کردن یه الگوریتم جدید
۱. توی `algorithms.py` یه کلاس جدید بساز که از `PixelationAlgorithm` ارث‌بری کنه و متد `apply` رو پیاده‌سازی کنه:
```python
class MyCoolAlgorithm(PixelationAlgorithm):
    def apply(self, image, pixel_size, palette):
        # منطق تو...
        return processed_image
```
۲. توی `AlgorithmFactory` اسم الگوریتمت رو به دیکشنری `_algorithms` اضافه کن:
```python
_algorithms = {
    "average": AverageColorAlgorithm,
    "median_cut": MedianCutAlgorithm,
    "kmeans": KMeansAlgorithm,
    "cool": MyCoolAlgorithm,
}
```
۳. حالا می‌تونی با `algorithm='cool'` ازش استفاده کنی.

### مشارکت
اگه دوست داری تغییراتت رو به پروژه اضافه کنی:
۱. از مخزن Fork بگیر.
۲. یه شاخهٔ جدید با اسم توصیفی بساز.
۳. تغییرات رو اعمال کن و تست‌ها رو اجرا کن:
   ```bash
   pip install -e .
   pip install pytest
   pytest tests/
   ```
۴. کامیت کن و Push بده.
۵. یه Pull Request به شاخهٔ `main` بفرست.

## تست‌ها

پروژه همراه با تست‌های pytest ارائه می‌شه. برای اجرای اونها:
```bash
pip install pytest
pytest tests/
```
تست‌ها شامل بررسی صحت الگوریتم‌ها، پشتیبانی از پالت، دیترینگ، تصاویر RGBA، بافرها و CLI هستن.

## نکات تکمیلی

- **دیترینگ** باعث می‌شه تغییرات رنگ‌ها نرم‌تر دیده بشه و از حالت مصنوعی کم کنه. مخصوصاً برای عکس‌های طبیعی توصیه می‌شه.
- **پالت رنگ** در همهٔ الگوریتم‌ها کار می‌کنه. اگر پالت بدی، رنگ‌های هر بلوک به نزدیک‌ترین رنگ پالت نگاشت می‌شن.
- در الگوریتم `kmeans` وقتی پالت نداشته باشی، به‌صورت پیش‌فرض ۸ رنگ استخراج می‌کنه. با دادن پالت، تعداد رنگ‌ها برابر طول پالت می‌شه.

## مجوز
این پروژه تحت مجوز MIT منتشر شده. هر جور دوست داری استفاده کن، تغییر بده و به اشتراک بذار.  
مشارکت‌ها با آغوش باز پذیرفته می‌شن.