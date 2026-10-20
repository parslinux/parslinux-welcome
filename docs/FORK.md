# Pars Linux Welcome - Çatallama ve Özelleştirme Kılavuzu (`FORK.md`)

Bu kılavuz, **Pars Linux Welcome** uygulamasını kendi Linux dağıtımınız, kurumunuz veya topluluğunuz için nasıl çatallayabileceğinizi (fork), yeniden markalayabileceğinizi (rebranding) ve özelleştirebileceğinizi adım adım açıklar.

---

## 🎨 1. Markalama ve İsim Değişiklikleri (Rebranding)

Uygulamanın adını, logosunu ve kimliğini değiştirmek için aşağıdaki dosyaları güncelleyin:

### A. Sabitler (`src/Config.py`)
`src/Config.py` dosyasını açarak uygulama kimliği ve adını güncelleyin:

```python
APP_ID = "org.sizinprojeniz.welcome"
APP_NAME = "Örnek Dağıtım Welcome"
APP_VERSION = "1.0.0"
```

### B. Masaüstü Başlatıcısı (`data/org.parslinux.welcome.desktop`)
Dosya adını `org.sizinprojeniz.welcome.desktop` olarak değiştirin ve içeriğini güncelleyin:

```ini
[Desktop Entry]
Name=Örnek Dağıtım Karşılama
Comment=Sistemi keşfedin ve özelleştirin
Exec=ornek-welcome
Icon=org.sizinprojeniz.welcome
Type=Application
Categories=GNOME;GTK;Utility;System;
```

### C. Logolar ve Vektörel Simgeler
- `data/org.parslinux.welcome.svg` dosyasını kendi dağıtımınızın SVG vektörel logosuyla değiştirin.
- Hicolor ikon dizinlerini (`data/icons/hicolor/`) kendi logonuzun PNG boyutlarıyla güncelleyin.

---

## 📦 2. Önerilen Uygulamaları Özelleştirme (`data/apps.json`)

Dağıtımınızın kullanıcılarına sunmak istediğiniz yazılımları `data/apps.json` dosyasından düzenleyin:

```json
[
  {
    "id": "firefox",
    "name": "Mozilla Firefox",
    "category": "internet",
    "description": "Gizlilik odaklı, hızlı ve güvenli internet tarayıcısı.",
    "pkg_arch": "firefox",
    "pkg_debian": "firefox-esr",
    "pkg_flatpak": "org.mozilla.firefox",
    "exec": "firefox"
  }
]
```

Kendi depolarınızdaki özel paket adlarını `pkg_arch` veya `pkg_debian` anahtarlarına yazabilirsiniz.

---

## 🔗 3. Topluluk ve Destek Bağlantıları (`data/links.json`)

Forum, web sitesi, sosyal medya ve wiki adreslerinizi `data/links.json` içinde tanımlayın:

```json
[
  {
    "id": "website",
    "title": "Resmi Web Sitesi",
    "desc": "Dağıtım hakkında son haberler ve sürüm duyuruları",
    "icon": "globe-symbolic",
    "url": "https://ornekproje.org"
  }
]
```

---

## 🖼️ 4. Duvar Kağıtları Koleksiyonu (`data/wallpapers/`)

Dağıtımınıza ait varsayılan duvar kağıtlarını `data/wallpapers/` klasörüne ekleyin. Sistem bu klasördeki tüm `.png`, `.jpg`, `.svg` ve `.webp` dosyalarını otomatik olarak tarar ve galeride öne çıkarır.

---

## 📜 5. Lisans ve Dağıtım Koşulları

Pars Linux Welcome, **GNU General Public License v3.0 (GPLv3)** ile lisanslanmıştır. Projeyi çatalladığınızda:
- Kaynak kodlarınızı açık tutmalı,
- Orijinal telif hakkı bildirimlerini korumalı,
- Lisansı GPLv3 olarak muhafaza etmelisiniz.
