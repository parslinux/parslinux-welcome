#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
from typing import Dict, Optional

class AppInstaller:
    """Popüler uygulamaların durumunu kontrol eden ve kurulumunu başlatan sınıf."""

    @staticmethod
    def is_installed(cmd: str, flatpak_id: str = "") -> bool:
        """Uygulamanın kurulu olup olmadığını denetler."""
        if cmd and shutil.which(cmd):
            return True
            
        if flatpak_id and shutil.which("flatpak"):
            try:
                res = subprocess.run(
                    ["flatpak", "info", flatpak_id],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                if res.returncode == 0:
                    return True
            except Exception:
                pass
                
        return False

    @staticmethod
    def get_preferred_terminal() -> Optional[str]:
        """Sistemde mevcut olan terminal uygulamasını bulur."""
        terminals = [
            "gnome-terminal",
            "xfce4-terminal",
            "ptyxis",
            "konsole",
            "alacritty",
            "kitty",
            "tilix",
            "xterm"
        ]
        for term in terminals:
            if shutil.which(term):
                return term
        return None

    @classmethod
    def install_app(cls, app: Dict) -> bool:
        """Uygulama için uygun paket yöneticisi komutunu terminal penceresinde çalıştırır."""
        # Dağıtım paket yöneticisini tespit et
        is_arch = shutil.which("pacman") is not None
        is_debian = shutil.which("apt") is not None
        has_flatpak = shutil.which("flatpak") is not None

        install_cmd = ""
        app_name = app.get("name", "Uygulama")

        if is_arch and app.get("pkg_arch"):
            pkg = app["pkg_arch"]
            install_cmd = f"sudo pacman -S --needed {pkg}"
        elif is_debian and app.get("pkg_debian"):
            pkg = app["pkg_debian"]
            install_cmd = f"sudo apt update && sudo apt install -y {pkg}"
        elif has_flatpak and app.get("flatpak"):
            fp = app["flatpak"]
            install_cmd = f"flatpak install -y flathub {fp}"
        else:
            return False

        term = cls.get_preferred_terminal()
        if not term:
            # Terminal yoksa arka planda pkexec ile çalıştırmayı dene
            try:
                subprocess.Popen(["pkexec", "bash", "-c", install_cmd])
                return True
            except Exception:
                return False

        # Terminalde kullanıcıya göstererek çalıştır
        full_script = f"echo '==> {app_name} Kuruluyor...'; {install_cmd}; echo 'Bitti. Çıkmak için Enter tuşuna basın...'; read"
        
        try:
            if term == "gnome-terminal" or term == "ptyxis":
                subprocess.Popen([term, "--", "bash", "-c", full_script])
            elif term == "xfce4-terminal":
                subprocess.Popen([term, "-e", f"bash -c \"{full_script}\""])
            elif term == "konsole":
                subprocess.Popen([term, "-e", "bash", "-c", full_script])
            else:
                subprocess.Popen([term, "-e", f"bash -c '{full_script}'"])
            return True
        except Exception as e:
            print(f"Kurulum başlatılamadı: {e}")
            return False
