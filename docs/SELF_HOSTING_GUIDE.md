# Pars Linux Welcome - Yerel ve Kapalı Ağ Barındırma Kılavuzu (`SELF_HOSTING_GUIDE.md`)

Bu belge, **Pars Linux Welcome** uygulamasının kurumsal ağlarda, çevrimdışı laboratuvarlarda veya internet erişimi kısıtlı hava boşluklu (air-gapped) ortamlarda yerel sunucular üzerinden nasıl barındırılabileceğini ve yapılandırılabileceğini açıklar.

---

## 🏢 Senaryolar ve Kullanım Alanları

- **Kurumsal İstemciler:** Dış internete çıkışı olmayan şirket içi Pars Linux masaüstü ortamları.
- **Eğitim Kurumları:** Üniversite ve okul laboratuvarlarında yerel paket aynası üzerinden çalışan sistemler.
- **Özel Yansımalar (Local Mirrors):** Yüksek hızlı yerel ağ önbellek sunucuları.

---

## 🛠️ Yapılandırma Adımları

### 1. Yerel Uygulama Kataloğu (`data/apps.json`)
Kapalı ağlarda dış internete (Flathub, Debian repo vb.) erişim olmadığı için, `apps.json` dosyasını yerel intranet aynanızı gösterecek şekilde düzenleyin:

```json
[
  {
    "id": "yerel-editor",
    "name": "Şirket İçi Kod Editörü",
    "category": "development",
    "description": "Yerel GitLab sunucusundan indirilen özel derleme.",
    "pkg_arch": "corp-editor",
    "pkg_debian": "corp-editor",
    "exec": "corp-editor"
  }
]
```

### 2. Yerel Destek Bağlantıları (`data/links.json`)
Dış web siteleri yerine şirket içi wiki, intranet yardım masası ve dokümantasyon adreslerini bağlayın:

```json
[
  {
    "id": "helpdesk",
    "title": "İç BT Destek Masası",
    "desc": "Kurumsal bilet açma ve yardım portalı",
    "icon": "help-browser-symbolic",
    "url": "http://destek.yerel.sirket"
  }
]
```

### 3. Çevrimdışı Paket Kurulum Motoru
`src/core/AppInstaller.py` içerisinde paket kurulumu çağrıldığında sistemin `/etc/pacman.d/mirrorlist` veya `/etc/apt/sources.list` dosyasında tanımlı yerel ayna sunucusu kullanılır:
- `http://mirror.yerel.sirket/parslinux/$repo/os/$arch`

### 4. Kurumsal Duvar Kağıtları Dağıtımı
Şirket logolu duvar kağıtlarını `/usr/share/backgrounds/` veya `/usr/share/parslinux-welcome/data/wallpapers/` altına yerleştirerek tüm istemcilerde standart kurumsal masaüstü deneyimi sağlayabilirsiniz.
