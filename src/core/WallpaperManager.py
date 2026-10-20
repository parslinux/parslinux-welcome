#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
from pathlib import Path
from src.Config import get_data_path, load_config, save_config
from src.core.SystemInfo import SystemInfo

# Yalnızca tüm Linux masaüstü ortamlarında (GNOME, KDE, XFCE, vb.) evrensel olarak desteklenen formatlar
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.svg')

class WallpaperManager:
    """Evrensel masaüstü ortamları (GNOME, KDE, XFCE, Cinnamon, MATE, LXQt, Wayland/Hyprland/Sway, X11) için duvar kağıdı yöneticisi."""

    @classmethod
    def get_available_wallpapers(cls) -> list[dict]:
        """
        Pars Linux ile gelen özgün duvar kağıtlarını ve sistemdeki evrensel resimleri listeler.
        Dönen liste öğeleri: {'id': str, 'name': str, 'path': str, 'category': str, 'is_bundled': bool}
        """
        wallpapers = []
        seen_paths = set()

        # 1. Pars Linux Dahili Evrensel Vektörel Duvar Kağıtları
        bundled_dir = get_data_path("wallpapers")
        if os.path.exists(bundled_dir):
            for fname in sorted(os.listdir(bundled_dir)):
                if fname.lower().endswith(VALID_EXTENSIONS):
                    p = os.path.abspath(os.path.join(bundled_dir, fname))
                    if p not in seen_paths:
                        seen_paths.add(p)
                        clean_name = (
                            fname.rsplit(".", 1)[0]
                            .replace("parslinux-", "")
                            .replace("-", " ")
                            .replace("_", " ")
                            .title()
                        )
                        wallpapers.append({
                            "id": fname,
                            "name": f"Pars {clean_name}",
                            "path": p,
                            "category": "Pars Linux",
                            "is_bundled": True
                        })

        # 2. Kullanıcının Eklediği Özel Duvar Kağıtları
        cfg = load_config()
        for custom_path in cfg.get("custom_wallpapers", []):
            if os.path.exists(custom_path) and custom_path not in seen_paths:
                seen_paths.add(custom_path)
                fname = os.path.basename(custom_path)
                clean_name = fname.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()
                wallpapers.append({
                    "id": fname,
                    "name": clean_name,
                    "path": custom_path,
                    "category": "Özel",
                    "is_bundled": False
                })

        # 3. Sistem Arka Plan Dizinleri (Yalnızca evrensel .png, .jpg, .svg)
        search_dirs = [
            ("/usr/share/backgrounds", "Sistem"),
            ("/usr/share/wallpapers", "Koleksiyon"),
            (str(Path.home() / "Resimler" / "Wallpapers"), "Kullanıcı"),
            (str(Path.home() / "Pictures" / "Wallpapers"), "Kullanıcı")
        ]

        for base_dir, default_cat in search_dirs:
            if not os.path.exists(base_dir):
                continue
            for root, dirs, files in os.walk(base_dir):
                if "/." in root:
                    continue
                rel_sub = os.path.relpath(root, base_dir)
                category = default_cat if rel_sub == "." else rel_sub.capitalize()

                for f in sorted(files):
                    if f.lower().endswith(VALID_EXTENSIONS):
                        full_path = os.path.abspath(os.path.join(root, f))
                        if full_path not in seen_paths:
                            seen_paths.add(full_path)
                            clean_name = f.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()
                            wallpapers.append({
                                "id": f,
                                "name": clean_name,
                                "path": full_path,
                                "category": category,
                                "is_bundled": False
                            })

        return wallpapers

    @classmethod
    def get_current_wallpaper(cls) -> str:
        """Şu anda aktif olan masaüstü duvar kağıdının yolunu döner."""
        de = SystemInfo.get_desktop_environment().lower()

        try:
            # 1. GNOME / Cosmic / Budgie
            if any(x in de for x in ["gnome", "unity", "budgie", "cosmic"]):
                cmd = ["gsettings", "get", "org.gnome.desktop.background", "picture-uri"]
                out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
                uri = out.strip("'\"")
                if uri.startswith("file://"):
                    return uri[7:]
                if uri:
                    return uri

            # 2. Cinnamon
            elif "cinnamon" in de:
                cmd = ["gsettings", "get", "org.cinnamon.desktop.background", "picture-uri"]
                out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
                uri = out.strip("'\"")
                if uri.startswith("file://"):
                    return uri[7:]
                if uri:
                    return uri

            # 3. MATE
            elif "mate" in de:
                cmd = ["gsettings", "get", "org.mate.background", "picture-filename"]
                out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
                return out.strip("'\"")

            # 4. XFCE
            elif "xfce" in de:
                cmd = ["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace0/last-image"]
                out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
                if out:
                    return out

        except Exception as e:
            print(f"Mevcut duvar kağıdı okunamadı: {e}")

        # Yapılandırmadaki kayıtlı duvar kağıdı fallback'i
        cfg = load_config()
        last_wp = cfg.get("last_wallpaper", "")
        if last_wp and os.path.exists(last_wp):
            return last_wp

        return ""

    @classmethod
    def add_custom_wallpaper(cls, file_path: str) -> bool:
        """Kullanıcının harici olarak seçtiği resmi yapılandırmaya ekler."""
        if not os.path.exists(file_path):
            return False
        abs_path = os.path.abspath(file_path)
        cfg = load_config()
        custom_list = cfg.get("custom_wallpapers", [])
        if abs_path not in custom_list:
            custom_list.insert(0, abs_path)
            cfg["custom_wallpapers"] = custom_list
            save_config(cfg)
        return True

    @classmethod
    def set_wallpaper(cls, image_path: str) -> bool:
        """
        Evrensel Masaüstü Duvar Kağıdı Ayarlayıcısı:
        GNOME, KDE Plasma, XFCE, Cinnamon, MATE, LXQt, Hyprland, Sway ve X11 ortamlarında
        arka planı tek tıkla uygular.
        """
        if not os.path.exists(image_path):
            print(f"Duvar kağıdı dosyası bulunamadı: {image_path}")
            return False

        abs_path = os.path.abspath(image_path)
        file_uri = f"file://{abs_path}"
        de = SystemInfo.get_desktop_environment().lower()
        applied = False

        # 1. GNOME / Budgie / Cosmic / Pop OS
        if any(x in de for x in ["gnome", "unity", "budgie", "cosmic"]):
            try:
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", file_uri], check=False)
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", file_uri], check=False)
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-options", "zoom"], check=False)
                applied = True
            except Exception as e:
                print(f"GNOME gsettings hatası: {e}")

        # 2. KDE Plasma 5 & 6
        elif "kde" in de or "plasma" in de:
            if shutil.which("plasma-apply-wallpaperimage"):
                res = subprocess.run(["plasma-apply-wallpaperimage", abs_path], check=False)
                applied = (res.returncode == 0)
            if not applied:
                js_script = f"""
                for (var i = 0; i < desktops().length; i++) {{
                    var d = desktops()[i];
                    d.wallpaperPlugin = "org.kde.image";
                    d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                    d.writeConfig("Image", "{file_uri}");
                }}
                """
                res = subprocess.run(["qdbus", "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", js_script], check=False)
                applied = (res.returncode == 0)

        # 3. XFCE (Tüm monitör ve çalışma alanları)
        elif "xfce" in de:
            try:
                props_out = subprocess.check_output(
                    ["xfconf-query", "-c", "xfce4-desktop", "-l"],
                    stderr=subprocess.DEVNULL
                ).decode()
                for line in props_out.splitlines():
                    if "last-image" in line or "image-path" in line:
                        subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-p", line, "-s", abs_path], check=False)
                applied = True
            except Exception:
                subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/workspace0/last-image", "-s", abs_path], check=False)
                applied = True

        # 4. Cinnamon
        elif "cinnamon" in de:
            try:
                subprocess.run(["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", file_uri], check=False)
                applied = True
            except Exception:
                pass

        # 5. MATE
        elif "mate" in de:
            try:
                subprocess.run(["gsettings", "set", "org.mate.background", "picture-filename", abs_path], check=False)
                applied = True
            except Exception:
                pass

        # 6. LXQt / LXDE
        elif "lxqt" in de and shutil.which("pcmanfm-qt"):
            subprocess.run(["pcmanfm-qt", "-w", abs_path], check=False)
            applied = True
        elif "lxde" in de and shutil.which("pcmanfm"):
            subprocess.run(["pcmanfm", "-w", abs_path], check=False)
            applied = True

        # 7. Wayland / Hyprland / Sway
        is_wayland = bool(os.environ.get("WAYLAND_DISPLAY"))
        if is_wayland:
            if shutil.which("swww"):
                subprocess.run(["swww", "img", abs_path, "--transition-type", "fade"], check=False)
                applied = True
            elif shutil.which("hyprctl"):
                subprocess.run(["hyprctl", "hyprpaper", "preload", abs_path], check=False)
                subprocess.run(["hyprctl", "hyprpaper", "wallpaper", f",{abs_path}"], check=False)
                applied = True
            elif shutil.which("swaybg"):
                subprocess.run(["pkill", "swaybg"], check=False)
                subprocess.Popen(["swaybg", "-i", abs_path, "-m", "fill"])
                applied = True

        # 8. X11 Window Managers ve Genel Yedek Araçlar (feh / nitrogen / xwallpaper)
        if not applied:
            if shutil.which("feh"):
                res = subprocess.run(["feh", "--bg-fill", abs_path], check=False)
                applied = (res.returncode == 0)
            elif shutil.which("nitrogen"):
                res = subprocess.run(["nitrogen", "--set-zoom-fill", abs_path, "--save"], check=False)
                applied = (res.returncode == 0)
            elif shutil.which("xwallpaper"):
                res = subprocess.run(["xwallpaper", "--zoom", abs_path], check=False)
                applied = (res.returncode == 0)

        # Başarılı uygulandıysa yapılandırmaya kaydet
        if applied:
            cfg = load_config()
            cfg["last_wallpaper"] = abs_path
            save_config(cfg)

        return applied
