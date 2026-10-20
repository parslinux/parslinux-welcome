#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from gi.repository import Gtk, Adw, GLib
from src.Config import get_data_path
from src.core.AppInstaller import AppInstaller
from src.core.DesktopActions import DesktopActions

class PageApps(Gtk.Box):
    """Popüler ve önerilen uygulamaların listelendiği, arandığı ve kurulduğu modern sayfa."""

    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.main_window = main_window
        self.app_rows = []  # Arama filtrelemesi için (row, search_text)

        # Üst Arama Çubuğu
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        search_box.set_margin_start(18)
        search_box.set_margin_end(18)
        search_box.set_margin_top(14)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Uygulama adı veya açıklama ile ara...")
        self.search_entry.set_hexpand(True)
        self.search_entry.connect("search-changed", self._on_search_changed)
        search_box.append(self.search_entry)
        self.append(search_box)

        # Kaydırılabilir alan
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.append(scroll)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(840)
        clamp.set_tightening_threshold(620)
        scroll.set_child(clamp)

        self.box_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.box_content.set_margin_top(12)
        self.box_content.set_margin_bottom(28)
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
            cat_name = cat.get("name", "Uygulamalar")
            apps_list = cat.get("apps", [])
            group.set_title(f"{cat_name} ({len(apps_list)})")
            
            for app in apps_list:
                row = self._create_app_row(app)
                group.add(row)

                # Arama için indeksle
                search_key = f"{app.get('name', '')} {app.get('desc', '')} {cat_name}".lower()
                self.app_rows.append((row, search_key, group))

            self.box_content.append(group)

    def _create_app_row(self, app: dict) -> Adw.ActionRow:
        """Tek bir uygulama için modern Adw.ActionRow oluşturur."""
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

        # Sağ Taraf Buton ve Rozet Kutusu
        suffix_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        suffix_box.set_valign(Gtk.Align.CENTER)

        if is_installed:
            badge = Gtk.Label(label="Kurulu")
            badge.add_css_class("pill-badge")
            badge.add_css_class("installed")
            suffix_box.append(badge)

            btn = Gtk.Button(label="Başlat")
            btn.connect("clicked", lambda b, c=cmd: DesktopActions.run_app_or_command(c))
            suffix_box.append(btn)
            row.set_activatable_widget(btn)
        else:
            btn = Gtk.Button(label="Kur")
            btn.add_css_class("suggested-action")
            btn.connect("clicked", lambda b, a=app, sb=suffix_box: self._on_install_clicked(b, a, sb))
            suffix_box.append(btn)
            row.set_activatable_widget(btn)

        row.add_suffix(suffix_box)
        return row

    def _on_install_clicked(self, button: Gtk.Button, app: dict, suffix_box: Gtk.Box):
        """Kurulum butonuna tıklandığında spinner gösterip kurulumu tetikler."""
        button.set_visible(False)

        spinner = Gtk.Spinner()
        spinner.start()
        suffix_box.append(spinner)

        def run_proc():
            success = AppInstaller.install_app(app)
            GLib.idle_add(self._on_install_done, button, spinner, suffix_box, app, success)

        import threading
        threading.Thread(target=run_proc, daemon=True).start()

    def _on_install_done(self, button: Gtk.Button, spinner: Gtk.Spinner, suffix_box: Gtk.Box, app: dict, success: bool):
        """Kurulum bittiğinde UI'ı günceller."""
        spinner.stop()
        suffix_box.remove(spinner)

        cmd = app.get("cmd", "")
        flatpak_id = app.get("flatpak", "")
        if AppInstaller.is_installed(cmd, flatpak_id):
            button.set_label("Başlat")
            button.remove_css_class("suggested-action")
            button.set_visible(True)
            button.connect("clicked", lambda b, c=cmd: DesktopActions.run_app_or_command(c))

            badge = Gtk.Label(label="Kurulu")
            badge.add_css_class("pill-badge")
            badge.add_css_class("installed")
            suffix_box.prepend(badge)
        else:
            button.set_label("Tekrar Dene")
            button.set_visible(True)

    def _on_search_changed(self, entry: Gtk.SearchEntry):
        """Arama metnine göre satırları gösterir veya gizler."""
        query = entry.get_text().strip().lower()

        # Her grup içindeki görünen satır sayısını takip et
        group_visible_counts = {}

        for row, search_key, group in self.app_rows:
            matches = (query in search_key) if query else True
            row.set_visible(matches)
            
            if group not in group_visible_counts:
                group_visible_counts[group] = 0
            if matches:
                group_visible_counts[group] += 1

        # Hiç elemanı kalmayan grupları gizle
        for group, count in group_visible_counts.items():
            group.set_visible(count > 0)
