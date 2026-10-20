# Pars Linux Welcome - Uygulama ve Bağlantı Ekleme Kılavuzu (`UYGULAMA_BAGLAMA.md`)

Bu kılavuz, **Pars Linux Welcome** uygulamasının "Uygulamalar" sekmesine yeni yazılımlar eklemeyi ve "Topluluk" sekmesine yeni bağlantılar bağlamayı açıklar.

---

## 📦 1. Yeni Bir Önerilen Uygulama Ekleme (`data/apps.json`)

Önerilen tüm uygulamalar [data/apps.json](file:///home/can/Masaüstü/proje/mcsm/masaüstü/inceleme_düzenleme/parslinux-welcome/data/apps.json) dosyası içinde JSON formatında tutulur.

### JSON Şeması:
```json
{
  "id": "benzersiz_id",
  "name": "Görünen Uygulama Adı",
  "category": "internet | development | productivity | multimedia | graphics",
  "description": "Kullanıcıya gösterilecek kısa açıklama metni.",
  "pkg_arch": "pacman_paket_adi",
  "pkg_debian": "apt_paket_adi",
  "pkg_flatpak": "org.flatpak.UygulamaId",
  "exec": "calistirilabilir_komut_adi",
  "icon": "data/icons/apps/ikon_adi.svg"
}
```

### Örnek Girdi:
```json
{
  "id": "inkscape",
  "name": "Inkscape",
  "category": "graphics",
  "description": "Profesyonel kalitede vektörel grafik çizim ve düzenleme yazılımı.",
  "pkg_arch": "inkscape",
  "pkg_debian": "inkscape",
  "pkg_flatpak": "org.inkscape.Inkscape",
  "exec": "inkscape",
  "icon": "data/icons/apps/inkscape.svg"
}
```

### Alanların Açıklaması:
- **`id`:** Benzersiz kimlik belirteci (küçük harf, alfanümerik).
- **`category`:** Uygulamanın listeleneceği kategori filtresi.
- **`pkg_arch`:** Arch / Pars Linux depolarındaki paket adı (`pacman -S ...`).
- **`pkg_debian`:** Debian / Ubuntu tabanlı sistemlerdeki paket adı (`apt install ...`).
- **`pkg_flatpak`:** (İsteğe bağlı) Flathub üzerindeki Flatpak ID'si.
- **`exec`:** Uygulamanın sistemde kurulu olup olmadığını anlamak için kullanılan komut adı (`which <exec>`).
- **`icon`:** `data/icons/apps/` altına eklenecek yüksek kaliteli SVG simgesinin yolu.

---

## 🎨 2. Uygulama Simgesi Ekleme (`data/icons/apps/`)

- Eklemek istediğiniz uygulamanın vektörel SVG simgesini `data/icons/apps/<id>.svg` olarak kaydedin.
- Simge kare oranlı (örneğin 64x64 veya 128x128 viewBox) ve temiz SVG formatında olmalıdır.
- Simge bulunamadığı durumda sistem varsayılan hicolor ikon temasından otomatik arama yapılır.

---

## 🔗 3. Topluluk ve Destek Bağlantısı Ekleme (`data/links.json`)

[data/links.json](file:///home/can/Masaüstü/proje/mcsm/masaüstü/inceleme_düzenleme/parslinux-welcome/data/links.json) dosyasını açarak yeni bir kart tanımlayın:

```json
{
  "id": "discord",
  "title": "Pars Linux Discord",
  "desc": "Sesli ve yazılı topluluk sohbet sunucumuza katılın",
  "icon": "chat-symbolic",
  "url": "https://discord.gg/parslinux"
}
```

### Alanlar:
- **`id`:** Benzersiz bağlantı kimliği.
- **`title`:** Kart başlığı.
- **`desc`:** Açıklayıcı alt metin.
- **`icon`:** GNOME / Adwaita sembolik simge adı (`globe-symbolic`, `chat-symbolic`, vb.).
- **`url`:** Tıklandığında varsayılan tarayıcıda açılacak web adresi (`https://...`).
