# Pars Welcome (`pars-welcome`)

**Pars Welcome**, Pars Linux kullanıcılarını karşılamak, ilk sistem ayarlarını kolaylaştırmak ve temel uygulamaları hızlıca kurmalarını sağlamak amacıyla geliştirilmiş, **GTK4 ve Libadwaita** tabanlı modern bir karşılama merkezidir.

---

## 🌟 Özellikler

* **Modern Libadwaita Arayüzü:** Akıcı animasyonlar, GNOME HIG uyumlu temiz kart yapısı ve sistemle entegre koyu/açık tema desteği.
* **Sistem Özeti:** Çekirdek (Kernel), Masaüstü Ortamı (DE), CPU, RAM ve Disk bilgilerini tek bakışta sunan özet paneli.
* **İlk Adımlar & Yapılandırma:**
  * Açık / Koyu / Sistem renk şeması geçişi.
  * **Pars Update** entegrasyonu (tek tıkla sistem güncelleme yöneticisi).
  * Ekran çözünürlüğü ve sistem ayarları kısayolları.
  * Sistem yedekleme (Timeshift) aracı başlatıcısı.
* **Önerilen Popüler Uygulamalar:** İnternet, geliştirici araçları, ofis ve multimedya kategorilerinde tek tıkla kurulum ve başlatma.
* **Topluluk & Destek:** Pars Linux web sitesi, forum, Telegram ve GitHub bağlantılarına hızlı erişim.
* **Otomatik Başlatma Yönetimi:** Sistem açılışında karşılama ekranını gösterme/gizleme anahtarı (`~/.config/autostart`).

---

## 🚀 Çalıştırma

```bash
# Projeyi doğrudan başlat:
./pars-welcome
```

---

## 📁 Proje Yapısı

```text
parslinux-welcome/
├── pars-welcome              # Çalıştırılabilir başlatıcı
├── src/
│   ├── Main.py               # Adw.Application & döngü
│   ├── Config.py             # Ayarlar ve dosya yolları
│   ├── core/
│   │   ├── SystemInfo.py     # Donanım ve sistem bilgisi
│   │   ├── DesktopActions.py # Tema ve masaüstü komutları
│   │   ├── AutostartManager.py # Açılışta başlatma yönetimi
│   │   └── AppInstaller.py   # Paket kurulum tetikleyicisi
│   └── ui/
│       ├── MainWindowAdw.py  # Libadwaita ana penceresi
│       └── pages/
│           ├── PageWelcome.py     # Karşılama ve Sistem Özeti
│           ├── PageFirstSteps.py # İlk Adımlar & Araçlar
│           ├── PageApps.py       # Popüler Uygulamalar
│           └── PageCommunity.py  # Topluluk & Bağlantılar
├── data/
│   ├── apps.json             # Popüler yazılımlar listesi
│   ├── links.json            # Topluluk bağlantıları
│   ├── style.css             # Modern CSS geliştirmeleri
│   └── org.parslinux.welcome.desktop
└── README.md
```
