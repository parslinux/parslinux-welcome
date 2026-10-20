# Pars Linux Welcome - Katkı Sağlama Kılavuzu (`CONTRIBUTING.md`)

Pars Linux Welcome projesine katkıda bulunmak istediğiniz için teşekkür ederiz! Açık kaynak topluluğunun desteği sayesinde projemizi geliştirmeye devam ediyoruz.

Bu belge, kod katkıları, hata bildirimleri, çeviri desteği ve tasarım önerilerinde bulunurken takip edilmesi gereken kuralları ve adımları açıklar.

---

## 🧭 Katkı Alanları

1. **Hata Bildirimi (Bug Reports):** Karşılaştığınız beklenmeyen durumları veya çökmeleri GitHub Issues üzerinden bildirin.
2. **Yeni Özellik Önerileri:** Kullanıcı deneyimini artıran fikirler ve yeni fonksiyonlar.
3. **Kod Katkısı:** Hata düzeltmeleri, performans iyileştirmeleri, sürücü tespiti ve modül geliştirmeleri.
4. **Çeviri Desteği:** Yeni diller ekleme veya mevcut çevirileri zenginleştirme (Bkz. [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)).
5. **Uygulama Kataloğu:** `data/apps.json` içerisine popüler ve yararlı açık kaynak yazılımlar önerme (Bkz. [UYGULAMA_BAGLAMA.md](UYGULAMA_BAGLAMA.md)).
6. **Duvar Kağıdı ve Sanat:** Pars Linux topluluğuna uygun özgün vektörel veya yüksek çözünürlüklü duvar kağıtları.

---

## 🛠️ Geliştirme Ortamını Hazırlama

### 1. Depoyu Çatallayın ve Klonlayın
```bash
git clone git@github.com:<kullanici-adiniz>/parslinux-welcome.git
cd parslinux-welcome
```

### 2. Bağımlılıkları Kurun
```bash
# Arch / Pars Linux:
sudo pacman -S --needed python python-gobject gtk4 libadwaita

# Debian / Ubuntu / Pardus:
sudo apt install -y python3 python3-gi gir1.2-gtk-4.0 gir1.2-adw-1
```

### 3. Yeni Bir Dal (Branch) Açın
```bash
git checkout -b feature/yeni-ozellik
# veya
git checkout -b fix/hata-duzeltme
```

---

## 🎨 Kodlama Standartları

- **Python Standartları:** Kodlar [PEP 8](https://peps.python.org/pep-0008/) standartlarına uygun, temiz ve okunabilir olmalıdır.
- **GNOME HIG Uyumu:** Eklenen tüm yeni arayüz bileşenleri Libadwaita tasarım standartlarına (`Adw.PreferencesGroup`, `Adw.ActionRow`, `Adw.Toast`) tam uyumlu olmalıdır.
- **W3C CSS Uyumu:** CSS dosyalarında (`data/style.css`) standart dışı fonksiyonlar yerine modern `var(--...)` değişkenleri ve `color-mix()` tercih edilmelidir.
- **Pango Markup Koruması:** Kullanıcıdan veya sistemden gelen dinamik etiket metinleri `GLib.markup_escape_text(str)` ile sarılmalıdır.
- **Çoklu Dil Desteği:** Kullanıcıya görünen her arayüz metni `_("Metin")` ile gettext sarmalına alınmalıdır.

---

## 🧪 Testleri Çalıştırma

Bir PR göndermeden önce mutlaka birim testlerini ve derleme kontrollerini çalıştırın:

```bash
# Birim testleri:
python3 -m unittest discover tests

# Sözdizimi denetimi:
python3 -m py_compile src/Config.py src/core/*.py src/ui/*.py src/ui/pages/*.py src/Main.py

# Uygulamayı başlatıp görsel olarak inceleyin:
./run.sh
```

---

## 📨 Pull Request (PR) Gönderme

1. Değişikliklerinizi açık ve anlaşılır bir commit mesajıyla işleyin:
   ```bash
   git commit -m "feat(ui): add GPU driver detection row to welcome page"
   ```
2. Dalınızı GitHub'a gönderin:
   ```bash
   git push origin feature/yeni-ozellik
   ```
3. GitHub üzerinde ana depoya (`parslinux/parslinux-welcome`) bir **Pull Request** açın.
4. PR açıklamasında neyin değiştirildiğini, neden yapıldığını ve nasıl test edildiğini özetleyin.
