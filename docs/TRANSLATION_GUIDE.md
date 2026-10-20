# Pars Linux Welcome - Çoklu Dil ve Çeviri Kılavuzu (`TRANSLATION_GUIDE.md`)

Pars Linux Welcome, dünya genelindeki tüm kullanıcılara erişebilmek için **GNU gettext** tabanlı güçlü bir yerelleştirme (i18n) altyapısına sahiptir.

Bu kılavuz, var olan çevirileri güncellemeyi ve projeye yeni bir dil eklemeyi adım adım açıklar.

---

## 🗂️ Çeviri Dizin Yapısı

```text
parslinux-welcome/
├── build-i18n.sh             # gettext PO/MO derleme ve güncelleme betiği
├── po/
│   ├── parslinux-welcome.pot # Şablon dosya (tüm çıkarılmış dizgeler)
│   ├── tr.po                 # Türkçe çeviri dosyası
│   └── en.po                 # İngilizce çeviri dosyası
└── data/locale/              # Çalışma zamanında okunan derlenmiş ikili kataloglar
    ├── tr/LC_MESSAGES/parslinux-welcome.mo
    └── en/LC_MESSAGES/parslinux-welcome.mo
```

---

## 🌐 Yeni Bir Dil Ekleme (Örnek: Almanca / de)

### 1. Yeni PO Dosyasını Oluşturun
Şablon dosyasından (`parslinux-welcome.pot`) yeni dil için `.po` dosyası türetin:

```bash
msginit -i po/parslinux-welcome.pot -o po/de.po -l de_DE.UTF-8
```

### 2. Çevirileri Düzenleyin
`po/de.po` dosyasını bir metin düzenleyici veya **Poedit** gibi görsel bir çeviri aracı ile açın:

```po
#: src/ui/pages/PageWelcome.py:15
msgid "Pars Linux'a Hoş Geldiniz"
msgstr "Willkommen bei Pars Linux"
```

### 3. Çevirileri Derleyin
Uygulamanın çevirileri tanıyabilmesi için `.po` dosyalarının ikili `.mo` formatına derlenmesi gerekir. Bunun için sağlanan betiği çalıştırmanız yeterlidir:

```bash
./build-i18n.sh
```

Bu işlem otomatik olarak `data/locale/de/LC_MESSAGES/parslinux-welcome.mo` dosyasını oluşturacaktır.

---

## 🔄 Kaynak Koddaki Değişiklikleri Eşitleme

Kaynak kodlara yeni `_("...")` metinleri eklendiğinde şablonu ve mevcut dilleri güncellemek için:

```bash
# 1. Şablonu güncelle:
xgettext --from-code=UTF-8 --language=Python --keyword=_ \
    -o po/parslinux-welcome.pot \
    src/Main.py src/Config.py src/core/*.py src/ui/*.py src/ui/pages/*.py src/ui/widgets/*.py

# 2. Mevcut dilleri eşitle:
msgmerge -U po/tr.po po/parslinux-welcome.pot
msgmerge -U po/en.po po/parslinux-welcome.pot

# 3. Derle:
./build-i18n.sh
```

---

## 🧪 Çeviriyi Test Etme

Belirli bir dilde uygulamayı yerel olarak test etmek için:

```bash
LANGUAGE=de_DE.UTF-8 ./run.sh
```
veya uygulama içerisindeki "İlk Adımlar" sekmesindeki dil seçici açılır kutusunu kullanabilirsiniz.
