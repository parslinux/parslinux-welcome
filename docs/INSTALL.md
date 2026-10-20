# Pars Welcome Kurulum Kılavuzu (`INSTALL.md`)

Bu belge, **Pars Welcome** (`pars-welcome`) uygulamasının bağımlılıklarını, yerel çalıştırma adımlarını ve sisteme kurulumunu açıklar.

---

## 📦 Bağımlılıklar

Pars Welcome, **Python 3**, **GTK4** ve **Libadwaita** üzerine kuruludur.

### 1. Arch Linux / Pars Linux
```bash
sudo pacman -S --needed \
    python \
    python-gobject \
    gtk4 \
    libadwaita
```

### 2. Debian / Ubuntu / Pardus
```bash
sudo apt update
sudo apt install -y \
    python3 \
    python3-gi \
    gir1.2-gtk-4.0 \
    gir1.2-adw-1
```

---

## 🚀 Yerel Olarak Çalıştırma (Geliştirme Modu)

Herhangi bir kurulum yapmadan doğrudan kaynak kodundan çalıştırmak için:

```bash
# Başlatıcı script ile:
./run.sh

# Veya doğrudan:
./pars-welcome
```

---

## ⚙️ Sisteme Kurulum (`install.sh`)

Uygulamayı `/usr/bin`, `/usr/share/parslinux-welcome` ve sistem uygulama menüsüne kurmak için:

```bash
sudo ./install.sh
```

Bu işlem:
1. `src/` ve `data/` dosyalarını `/usr/share/parslinux-welcome/` altına kopyalar.
2. `pars-welcome` komutunu `/usr/bin/pars-welcome` olarak bağlar.
3. Menü simgesini (`.desktop`) `/usr/share/applications/` altına ekler.
4. Vektörel ikonu (`.svg`) `/usr/share/icons/hicolor/scalable/apps/` altına yerleştirir.
5. İkon ve masaüstü veritabanını günceller.

---

## 🗑️ Sistemden Kaldırma (`uninstall.sh`)

Sistemden tamamen temizlemek için:

```bash
sudo ./uninstall.sh
```

---

## 📦 Paket Oluşturma

### Arch / Pars Linux İçin PKGBUILD:
```bash
makepkg -sf
sudo pacman -U parslinux-welcome-*.pkg.tar.zst
```

### Evrensel Paketleme Betiği:
```bash
./build-pkg.sh
```
