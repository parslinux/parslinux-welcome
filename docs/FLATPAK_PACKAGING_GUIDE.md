# Pars Linux Welcome - Flatpak Paketleme Kılavuzu (`FLATPAK_PACKAGING_GUIDE.md`)

Bu kılavuz, **Pars Linux Welcome** uygulamasının bağımsız bir sandbox paketi olarak **Flatpak** formatında derlenmesini, test edilmesini ve Flathub standartlarına göre dağıtılmasını açıklar.

---

## 📦 Uygulama Tanımlayıcısı (App ID)

- **ID:** `org.parslinux.welcome`
- **Çalışma Zamanı (Runtime):** `org.gnome.Platform` (Sürüm 46 veya 47)
- **Geliştirme Kiti (SDK):** `org.gnome.Sdk`

---

## 📜 Örnek Flatpak Manifestosu (`org.parslinux.welcome.json`)

```json
{
  "app-id": "org.parslinux.welcome",
  "runtime": "org.gnome.Platform",
  "runtime-version": "47",
  "sdk": "org.gnome.Sdk",
  "command": "pars-welcome",
  "finish-args": [
    "--share=ipc",
    "--socket=fallback-x11",
    "--socket=wayland",
    "--share=network",
    "--filesystem=home:ro",
    "--filesystem=xdg-config/autostart:create",
    "--filesystem=/usr/share/backgrounds:ro",
    "--talk-name=org.freedesktop.portal.Desktop",
    "--talk-name=org.freedesktop.portal.Settings",
    "--talk-name=org.freedesktop.portal.Wallpaper"
  ],
  "modules": [
    {
      "name": "parslinux-welcome",
      "buildsystem": "simple",
      "build-commands": [
        "mkdir -p /app/share/parslinux-welcome",
        "cp -r src data /app/share/parslinux-welcome/",
        "install -Dm755 pars-welcome /app/bin/pars-welcome",
        "install -Dm644 data/org.parslinux.welcome.desktop /app/share/applications/org.parslinux.welcome.desktop",
        "install -Dm644 data/org.parslinux.welcome.svg /app/share/icons/hicolor/scalable/apps/org.parslinux.welcome.svg"
      ],
      "sources": [
        {
          "type": "git",
          "url": "https://github.com/parslinux/parslinux-welcome.git",
          "tag": "v1.0.0"
        }
      ]
    }
  ]
}
```

---

## 🛠️ Yerel Olarak Derleme ve Test Etme

### 1. `flatpak-builder` Aracını Kurun
```bash
# Arch Linux:
sudo pacman -S flatpak flatpak-builder

# Ubuntu / Debian:
sudo apt install flatpak flatpak-builder
```

### 2. GNOME Platform Çalışma Zamanını İndirin
```bash
flatpak install flathub org.gnome.Platform//47 org.gnome.Sdk//47
```

### 3. Paketi Derleyin
```bash
flatpak-builder --user --install --force-clean build-dir org.parslinux.welcome.json
```

### 4. Flatpak Paketini Çalıştırın
```bash
flatpak run org.parslinux.welcome
```

---

## ⚠️ Sandbox ve İzin Notları

- **Duvar Kağıdı:** Flatpak kısıtlamaları altındayken duvar kağıdı uygulamak için FreeDesktop `org.freedesktop.portal.Wallpaper` portalı kullanılır.
- **Paket Kurulumu:** Flatpak sandbox içinde doğrudan `pacman` veya `apt` çalıştırılamayacağı için, sistem paketleri yerine `flatpak` veya `xdg-desktop-portal` üzerinden Flatpak uygulama kurulumu tetiklenir.
