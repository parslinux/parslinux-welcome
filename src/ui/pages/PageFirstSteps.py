#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Adw, GLib
from src.core.DesktopActions import DesktopActions
from src.Config import load_config, save_config

class PageFirstSteps(Gtk.Box):
    """İlk Adımlar sayfası: Görsel tema seçimi, ekran ayarları ve sistem yönetimi."""

    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.main_window = main_window

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.append(scroll)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(840)
        clamp.set_tightening_threshold(620)
        scroll.set_child(clamp)

        box_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        box_content.set_margin_top(16)
        box_content.set_margin_bottom(28)
        box_content.set_margin_start(16)
        box_content.set_margin_end(16)
        clamp.set_child(box_content)

        # 1. Görünüm & Tema Kartları
        self._build_theme_cards_section(box_content)

        # 2. Ekran ve Kişiselleştirme
        self._build_customization_section(box_content)

        # 3. Sistem Yönetim ve Bakım Araçları
        self._build_management_section(box_content)

    def _build_theme_cards_section(self, container):
        """Kullanıcının tek tıkla Açık, Koyu veya Sistem temasını seçebileceği görsel kartlar."""
        group_theme = Adw.PreferencesGroup()
        group_theme.set_title("Görünüm ve Renk Teması")
        group_theme.set_description("Masaüstü ve uygulama arayüzü renk stilinizi belirleyin")

        # 3 sütunlu kart kutusu
        box_cards = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
        box_cards.set_homogeneous(True)
        box_cards.set_margin_top(6)

        current_theme = load_config().get("theme_mode", "system")
        self.theme_widgets = {}

        # 1. Açık Tema Kartı
        card_light = self._create_theme_card("Açık Tema", "light-mode-symbolic", "light", current_theme == "light")
        # 2. Koyu Tema Kartı
        card_dark = self._create_theme_card("Koyu Tema", "weather-clear-night-symbolic", "dark", current_theme == "dark")
        # 3. Sistem Varsayılanı Kartı
        card_system = self._create_theme_card("Sistem", "emblem-system-symbolic", "system", current_theme == "system")

        box_cards.append(card_light)
        box_cards.append(card_dark)
        box_cards.append(card_system)

        box_wrap = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_wrap.append(box_cards)
        group_theme.add(box_wrap)

        container.append(group_theme)

    def _create_theme_card(self, title: str, icon_name: str, mode: str, is_active: bool) -> Gtk.Button:
        """Tıklanabilir modern tema önizleme kartı."""
        btn = Gtk.Button()
        btn.add_css_class("theme-card")
        if is_active:
            btn.add_css_class("active")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)

        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(32)
        box.append(icon)

        lbl = Gtk.Label(label=title)
        lbl.set_css_classes(["heading"])
        box.append(lbl)

        btn.set_child(box)
        btn.connect("clicked", lambda b, m=mode: self._on_theme_card_clicked(m))
        self.theme_widgets[mode] = btn
        return btn

    def _on_theme_card_clicked(self, mode: str):
        """Seçilen temayı uygular ve arayüzü günceller."""
        DesktopActions.set_color_scheme(mode)
        cfg = load_config()
        cfg["theme_mode"] = mode
        save_config(cfg)

        for m, widget in self.theme_widgets.items():
            if m == mode:
                widget.add_css_class("active")
            else:
                widget.remove_css_class("active")

    def _build_customization_section(self, container):
        """Ekran, çözünürlük ve görünüm ayarları."""
        group_cust = Adw.PreferencesGroup()
        group_cust.set_title("Kişiselleştirme")
        group_cust.set_description("Monitör ve ekran görüntüleme seçenekleri")

        # Ekran Çözünürlüğü ve Ölçekleme
        row_display = Adw.ActionRow()
        row_display.set_title("Ekran Çözünürlüğü ve Ölçekleme")
        row_display.set_subtitle("Monitör yenileme hızı, çözünürlük ve HiDPI (100% / 200%) ölçekleme")
        row_display.set_icon_name("preferences-desktop-display-symbolic")

        btn_display = Gtk.Button(label="Yapılandır")
        btn_display.set_valign(Gtk.Align.CENTER)
        btn_display.connect("clicked", lambda b: DesktopActions.open_display_settings())
        row_display.add_suffix(btn_display)
        row_display.set_activatable_widget(btn_display)
        group_cust.add(row_display)

        container.append(group_cust)

    def _build_management_section(self, container):
        """Sistem bakım, güncelleme ve yedekleme araçları."""
        group_tools = Adw.PreferencesGroup()
        group_tools.set_title("Sistem Yönetimi ve Güvenlik")
        group_tools.set_description("Güncellemeler, yedekleme ve denetim masası")

        # Pars Update
        row_update = Adw.ActionRow()
        row_update.set_title("Pars Update (Paket Güncelleyici)")
        row_update.set_subtitle("Dağıtım paketlerini, çekirdeği ve güvenlik yamalarını güncelleyin")
        row_update.set_icon_name("software-update-available-symbolic")

        btn_update = Gtk.Button(label="Güncelle")
        btn_update.add_css_class("suggested-action")
        btn_update.set_valign(Gtk.Align.CENTER)
        btn_update.connect("clicked", lambda b: DesktopActions.launch_pars_update())
        row_update.add_suffix(btn_update)
        row_update.set_activatable_widget(btn_update)
        group_tools.add(row_update)

        # Sistem Yedekleme
        row_backup = Adw.ActionRow()
        row_backup.set_title("Sistem Anlık Görüntüsü (Snapshot)")
        row_backup.set_subtitle("Olası bir sistem arızasında sistemi geri yüklemek için yedek oluşturun")
        row_backup.set_icon_name("drive-multidisk-symbolic")

        btn_backup = Gtk.Button(label="Yedekle")
        btn_backup.set_valign(Gtk.Align.CENTER)
        btn_backup.connect("clicked", lambda b: DesktopActions.open_backup_tool())
        row_backup.add_suffix(btn_backup)
        row_backup.set_activatable_widget(btn_backup)
        group_tools.add(row_backup)

        # Sistem Ayarları
        row_settings = Adw.ActionRow()
        row_settings.set_title("Sistem Kontrol Merkezi")
        row_settings.set_subtitle("Ağ, Bluetooth, ses, kullanıcılar ve tüm donanım seçenekleri")
        row_settings.set_icon_name("preferences-system-symbolic")

        btn_settings = Gtk.Button(label="Ayarlar")
        btn_settings.set_valign(Gtk.Align.CENTER)
        btn_settings.connect("clicked", lambda b: DesktopActions.open_system_settings())
        row_settings.add_suffix(btn_settings)
        row_settings.set_activatable_widget(btn_settings)
        group_tools.add(row_settings)

        container.append(group_tools)
