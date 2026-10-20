#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from gi.repository import Gtk, Adw, GLib
from src.Config import get_data_path
from src.core.DesktopActions import DesktopActions

class PageCommunity(Gtk.Box):
    """Topluluk, wiki ve destek bağlantıları sayfası."""

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

        box_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box_content.set_margin_top(16)
        box_content.set_margin_bottom(24)
        box_content.set_margin_start(16)
        box_content.set_margin_end(16)
        clamp.set_child(box_content)

        # Topluluk Grubu
        group = Adw.PreferencesGroup()
        group.set_title("Pars Linux Topluluğu ve Destek")
        group.set_description("Sorularınız, katkılarınız ve önerileriniz için topluluğumuza katılın")

        links_file = get_data_path("links.json")
        try:
            with open(links_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Bağlantı listesi okunamadı: {e}")
            data = {"links": []}

        for item in data.get("links", []):
            row = Adw.ActionRow()
            title_text = GLib.markup_escape_text(item.get("title", ""))
            sub_text = GLib.markup_escape_text(item.get("subtitle", ""))
            row.set_title(title_text)
            row.set_subtitle(sub_text)
            row.set_icon_name(item.get("icon", "globe-symbolic"))

            url = item.get("url", "")

            btn_open = Gtk.Button()
            btn_open.set_icon_name("external-link-symbolic")
            btn_open.set_valign(Gtk.Align.CENTER)
            btn_open.add_css_class("flat")
            btn_open.connect("clicked", lambda b, u=url: DesktopActions.open_url(u))

            row.add_suffix(btn_open)
            row.set_activatable_widget(btn_open)
            group.add(row)

        box_content.append(group)
