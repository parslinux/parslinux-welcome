#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import gettext
import locale
from src.Config import get_data_path, load_config, save_config

APP_DOMAIN = "parslinux-welcome"

_current_translation = None
_current_lang = "system"

def get_locale_dir() -> str:
    """Yerel veya sistem gettext locale dizinini döner."""
    local_dir = get_data_path("locale")
    if os.path.exists(local_dir):
        return local_dir
    if os.path.exists("/usr/share/locale"):
        return "/usr/share/locale"
    return local_dir

def set_language(lang_code: str = "system", save: bool = True):
    """
    Uygulama dilini ayarlar.
    lang_code: 'system', 'tr', 'en'
    """
    global _current_translation, _current_lang
    _current_lang = lang_code
    locale_dir = get_locale_dir()

    languages = None if (lang_code == "system" or not lang_code) else [lang_code]

    try:
        _current_translation = gettext.translation(
            APP_DOMAIN,
            localedir=locale_dir,
            languages=languages,
            fallback=True
        )
    except Exception:
        _current_translation = gettext.NullTranslations()

    if save:
        cfg = load_config()
        cfg["language"] = lang_code
        save_config(cfg)

def init_i18n():
    """Uygulama başlangıcında kayıtlı dil tercihini yükler."""
    cfg = load_config()
    lang = cfg.get("language", "system")
    set_language(lang, save=False)

def _(message: str) -> str:
    """Evrensel çeviri sarmalayıcısı."""
    global _current_translation
    if _current_translation is None:
        init_i18n()
    return _current_translation.gettext(message)

def get_current_language() -> str:
    return _current_lang
