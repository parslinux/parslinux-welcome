#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
from gi.repository import Gio, GLib, Adw

class DesktopActions:
    """Masaüstü eylemleri, ayarlar, uygulama ve bağlantı tetikleyicisi."""

    @staticmethod
    def open_url(url: str) -> bool:
        """Verilen web adresini varsayılan tarayıcıda açar."""
        try:
            return Gio.AppInfo.launch_default_for_uri(url, None)
        except Exception:
            try:
                subprocess.Popen(["xdg-open", url])
                return True
            except Exception as e:
                print(f"URL açma hatası: {e}")
                return False

    @staticmethod
    def run_app_or_command(command: str) -> bool:
        """Verilen komut veya uygulamayı arka planda başlatır."""
        try:
            parts = command.split()
            cmd_name = parts[0]
            if shutil.which(cmd_name):
                subprocess.Popen(parts)
                return True
            return False
        except Exception as e:
            print(f"Uygulama başlatma hatası ({command}): {e}")
            return False

    @classmethod
    def launch_pars_update(cls) -> bool:
        """Pars Update uygulamasını başlatır."""
        candidates = ["pars-update", "/usr/bin/pars-update", "parslinux-update"]
        for cmd in candidates:
            if shutil.which(cmd):
                return cls.run_app_or_command(cmd)
        
        # Eğer yerel klasörde varsa
        local_pars_update = os.path.expanduser("~/pars-update/pars-update")
        if os.path.exists(local_pars_update):
            return cls.run_app_or_command(local_pars_update)
            
        return False

    @classmethod
    def open_system_settings(cls) -> bool:
        """Masaüstü ortamına uygun ayarlar merkezini açar."""
        settings_apps = [
            "gnome-control-center",
            "xfce4-settings-manager",
            "systemsettings",
            "cinnamon-settings",
            "mate-control-center"
        ]
        for app in settings_apps:
            if shutil.which(app):
                return cls.run_app_or_command(app)
        return False

    @classmethod
    def open_backup_tool(cls) -> bool:
        """Sistem yedekleme aracını (Timeshift, Déjà Dup, vb.) açar."""
        backup_apps = ["timeshift-gtk", "timeshift", "deja-dup", "snapper-gui"]
        for app in backup_apps:
            if shutil.which(app):
                return cls.run_app_or_command(app)
        return False

    @classmethod
    def open_display_settings(cls) -> bool:
        """Ekran ve çözünürlük ayarlarını açar."""
        display_apps = [
            "gnome-control-center display",
            "xfce4-display-settings",
            "kcmshell5 kcm_kscreen",
            "cinnamon-settings display"
        ]
        for app in display_apps:
            cmd = app.split()[0]
            if shutil.which(cmd):
                return cls.run_app_or_command(app)
        return False

    @classmethod
    def set_color_scheme(cls, mode: str):
        """Libadwaita ve masaüstü açık/koyu renk şemasını ayarlar ('default', 'force-light', 'force-dark')."""
        style_manager = Adw.StyleManager.get_default()
        if mode == "dark":
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
            cls._apply_system_theme(dark=True)
        elif mode == "light":
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
            cls._apply_system_theme(dark=False)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)

    @staticmethod
    def _apply_system_theme(dark: bool):
        """GNOME veya diğer masaüstlerinde sistem genelinde koyu/açık temayı gsettings ile günceller."""
        try:
            scheme_val = "prefer-dark" if dark else "default"
            subprocess.run([
                "gsettings", "set", "org.gnome.desktop.interface", "color-scheme", scheme_val
            ], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
