# Pars Linux Welcome - Veri Yönetimi ve Gizlilik Kılavuzu (`DATA_SAVING_GUIDE.md`)

Bu belge, **Pars Linux Welcome** uygulamasının sistemde nereye ve hangi verileri kaydettiğini, veri saklama biçimini, kullanıcı gizliliğini ve telemetrisiz mimarisini açıklar.

---

## 🔒 Gizlilik İlkeleri ve Sıfır Telemetri

1. **Sıfır Telemetri:** Pars Linux Welcome, kullanıcının sisteminden hiçbir donanım bilgisi, IP adresi, tıklama verisi, kullanım istatistiği veya kişisel bilgi **toplamaz**, sunuculara göndermez ve üçüncü taraflarla paylaşmaz.
2. **Çevrimdışı Çalışabilirlik:** İnternet bağlantısı olmasa dahi uygulamanın tüm fonksiyonları (donanım tespiti, duvar kağıdı değişimi, tema yönetimi) eksiksiz çalışır. Yalnızca paket indirme ve topluluk linklerine tıklama aşamalarında ağa erişilir.
3. **Kullanıcı Kontrolü:** Uygulama kullanıcının izni olmadan arka planda hiçbir servis veya arka plan işlemi çalıştırmaz.

---

## 📂 Veri Saklama Konumları

Pars Linux Welcome, **XDG Base Directory Specification** standartlarını sıkı bir şekilde takip eder.

### 1. Kullanıcı Yapılandırması (`~/.config/pars-welcome/config.json`)
Kullanıcının tercihleri (örneğin arayüz dili, seçilen tema modu veya başlangıçta gösterilip gösterilmeyeceği) bu JSON dosyasında saklanır:

```json
{
  "autostart": true,
  "language": "system",
  "theme": "system",
  "last_run": "2026-10-20T19:00:00"
}
```

- **Konum:** `$XDG_CONFIG_HOME/pars-welcome/config.json` (Varsayılan: `~/.config/pars-welcome/config.json`)
- **İzinler:** Yalnızca oturum sahibi kullanıcı (`0600` veya `0644`) tarafından okunabilir ve yazılabilir.

### 2. Oturum Açılışında Otomatik Başlatma (`~/.config/autostart/`)
Kullanıcı "Sistem açılışında göster" seçeneğini aktif bıraktığında:
- **Konum:** `~/.config/autostart/org.parslinux.welcome.desktop`
- Kullanıcı bu seçeneği kapattığında, söz konusu masaüstü başlatıcı dosyası güvenle silinir.

### 3. Kullanıcının Eklediği Duvar Kağıtları (`~/.local/share/backgrounds/` veya `~/Resimler`)
Duvar kağıdı galerisinde "Dosyadan Ekle" butonuna basılarak seçilen duvar kağıtları kullanıcının kendi depolama alanında kalır; kopya oluşturulmaz, doğrudan dosya yoluna referans verilir.

---

## 🧹 Verileri Temizleme ve Sıfırlama

Uygulamanın tüm ayarlarını ve kayıtlı tercihlerini fabrika ayarlarına döndürmek için:

```bash
# Yapılandırmayı ve autostart dosyasını silme:
rm -rf ~/.config/pars-welcome
rm -f ~/.config/autostart/org.parslinux.welcome.desktop
```

Bu işlemden sonra uygulama tekrar çalıştırıldığında sistem varsayılanlarıyla temiz bir açılış yapar.
