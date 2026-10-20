# Güvenlik Politikası (`SECURITY.md`)

Pars Linux ekibi olarak kullanıcılarımızın güvenliğini ve sistem bütünlüğünü en üst düzeyde önemsiyoruz.

---

## 🛡️ Desteklenen Sürümler

Aşağıdaki tabloda güvenlik güncellemeleri ve yamaları alan güncel Pars Linux Welcome sürümleri listelenmiştir:

| Sürüm | Destek Durumu |
|---|---|
| `1.0.x` | ✅ Aktif Olarak Destekleniyor |
| `< 1.0.0` | ❌ Desteklenmiyor |

---

## 🔒 Güvenlik Mimarisi ve Ayrıcalık Ayrımı

Pars Linux Welcome, en az ayrıcalık ilkesi (**Principle of Least Privilege**) göz önünde bulundurularak tasarlanmıştır:

1. **Root Olmayan Kullanıcı Ortamı:** Uygulama asla `root` yetkileriyle veya `sudo pars-welcome` olarak çalıştırılmamalıdır. Tamamen standart kullanıcı izinleriyle (`UID >= 1000`) çalışır.
2. **Kabuk ve Kod Enjeksiyon Koruması:** Sistem komutları çalıştırılırken `shell=True` kullanılmaz; `subprocess.Popen` veya `subprocess.run` komut argümanları liste olarak (`['pacman', '-S', ... ]`) verilir.
3. **Pango Markup Güvenliği:** Donanım bilgisi (CPU adı, çekirdek sürümü vb.) arayüzde gösterilmeden önce `GLib.markup_escape_text()` fonksiyonundan geçirilerek XML/Pango arayüz enjeksiyonları önlenir.
4. **Paket Kurulum İzolasyonu:** Bir paket kurulurken sistem kimlik doğrulaması (`sudo` / `polkit`) uygulamanın içinde değil, kullanıcının güvenilir terminal öykünücüsü içinde doğrudan işletim sistemi tarafından sorulur.

---

## 🚨 Güvenlik Açığı Bildirimi (Reporting a Vulnerability)

Pars Linux Welcome uygulamasında potansiyel bir güvenlik açığı tespit ettiyseniz, lütfen bunu herkese açık GitHub Issues üzerinden **yayınlamayın**.

Güvenlik açıklarını güvenli bir şekilde bildirmek için:

1. **E-Posta:** `security@parslinux.org` adresine ayrıntılı bir açıklama gönderin.
2. **GitHub Security Advisory:** Depo üzerindeki "Security" sekmesinden "Report a vulnerability" butonunu kullanarak özel (private) rapor oluşturun.

Lütfen raporunuza şunları ekleyin:
- Güvenlik açığının türü ve etkisi,
- Açığı yeniden oluşturmak için adım adım adımlar (Proof of Concept),
- Etkilenen sistem ve işletim sistemi ortamı.

Güvenlik ekibimiz bildiriminizi en geç **48 saat** içinde yanıtlayacak ve çözüm sürecini başlatacaktır.
