# Pars Linux Welcome - Test Stratejisi ve Yönergeleri (`TESTING.md`)

Bu belge, **Pars Linux Welcome** uygulamasının kararlılığını, donanım uyumluluğunu ve arayüz güvenliğini doğrulamak için kullanılan test mimarisini, birim testlerini ve test süreçlerini açıklar.

---

## 🧪 Test Mimarisi

Uygulamanın test takımı standart Python kütüphanesi olan `unittest` üzerine inşa edilmiştir.

### Test Katmanları:
1. **Çekirdek Servis Testleri (`src/core/`):**
   - Donanım tespiti (`SystemInfo.py` CPU, RAM, Disk, DE ayrıştırması)
   - Yapılandırma ve Autostart yöneticisi (`AutostartManager.py`, `Config.py`)
   - Evrensel duvar kağıdı motoru (`WallpaperManager.py` dosya uzantısı filtreleri ve komut eşleme)
2. **Arayüz ve Simge Testleri (`src/ui/`):**
   - İkon önbelleği ve güvenli SVG yükleyici (`Icons.py`)
   - Libadwaita tema ve sayfa yapılandırması
3. **Pango & Güvenlik Testleri:**
   - Markup kaçırma (`GLib.markup_escape_text`) kontrolleri
   - CSS sözdizimi ve tema ayrıştırıcı (GtkCssProvider) testleri

---

## 🚀 Testleri Çalıştırma

### 1. Tüm Test Takımını Çalıştırma
```bash
python3 -m unittest discover tests
```

Çıktı örneği:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.048s

OK
```

### 2. Belirli Bir Test Sınıfını Çalıştırma
```bash
python3 -m unittest tests.test_welcome.TestParsWelcome.test_system_info
```

### 3. Ayrıntılı (Verbose) Modda Çalıştırma
```bash
python3 -m unittest -v tests/test_welcome.py
```

### 4. Kod Sözdizimi ve Derleme Denetimi
```bash
python3 -m py_compile src/Config.py src/core/*.py src/ui/*.py src/ui/pages/*.py src/Main.py
```

### 5. GTK CSS Sözdizimi Doğrulama
```bash
GTK_DEBUG=css python3 -c "
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
p = Gtk.CssProvider()
p.load_from_path('data/style.css')
print('CSS valid!')
"
```

---

## 🛠️ Yeni Test Yazma Yönergeleri

Yeni bir modül veya özellik eklendiğinde `tests/test_welcome.py` içine yeni bir test metodu ekleyin:

```python
def test_yeni_ozellik(self):
    """Yeni eklenen servisin doğruluğunu test eder."""
    sonuc = BenimServisim.calistir()
    self.assertIsNotNone(sonuc)
    self.assertTrue(sonuc.get("durum"))
```

- Harici sistem dosyaları (`/etc/os-release`, `~/.config`) test edilirken geçici dizinler (`tempfile.TemporaryDirectory`) kullanılmalıdır.
- Testler sistem donanımından veya aktif masaüstü ortamından bağımsız çalışabilmeli (fail-safe fallback) olmalıdır.
