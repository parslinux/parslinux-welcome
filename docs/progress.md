# Pars Welcome - Geliştirme İlerleme Durumu (`progress.md`)

## 📅 Tarih: 2026-10-20
**Durum:** v1.0.0 İskelet ve Temel Özellikler Tamamlandı ✅

---

### 🚀 Tamamlanan Aşamalar

1. **Mimari Kurulum:**
   - [x] Temiz `welcome` Git dalı yapılandırıldı.
   - [x] GTK4 ve Libadwaita (Adw 1) bağımlılıkları doğrulandı.
   - [x] `core` ve `ui` modüler katman ayrımı yapıldı.

2. **Core (İş Mantığı) Geliştirmesi:**
   - [x] `SystemInfo.py`: OS, Kernel, Masaüstü Ortamı (DE), CPU, RAM ve Disk alanı tespit motoru.
   - [x] `AutostartManager.py`: FreeDesktop XDG `~/.config/autostart` ve JSON yapılandırma yöneticisi.
   - [x] `DesktopActions.py`: Açık/Koyu tema yönetimi (`Adw.StyleManager` + `gsettings`), `pars-update` tetikleyici, sistem yedekleme ve ekran ayarları açıcı.
   - [x] `AppInstaller.py`: Sistem paket yöneticisine (Pacman/APT/Flatpak) göre popüler uygulamaları terminalde kurma desteği.

3. **UI (Arayüz) Bileşenleri:**
   - [x] `MainWindowAdw.py`: Libadwaita `Adw.HeaderBar`, `Adw.ViewSwitcher`, `Adw.ViewStack`, alt araç çubuğu ve About diyaloğu.
   - [x] `PageWelcome.py`: Modern karşılama banner'ı, hızlı aksiyon butonları ve donanım özet kartları.
   - [x] `PageFirstSteps.py`: Renk şeması seçicisi (Açık, Koyu, Sistem), ekran ayarları ve Pars Update butonu.
   - [x] `PageApps.py`: `apps.json` tabanlı kategorili yazılım kataloğu (Brave, VSCode, VLC, LibreOffice vb.) ve dinamik Kur/Başlat kontrolleri.
   - [x] `PageCommunity.py`: Web, forum, Telegram, Wiki ve GitHub yönlendirme kartları.

4. **Veri ve Tasarım Dosyaları:**
   - [x] `data/style.css`: Modern Libadwaita & GTK4 uyumlu stil dosyası. Standart dışı / eski `@define-color`, `alpha()` ve `filter` sözdizimleri, W3C CSS ve GTK 4.12+ standartlarına uygun `var(--...)` değişkenleri ve `color-mix(in srgb, ...)` fonksiyonlarıyla modernize edilerek editör ve tema ayrıştırıcı uyarıları sıfırlandı.
   - [x] `data/org.parslinux.welcome.svg`: Özgün vektörel leopar pençesi ve karşılama rozeti ikonu.
   - [x] `data/org.parslinux.welcome.desktop`: Masaüstü ve autostart standart başlatıcısı.
   - [x] `data/icons/apps/`: 14 popüler uygulama için yüksek kaliteli bağımsız SVG simge paketi.
   - [x] `data/wallpapers/`: Pars Linux temalı özgün 1080p vektörel duvar kağıtları (`parslinux-leopard-dark.svg`, `parslinux-aurora-light.svg`).

5. **Evrensel Duvar Kağıdı ve Kişiselleştirme Modülü:**
   - [x] `WallpaperManager.py`: Yalnızca tüm masaüstü ortamlarında çalışan evrensel formatları (`.png`, `.jpg`, `.svg`, `.webp`) filtreleyip tarayan motor (GNOME-spesifik `.jxl` bağımlılığı kaldırıldı).
   - [x] Evrensel Masaüstü & Pencere Yöneticisi Desteği: GNOME, KDE Plasma 5/6, XFCE, Cinnamon, MATE, LXQt, Hyprland, Sway ve X11 (`feh`/`nitrogen`/`xwallpaper`) için otomatik tespit ve arka plan uygulama desteği.
   - [x] Özgün Pars Linux Koleksiyonu: `parslinux-leopard-dark.svg`, `parslinux-aurora-light.svg`, `parslinux-sunset-mountain.svg`, `parslinux-minimal-slate.svg`.
   - [x] `WallpaperDialog.py`: Kategori filtreleme, arama ve kullanıcının istediği herhangi bir resmi seçip masaüstüne uygulayabileceği "Dosyadan Ekle" butonlu galeri penceresi.
   - [x] `PageFirstSteps.py`: Doğrudan ana sayfadan tıklanabilen 4 Pars Linux duvar kağıdı şeridi ve tam galeri açıcı buton entegrasyonu.

6. **Çoklu Dil Desteği (i18n):**
   - [x] GNU `gettext` altyapısı ve `I18n.py` modülü entegre edildi.
   - [x] Tüm arayüz dizgeleri `_()` ile sarmalandı.
   - [x] `po/parslinux-welcome.pot`, `po/tr.po` ve `po/en.po` dosyaları oluşturuldu.
   - [x] `data/locale/tr` ve `data/locale/en` ikili MO katalogları derlendi.
   - [x] `PageFirstSteps.py`: Sistem varsayılanı, Türkçe ve İngilizce arasında geçiş sağlayan dinamik dil seçici açılır kutusu (`Gtk.DropDown`).
   - [x] `build-i18n.sh`: Çevirileri tek komutla güncelleme ve derleme betiği.

7. **Donanım ve Sürücü Algılama Modülü (`DriverManager.py`):**
   - [x] GPU Tespiti: Intel, NVIDIA, AMD, Sanal Makine (VirtualBox/VMware/QEMU) ekran kartı ve aktif çekirdek sürücüsü tespiti (`i915`, `xe`, `nvidia`, `nouveau`, `amdgpu`).
   - [x] NVIDIA Özel Sürücü Durumu & Önerisi: Açık kaynak `nouveau` tespit edildiğinde tek tıkla özel `nvidia` sürücüsü kurma aksiyonu.
   - [x] Wi-Fi Tespiti: PCI ve USB kablosuz ağ adaptörleri tespiti, aktif çekirdek sürücüsü (`iwlwifi` vb.) ve bağlantı durumu kontrolü.
   - [x] `PageFirstSteps.py` Entegrasyonu: "Donanım ve Sürücüler" tercih grubu altında detaylı sürücü ve bağlantı kartları.

8. **Test & Güvenlik:**
   - [x] Pango markup koruması (`GLib.markup_escape_text`) entegre edildi.
   - [x] `tests/test_welcome.py` ile birim testleri (7 test, %100 başarılı).

---

### 📋 Gelecek Yol Haritası (Sıradaki Adımlar)

- [x] **Sürücü Algılama:** Ekran kartı (Nvidia / AMD / Intel) ve Wi-Fi sürücüsü kontrolü eklenmesi.
- [ ] **Karşılama Turu (Tour Mode):** İlk kez oturum açan kullanıcılar için `Adw.Carousel` tabanlı 3 adımlı hoş geldiniz sihirbazı.
