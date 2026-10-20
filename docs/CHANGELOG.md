# Değişiklik Günlüğü (`CHANGELOG.md`)

Bu proje [Semantic Versioning (SemVer)](https://semver.org/) ilkelerine bağlıdır. Tüm önemli değişiklikler bu belgede belgelenmektedir.

---

## [1.0.0] - 2026-10-20

### 🚀 İlk Kararlı Sürüm (Initial Production Release)

**Pars Linux Welcome** (`parslinux-welcome`), modern GNOME Human Interface Guidelines (HIG) standartlarına uygun olarak GTK4 ve Libadwaita (`Adw 1`) ile sıfırdan inşa edildi.

#### ✨ Eklenen Özellikler

- **Modern Libadwaita Arayüzü:**
  - `Adw.HeaderBar` üzerinde `Adw.ViewSwitcher` ile 4 ana sekme: *Karşılama*, *İlk Adımlar*, *Uygulamalar*, *Topluluk*.
  - Sayfa durum bildirimleri için entegre `Adw.ToastOverlay`.
  - Sistem donanım ve oturum bilgilerini görselleştiren özel `InfoCard` bileşeni (CPU, Bellek doluluk çubuğu, Disk kullanım göstergesi).

- **Evrensel Duvar Kağıdı Modülü (`WallpaperManager`):**
  - Tüm masaüstü ortamlarında çalışan evrensel format desteği (`.png`, `.jpg`, `.svg`, `.webp`).
  - GNOME, KDE Plasma 5/6, XFCE, Cinnamon, MATE, LXQt, Hyprland (`hyprpaper`), Sway (`swaybg`) ve X11 pencere yöneticileri için otomatik tespit ve tek tıkla arka plan uygulama.
  - Özgün 1080p Pars Linux vektörel duvar kağıtları koleksiyonu (`parslinux-leopard-dark.svg`, `parslinux-aurora-light.svg`, `parslinux-sunset-mountain.svg`, `parslinux-minimal-slate.svg`).
  - Kategori filtreleme, arama ve özel dosya seçimi (`Gtk.FileDialog`) sunan tam ekran `WallpaperDialog` galeri penceresi.

- **Çoklu Dil Desteği (i18n):**
  - GNU `gettext` altyapısı üzerine kurulu dinamik dil yönetim motoru (`I18n.py`).
  - Türkçe (TR) ve İngilizce (EN) dil katalogları (`po/` ve `data/locale/`).
  - İlk Adımlar sayfasında anında dil değiştirmeyi sağlayan `Gtk.DropDown` dil seçicisi.
  - Yeni çevirileri güncellemek ve derlemek için `build-i18n.sh` betiği.

- **Önerilen Uygulamalar Kataloğu (`PageApps`):**
  - `data/apps.json` tabanlı kategorili yazılım kataloğu (İnternet, Geliştirme, Üretkenlik, Çoklu Ortam, Grafik).
  - Canlı isim ve açıklama arama motoru (`Gtk.SearchEntry`).
  - Sistemde kurulu olan uygulamaları otomatik algılama ve "Yüklü" rozeti basma.
  - Bağımsız 14 popüler uygulama için yüksek kaliteli SVG simge paketi (`brave-browser`, `google-chrome`, `visual-studio-code`, `docker`, `git`, vb.).
  - Pacman, APT ve Flatpak üzerinden tek tıkla terminalde kurulum mekanizması (`AppInstaller.py`).

- **Görünüm ve Sistem Ayarları:**
  - Açık, Koyu ve Sistem Varsayılanı renk şeması kartları (`Adw.StyleManager` + GNOME `color-scheme` senkronizasyonu).
  - Ekran çözünürlüğü ve HiDPI ölçekleme ayarlarını doğrudan açan kısayol.
  - Pars Update (`pars-update`) entegrasyonu ile tek tıkla paket güncelleme sihirbazı.
  - Oturum açılışında otomatik başlatma seçeneği (`~/.config/autostart`).

- **Tasarım ve Stil:**
  - W3C CSS ve GTK 4.12+ standartlarına uygun `var(--...)` değişkenleri ve `color-mix()` fonksiyonlarıyla sıfır uyarı veren `data/style.css`.
  - Pars Linux origami leopar ve pençe vektörel simgeleri (`org.parslinux.welcome.svg`).

- **Paketleme ve Test:**
  - Arch Linux ve Pars Linux için resmi `PKGBUILD`.
  - Debian ve Arch tabanlı sistemler için tam donanımlı `install.sh` ve `uninstall.sh`.
  - `tests/test_welcome.py` ile birim testleri (6/6 test %100 başarılı).
