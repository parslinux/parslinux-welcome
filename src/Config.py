#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path

APP_ID = "org.parslinux.welcome"
APP_NAME = "Pars Hoş Geldiniz"
VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

USER_CONFIG_DIR = Path.home() / ".config" / "parslinux"
CONFIG_FILE = USER_CONFIG_DIR / "welcome.json"

DEFAULT_CONFIG = {
    "show_on_startup": True,
    "theme_mode": "system",  # "system", "light", "dark"
    "version": VERSION
}

def get_data_path(relative_path: str) -> str:
    """Sistemde veya yerel geliştirme ortamındaki data dosyası yolunu döner."""
    local_path = DATA_DIR / relative_path
    if local_path.exists():
        return str(local_path)
    
    # Sistem geneli kurulu yol
    sys_path = Path("/usr/share/parslinux-welcome") / relative_path
    if sys_path.exists():
        return str(sys_path)
        
    return str(local_path)

def load_config() -> dict:
    """Kullanıcı yapılandırmasını yükler."""
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {**DEFAULT_CONFIG, **data}
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config: dict) -> bool:
    """Kullanıcı yapılandırmasını kaydeder."""
    try:
        USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Ayar kaydetme hatası: {e}")
        return False
