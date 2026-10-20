# Pars Welcome (`pars-welcome`) - Geliştirici & Claude Kılavuzu

Pars Linux için GTK4 ve Libadwaita tabanlı modern karşılama ve başlangıç merkezi.

## 📌 Proje Genel Bakışı
- **Dil:** Python 3 (3.10+)
- **Arayüz Kütüphanesi:** GTK4 (`gi.repository.Gtk 4.0`), Libadwaita (`gi.repository.Adw 1`)
- **Tasarım Standartları:** GNOME Human Interface Guidelines (HIG), Adwaita Widgets (`Adw.ViewStack`, `Adw.PreferencesGroup`, `Adw.ActionRow`, `Adw.StatusPage`)
- **Hedef Dağıtım:** Pars Linux (Arch Linux ve Debian/Ubuntu uyumlu)
- **Paket Adı:** `parslinux-welcome` (Binary: `pars-welcome`)

---

## 🏗️ Mimari Yapı
```text
src/
├── Main.py               # Adw.Application ve stil yöneticisi
├── Config.py             # Uygulama sabitleri ve kullanıcı yapılandırması
├── core/                 # İş Mantığı (İşletim sistemi, autostart, donanım, paket yükleyici)
│   ├── SystemInfo.py     # CPU, RAM, Disk, Kernel ve DE bilgisi
│   ├── AutostartManager.py # ~/.config/autostart XDG yönetimi
│   ├── DesktopActions.py # Açık/Koyu tema, Pars Update, URL açma
│   └── AppInstaller.py   # Popüler uygulamaları terminalde kurma
└── ui/                   # Kullanıcı Arayüzü (GTK4 / Libadwaita)
    ├── MainWindowAdw.py  # Ana pencere, HeaderBar, ViewSwitcher
    └── pages/
        ├── PageWelcome.py     # Karşılama ve Sistem Özeti
        ├── PageFirstSteps.py  # İlk Adımlar ve Tema
        ├── PageApps.py        # Önerilen Uygulamalar
        └── PageCommunity.py   # Topluluk ve Dokümantasyon
```

---

## 🛠️ Komutlar ve İş Akışları

### Yerel Çalıştırma
```bash
./run.sh
# veya
./pars-welcome
```

### Testleri Çalıştırma
```bash
python3 -m unittest discover tests
```

### Kod Denetimi (Syntax Check)
```bash
python3 -m py_compile src/Config.py src/core/*.py src/ui/*.py src/ui/pages/*.py src/Main.py
```

### Sisteme Kurulum ve Kaldırma
```bash
sudo ./install.sh
sudo ./uninstall.sh
```

### Paketleme
```bash
# Arch/Pars Linux (PKGBUILD):
makepkg -sf

# Çoklu Paketleme Aracı:
./build-pkg.sh
```

---

## 🎨 Tasarım & Kodlama İlkeleri
1. **Pango Markup Koruması:** `Adw.ActionRow` ve etiketlerde dinamik metinler ayarlanırken `&`, `<`, `>` gibi XML karakterleri her zaman `GLib.markup_escape_text()` ile korunmalıdır.
2. **Karanlık/Aydınlık Tema:** `Adw.StyleManager` ve `org.gnome.desktop.interface color-scheme` senkronize tutulmalıdır.
3. **Core / UI Ayrımı:** Donanım okuma, sistem komutu tetikleme gibi işlemler asla doğrudan UI widget'ı içinde yapılmamalı; `src/core/` altındaki sınıflara delege edilmelidir.
4. **Çoklu Dil Uyum:** Tüm kullanıcı metinleri ilerde gettext entegrasyonuna uygun temiz dizgeler olmalıdır.
