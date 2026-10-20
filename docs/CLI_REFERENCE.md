# Pars Linux Welcome - Komut Satırı Başvuru Kılavuzu (`CLI_REFERENCE.md`)

Bu belge, **Pars Linux Welcome** (`pars-welcome`) uygulamasının terminalden çalıştırılması sırasında kullanılabilecek argümanları, seçenekleri ve ortam değişkenlerini açıklar.

---

## 💻 Kullanım Sözdizimi

```bash
pars-welcome [SEÇENEKLER]
```

veya yerel geliştirme ortamında:

```bash
./run.sh [SEÇENEKLER]
# veya
python3 src/Main.py [SEÇENEKLER]
```

---

## ⚙️ Komut Satırı Seçenekleri

| Seçenek | Açıklama |
|---|---|
| `-h`, `--help` | Yardım iletisini ve kullanılabilir komutları ekrana yazdırır ve çıkar. |
| `-v`, `--version` | Uygulamanın kurulu sürüm numarasını (`v1.0.0`) ekrana basar. |
| `--debug` | Konsola ayrıntılı hata ayıklama ve tespit loglarını basar. |
| `--autostart` | Uygulama sistem başlangıcında açıldığında kullanılır; eğer kullanıcı "Başlangıçta Göster" seçeneğini kapattıysa pencere açılmadan sessizce kapanır. |

---

## 🌐 Ortam Değişkenleri (Environment Variables)

Uygulamanın davranışını, dilini veya GTK render motorunu etkilemek için aşağıdaki ortam değişkenleri kullanılabilir:

### 1. Dil Seçimi (`LANG`, `LANGUAGE`, `LC_ALL`)
Arayüz dilini zorlamak için:
```bash
# Türkçe ile başlatma:
LANGUAGE=tr_TR.UTF-8 pars-welcome

# İngilizce ile başlatma:
LANGUAGE=en_US.UTF-8 pars-welcome
```

### 2. GTK CSS ve Hata Ayıklama (`GTK_DEBUG`)
Stil ve arayüz denetimlerini incelemek için:
```bash
# CSS ayrıştırıcı uyarılarını konsola basma:
GTK_DEBUG=css pars-welcome

# GTK Etkileşimli İnceleyiciyi (GTK Inspector) açma:
GTK_DEBUG=interactive pars-welcome
```

### 3. Libadwaita Renk Şeması (`ADW_DISABLE_PORTAL`)
Masaüstü portalı yerine yerel stilleri zorlamak için:
```bash
ADW_DISABLE_PORTAL=1 pars-welcome
```

---

## 💡 Örnek Kullanımlar

### 1. Standart Başlatma
```bash
pars-welcome
```

### 2. Eski Oturumları Temizleyerek Yerel Başlatma
```bash
./run.sh
```

### 3. Oturum Açılışında Çağrılma (XDG Autostart Kuralı)
```bash
pars-welcome --autostart
```
*Not: Bu modda eğer `~/.config/pars-welcome/config.json` dosyasında `autostart: false` ise uygulama kullanıcıyı rahatsız etmeden sonlanır.*
