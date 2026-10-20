# Sürüm ve Uyumluluk Politikası (`VERSION.md`)

Bu belge, **Pars Linux Welcome** uygulamasının sürüm numaralandırma şemasını, sürüm döngüsünü ve sistem bileşenleri uyumluluk matrisini açıklar.

---

## 🏷️ Sürüm Numaralandırma Şeması (SemVer 2.0)

Pars Linux Welcome, [SemVer 2.0](https://semver.org/) biçimini (`MAJOR.MINOR.PATCH`) kullanır:

- **MAJOR (Ana Sürüm):** Geriye dönük uyumsuz köklü mimari değişiklikler veya kütüphane yükseltmeleri (Örn: GTK3'ten GTK4'e geçiş).
- **MINOR (Alt Sürüm):** Geriye dönük uyumlu yeni özellikler (Örn: Yeni donanım algılayıcı, yeni duvar kağıdı motoru, yeni dil desteği).
- **PATCH (Yama Sürümü):** Geriye dönük uyumlu hata düzeltmeleri, CSS görsel düzeltmeleri ve çeviri güncellemeleri.

---

## 📊 Sistem Uyumluluk Matrisi

| Bileşen | Minimum Sürüm | Önerilen Sürüm |
|---|---|---|
| **Python** | 3.10 | 3.12+ |
| **GTK4** | 4.10 | 4.20+ (GTK 4.24+) |
| **Libadwaita** | 1.4 | 1.5+ (Adw 1.10+) |
| **PyGObject** | 3.44 | 3.48+ |
| **GNU gettext** | 0.21 | 0.22+ |

---

## 🖥️ Desteklenen Masaüstü Ortamları

Pars Linux Welcome, çoklu masaüstü algılama ve evrensel komut soyutlaması sayesinde aşağıdaki ortamlarda test edilmiş ve tam uyumludur:

| Masaüstü Ortamı | Tema Desteği | Duvar Kağıdı Entegrasyonu |
|---|---|---|
| **GNOME 44+** | ✅ Tam (`gsettings`) | ✅ Tam (`gsettings`) |
| **KDE Plasma 5 / 6** | ✅ Tam (`kdeglobals`) | ✅ Tam (`plasma-apply-wallpaperimage`) |
| **XFCE 4.18+** | ✅ Tam (`xfconf`) | ✅ Tam (`xfconf-query`) |
| **Cinnamon 5+** | ✅ Tam | ✅ Tam (`gsettings`) |
| **MATE 1.26+** | ✅ Tam | ✅ Tam (`gsettings`) |
| **Hyprland / Sway** | ✅ Tam (Adwaita portal) | ✅ Tam (`hyprpaper` / `swaybg`) |
| **X11 Standart (i3, Openbox vb.)** | ✅ Tam | ✅ Tam (`feh` / `nitrogen` / `xwallpaper`) |
