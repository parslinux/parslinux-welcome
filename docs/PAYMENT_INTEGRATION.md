# Pars Linux - Bağış ve Destek Entegrasyon Kılavuzu (`PAYMENT_INTEGRATION.md`)

**Pars Linux**, kâr amacı gütmeyen, bağımsız ve topluluk odaklı bir açık kaynak işletim sistemi projesidir.

Bu belge, Pars Linux projesine yapılabilecek bağış modellerini, sunucu/altyapı finansmanını ve karşılama uygulamasında yer alan destek entegrasyonlarını açıklar.

---

## 🎯 Fonlama Amacı ve Şeffaflık

Toplanan tüm bağış ve sponsorluk gelirleri doğrudan şu alanlarda kullanılır:
1. **Depo ve Yansıma (Mirror) Sunucuları:** Hızlı paket indirmeleri ve ISO dağıtımı için bant genişliği maliyetleri.
2. **Derleme Altyapısı:** CI/CD sunucuları, otomatik paketleme ve test laboratuvarları.
3. **Alan Adları ve Web Hizmetleri:** Forum, Wiki ve dokümantasyon portalları.
4. **Tasarım ve Sanat Çalışmaları:** Simge paketleri, ses temaları ve özgün duvar kağıdı üretimleri.

---

## 💳 Destek Kanalları ve Entegrasyonlar

### 1. GitHub Sponsors
- **Profil:** [github.com/sponsors/parslinux](https://github.com/sponsors/parslinux)
- **Özellikler:** Aylık düzenli veya tek seferlik katkı; rozet ve doğrudan GitHub profilinde destekçi olarak listelenme.

### 2. Patreon / Open Collective
- **Topluluk Fonu:** Şeffaf bütçe yönetimi ve harcama dökümleri topluluk üyeleriyle paylaşılır.

### 3. Kripto Varlıklar (Kullanıcı İsteğine Bağlı)
- Bitcoin (BTC), Ethereum (ETH) ve Monero (XMR) ile merkeziyetsiz bağış desteği.

---

## 🖥️ Karşılama Merkezindeki Entegrasyon (`PageCommunity.py`)

Karşılama uygulamasında kullanıcıları rahatsız edici reklamlar, bağış açılır pencereleri veya zorunlu bildirimler **kesinlikle yer almaz**.

Destek bağlantısı, [PageCommunity.py](file:///home/can/Masaüstü/proje/mcsm/masaüstü/inceleme_düzenleme/parslinux-welcome/src/ui/pages/PageCommunity.py) içerisinde ve `data/links.json` veri dosyasında yer alan şık ve isteğe bağlı bir topluluk kartı olarak sunulur:

```json
{
  "id": "donate",
  "title": "Projeyi Destekleyin",
  "desc": "Pars Linux'un bağımsız kalmasına ve sunucu giderlerine katkıda bulunun.",
  "icon": "emblem-favorite-symbolic",
  "url": "https://parslinux.org/donate"
}
```

Kullanıcı karta tıkladığında sistemin varsayılan web tarayıcısı üzerinden güvenli bağış sayfası açılır.
