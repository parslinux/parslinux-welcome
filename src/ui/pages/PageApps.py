#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from gi.repository import Gtk, Adw, GLib
from src.Config import get_data_path
from src.core.AppInstaller import AppInstaller
from src.core.DesktopActions import DesktopActions

class PageApps(Gtk.Box):
    """Popüler ve önerilen uygulamaların listelendiği ve kurulduğu sayfa."""

    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.main_window = main_window

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.append(scroll)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(800)
        clamp.set_tightening_threshold(600)
        scroll.set_child(clamp)

        self.box_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.box_content.set_margin_top(16)
        self.box_content.set_margin_bottom(24)
        self.box_content.set_margin_start(16)
        self.box_content.set_margin_end(16)
        clamp.set_child(self.box_content)

        self._load_and_render_apps()

    def _load_and_render_apps(self):
        """apps.json dosyasından kategorileri ve uygulamaları yükleyip çizer."""
        apps_file = get_data_path("apps.json")
        try:
            with open(apps_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Uygulama listesi yüklenemedi: {e}")
            data = {"categories": []}

        for cat in data.get("categories", []):
            group = Adw.PreferencesGroup()
            group.set_title(cat.get("name", "Uygulamalar"))
            
            for app in cat.get("apps", []):
                row = self._create_app_row(app)
                group.add(row)

            self.box_content.append(group)

    def _create_app_row(self, app: dict) -> Adw.ActionRow:
        """Tek bir uygulama için Adw.ActionRow oluşturur."""
        row = Adw.ActionRow()
        title_text = GLib.markup_escape_text(app.get("name", "Uygulama"))
        desc_text = GLib.markup_escape_text(app.get("desc", ""))
        row.set_title(title_text)
        row.set_subtitle(desc_text)

        icon_name = app.get("icon", "application-x-executable")
        row.set_icon_name(icon_name)

        cmd = app.get("cmd", "")
        flatpak_id = app.get("flatpak", "")
        is_installed = AppInstaller.is_installed(cmd, flatpak_id)

        btn = Gtk.Button()
        btn.set_valign(Gtk.Align.CENTER)

        if is_installed:
            btn.set_label("Başlat")
            btn.connect("clicked", lambda b, c=cmd: DesktopActions.run_app_or_command(c))
        else:
            btn.set_label("Kur")
            btn.add_css_class("suggested-action")
            btn.connect("clicked", lambda b, a=app: self._on_install_clicked(b, a))

        row.add_suffix(btn)
        return row

    def _on_install_clicked(self, button: Gtk.Button, app: dict):
        """Kurulum butonuna tıklandığında kurulumu tetikler."""
        button.set_sensitive(False)
        button.set_label("Kuruluyor...")
        success = AppInstaller.install_app(app)
        if not success:
            button.set_label("Kurulamadı")
            button.set_sensitive(True)
