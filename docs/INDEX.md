# Pars Linux Welcome - Dokümantasyon İndeksi (`INDEX.md`)

**Pars Linux Welcome** (`pars-welcome`), Pars Linux işletim sistemi için modern, kullanıcı dostu ve hızlı bir karşılama, sistem yapılandırma ve uygulama keşif merkezidir.

Bu dizin, projenin mimarisi, geliştirme standartları, paketleme kılavuzları, güvenlik ilkeleri ve topluluk yönergelerini içeren kapsamlı dokümantasyon haritasıdır.

---

## 🗺️ Dokümantasyon Haritası

### 🚀 Başlangıç ve Temel Bilgiler
* [**README.md**](../README.md): Projeye genel bakış, temel özellikler ve ekran görüntüleri.
* [**CLAUDE.md**](CLAUDE.md): Geliştirici ve yapay zeka asistanları için mimari özet ve komutlar.
* [**INSTALL.md**](INSTALL.md): Bağımlılıklar, yerel çalıştırma, kurulum ve paket oluşturma.
* [**CLI_REFERENCE.md**](CLI_REFERENCE.md): Uçbirimden çalıştırma argümanları, bayraklar ve ortam değişkenleri.
* [**progress.md**](progress.md): Geliştirme süreci, tamamlanan aşamalar ve gelecek yol haritası.

### 🏗️ Mimari ve Yazılım Geliştirme
* [**ARCHITECTURE.md**](ARCHITECTURE.md): GTK4 ve Libadwaita katmanlı yazılım mimarisi, modüller ve veri akışı.
* [**TESTING.md**](TESTING.md): Birim testleri, UI test stratejisi, mock yapıları ve test otomasyonu.
* [**UYGULAMA_BAGLAMA.md**](UYGULAMA_BAGLAMA.md): `apps.json` ve `links.json` veri kataloglarına yeni uygulama veya bağlantı entegrasyonu.
* [**DATA_SAVING_GUIDE.md**](DATA_SAVING_GUIDE.md): Yapılandırma dosyalarının saklanması, XDG Autostart yönetimi ve telemetrisiz veri politikası.

### 📦 Dağıtım, Paketleme ve Özelleştirme
* [**FLATPAK_PACKAGING_GUIDE.md**](FLATPAK_PACKAGING_GUIDE.md): Flatpak manifestosu hazırlama, sandbox izinleri ve Flathub dağıtımı.
* [**FORK.md**](FORK.md): Başka bir Linux dağıtımı veya özel sürüm için projeyi çatallama ve markalama (rebranding) rehberi.
* [**SELF_HOSTING_GUIDE.md**](SELF_HOSTING_GUIDE.md): Kurumsal / kapalı ağlar için ayna, katalog ve duvar kağıdı sunucusu barındırma.
* [**VERSION.md**](VERSION.md): SemVer 2.0 sürüm numaralandırması ve sistem uyumluluk matrisi.
* [**CHANGELOG.md**](CHANGELOG.md): Sürümler arası değişiklikler, eklenen özellikler ve hata düzeltmeleri.

### 🌐 Çeviri ve Topluluk
* [**TRANSLATION_GUIDE.md**](TRANSLATION_GUIDE.md): GNU gettext çoklu dil desteği, POT/PO dosyalarını düzenleme ve derleme.
* [**CONTRIBUTING.md**](CONTRIBUTING.md): Projeye katkı sağlama kuralları, kodlama standartları ve Pull Request süreci.
* [**PAYMENT_INTEGRATION.md**](PAYMENT_INTEGRATION.md): Pars Linux topluluk bağışları, sponsorluk ve fonlama modeli.

### 🛡️ Güvenlik ve Hukuki Şartlar
* [**SECURITY.md**](SECURITY.md): Güvenlik politikası, ayrıcalık sınırları (`pkexec` ayrımı) ve güvenlik açığı bildirme süreci.
* [**TERMS.md**](TERMS.md): Terms of Service and GNU General Public License v3 terms (English).
* [**SARTLAR.md**](SARTLAR.md): Kullanım şartları, garanti sorumluluk reddi ve lisans beyanı (Türkçe).

---

## 📌 Hızlı Gezinme Tablosu

| Konu | Doküman | Hedef Kitle |
|---|---|---|
| Mimarî & Katmanlar | [ARCHITECTURE.md](ARCHITECTURE.md) | Yazılım Geliştiriciler |
| Kurulum & Bağımlılıklar | [INSTALL.md](INSTALL.md) | Sistem Yöneticileri & Kullanıcılar |
| CLI Seçenekleri | [CLI_REFERENCE.md](CLI_REFERENCE.md) | İleri Seviye Kullanıcılar |
| Yeni Uygulama Ekleme | [UYGULAMA_BAGLAMA.md](UYGULAMA_BAGLAMA.md) | Topluluk & Paket Sorumluları |
| Çeviri Yapma | [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) | Çevirmenler |
| Çatallama & Dağıtım | [FORK.md](FORK.md) | Linux Dağıtım Geliştiricileri |
| Güvenlik Politikası | [SECURITY.md](SECURITY.md) | Güvenlik Araştırmacıları |
