#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# src modüllerinin doğru bulunabilmesi için kök dizini ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk

from src.Config import APP_ID, APP_NAME, get_data_path, load_config
from src.core.DesktopActions import DesktopActions
from src.core.I18n import init_i18n
from src.ui.MainWindowAdw import MainWindowAdw

class ParsWelcomeApp(Adw.Application):
    """Pars Welcome Libadwaita Uygulama Sınıfı."""

    def __init__(self):
        super().__init__(
            application_id=APP_ID,
            flags=0
        )

    def do_startup(self):
        """Uygulama ilk ayağa kalkarken dil, CSS ve stil ayarlarını yükler."""
        Adw.Application.do_startup(self)
        init_i18n()
        self._load_styles()
        self._load_initial_theme()

    def do_activate(self):
        """Pencereyi ekrana getirir."""
        win = self.props.active_window
        if not win:
            win = MainWindowAdw(self)
        win.present()

    def _load_styles(self):
        """data/style.css dosyasını global GTK Display'e bağlar."""
        css_file = get_data_path("style.css")
        if os.path.exists(css_file):
            provider = Gtk.CssProvider()
            try:
                provider.load_from_path(css_file)
                display = Gdk.Display.get_default()
                if display:
                    Gtk.StyleContext.add_provider_for_display(
                        display,
                        provider,
                        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                    )
            except Exception as e:
                print(f"CSS yükleme hatası: {e}")

    def _load_initial_theme(self):
        """Kullanıcının kayıtlı tema tercihini uygular."""
        cfg = load_config()
        theme_mode = cfg.get("theme_mode", "system")
        DesktopActions.set_color_scheme(theme_mode)

def main():
    app = ParsWelcomeApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main())
