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
   - [x] `data/style.css`: Modern gölgeler, kart borderları ve accent renkleri.
   - [x] `data/org.parslinux.welcome.svg`: Özgün vektörel leopar pençesi ve karşılama rozeti ikonu.
   - [x] `data/org.parslinux.welcome.desktop`: Masaüstü ve autostart standart başlatıcısı.

5. **Test & Güvenlik:**
   - [x] Pango markup koruması (`GLib.markup_escape_text`) entegre edildi.
   - [x] `tests/test_welcome.py` ile birim testleri yazıldı (4 test, %100 başarılı).

---

### 📋 Gelecek Yol Haritası (Sıradaki Adımlar)

- [ ] **Dahili Duvar Kağıdı Seçicisi:** Pardus/Mint tarzında önceden tanımlı Pars Linux duvar kağıtlarını seçebilme galerisi.
- [ ] **Çoklu Dil Desteği (i18n):** `gettext` altyapısı ile Türkçe ve İngilizce PO/MO dosyalarının bağlanması.
- [ ] **Sürücü Algılama:** Ekran kartı (Nvidia / AMD) ve Wi-Fi sürücüsü kontrolü eklenmesi.
- [ ] **Karşılama Turu (Tour Mode):** İlk kez oturum açan kullanıcılar için `Adw.Carousel` tabanlı 3 adımlı hoş geldiniz sihirbazı.
