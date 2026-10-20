#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from src.Config import get_data_path, load_config, save_config

class AutostartManager:
    """Kullanıcının giriş yaptığında uygulamanın otomatik açılmasını yönetir."""

    AUTOSTART_DIR = Path.home() / ".config" / "autostart"
    DESKTOP_FILENAME = "org.parslinux.welcome.desktop"
    AUTOSTART_FILE = AUTOSTART_DIR / DESKTOP_FILENAME

    @classmethod
    def is_enabled(cls) -> bool:
        """Açılışta otomatik başlatmanın etkin olup olmadığını kontrol eder."""
        config = load_config()
        if not config.get("show_on_startup", True):
            return False

        if not cls.AUTOSTART_FILE.exists():
            return False

        try:
            with open(cls.AUTOSTART_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if "Hidden=true" in content or "X-GNOME-Autostart-enabled=false" in content:
                    return False
            return True
        except Exception:
            return False

    @classmethod
    def set_enabled(cls, enable: bool) -> bool:
        """Otomatik başlatmayı açar veya kapatır."""
        # 1. Config dosyasını güncelle
        config = load_config()
        config["show_on_startup"] = enable
        save_config(config)

        # 2. XDG Autostart dosyasını güncelle
        try:
            if enable:
                cls.AUTOSTART_DIR.mkdir(parents=True, exist_ok=True)
                source_desktop = get_data_path(cls.DESKTOP_FILENAME)
                
                content = ""
                if os.path.exists(source_desktop):
                    with open(source_desktop, "r", encoding="utf-8") as f:
                        content = f.read()
                else:
                    content = (
                        "[Desktop Entry]\n"
                        "Name=Pars Hoş Geldiniz\n"
                        "Comment=Pars Linux Hoş Geldiniz Merkezi\n"
                        "Exec=pars-welcome\n"
                        "Icon=org.parslinux.welcome\n"
                        "Terminal=false\n"
                        "Type=Application\n"
                        "Categories=Settings;\n"
                        "X-GNOME-Autostart-enabled=true\n"
                    )

                with open(cls.AUTOSTART_FILE, "w", encoding="utf-8") as f:
                    f.write(content)
            else:
                if cls.AUTOSTART_FILE.exists():
                    cls.AUTOSTART_FILE.unlink()
            return True
        except Exception as e:
            print(f"Autostart güncelleme hatası: {e}")
            return False
