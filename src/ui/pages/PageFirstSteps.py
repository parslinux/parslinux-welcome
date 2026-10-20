#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Adw
from src.core.DesktopActions import DesktopActions
from src.Config import load_config, save_config

class PageFirstSteps(Gtk.Box):
    """İlk Adımlar sayfası: Görünüm ayarları, sistem araçları ve donanım."""

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

        # 1. Görünüm & Tema
        self._build_appearance_group(box_content)

        # 2. Sistem ve Yönetim Araçları
        self._build_system_tools_group(box_content)

    def _build_appearance_group(self, container):
        """Görünüm, açık/koyu tema ayarlarını oluşturur."""
        group_theme = Adw.PreferencesGroup()
        group_theme.set_title("Görünüm ve Tema")
        group_theme.set_description("Masaüstü ve uygulama renk stilinizi belirleyin")

        row_theme = Adw.ActionRow()
        row_theme.set_title("Renk Teması")
        row_theme.set_subtitle("Açık, Koyu veya sistem varsayılan modunu seçin")
        row_theme.set_icon_name("preferences-desktop-theme-symbolic")

        box_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box_buttons.set_valign(Gtk.Align.CENTER)

        btn_light = Gtk.Button(label="Açık")
        btn_light.connect("clicked", lambda b: self._set_theme("light"))

        btn_dark = Gtk.Button(label="Koyu")
        btn_dark.connect("clicked", lambda b: self._set_theme("dark"))

        btn_system = Gtk.Button(label="Sistem")
        btn_system.connect("clicked", lambda b: self._set_theme("system"))

        box_buttons.append(btn_light)
        box_buttons.append(btn_dark)
        box_buttons.append(btn_system)

        row_theme.add_suffix(box_buttons)
        group_theme.add(row_theme)

        # Ekran Çözünürlüğü ve Ölçekleme
        row_display = Adw.ActionRow()
        row_display.set_title("Ekran ve Ölçekleme")
        row_display.set_subtitle("Monitör çözünürlüğü ve HiDPI ölçekleme ayarları")
        row_display.set_icon_name("preferences-desktop-display-symbolic")

        btn_display = Gtk.Button(label="Yapılandır")
        btn_display.set_valign(Gtk.Align.CENTER)
        btn_display.connect("clicked", lambda b: DesktopActions.open_display_settings())
        row_display.add_suffix(btn_display)
        row_display.set_activatable_widget(btn_display)
        group_theme.add(row_display)

        container.append(group_theme)

    def _build_system_tools_group(self, container):
        """Sistem bakım, yedekleme ve güncelleme araçları."""
        group_tools = Adw.PreferencesGroup()
        group_tools.set_title("Sistem Yönetimi")
        group_tools.set_description("Temel bakım, güncelleme ve güvenlik araçları")

        # Pars Update
        row_update = Adw.ActionRow()
        row_update.set_title("Pars Update (Güncelleme Yöneticisi)")
        row_update.set_subtitle("Sistem paketlerini ve güvenlik yamalarını denetleyin")
        row_update.set_icon_name("software-update-available-symbolic")

        btn_update = Gtk.Button(label="Aç")
        btn_update.add_css_class("suggested-action")
        btn_update.set_valign(Gtk.Align.CENTER)
        btn_update.connect("clicked", lambda b: DesktopActions.launch_pars_update())
        row_update.add_suffix(btn_update)
        row_update.set_activatable_widget(btn_update)
        group_tools.add(row_update)

        # Sistem Yedekleme
        row_backup = Adw.ActionRow()
        row_backup.set_title("Sistem Yedekleme")
        row_backup.set_subtitle("Olası sorunlara karşı sistem anlık görüntüsü (snapshot) oluşturun")
        row_backup.set_icon_name("drive-multidisk-symbolic")

        btn_backup = Gtk.Button(label="Başlat")
        btn_backup.set_valign(Gtk.Align.CENTER)
        btn_backup.connect("clicked", lambda b: DesktopActions.open_backup_tool())
        row_backup.add_suffix(btn_backup)
        row_backup.set_activatable_widget(btn_backup)
        group_tools.add(row_backup)

        # Genel Sistem Ayarları
        row_settings = Adw.ActionRow()
        row_settings.set_title("Kontrol Merkezi (Ayarlar)")
        row_settings.set_subtitle("Ağ, ses, kullanıcılar ve tüm sistem seçenekleri")
        row_settings.set_icon_name("preferences-system-symbolic")

        btn_settings = Gtk.Button(label="Ayarlar")
        btn_settings.set_valign(Gtk.Align.CENTER)
        btn_settings.connect("clicked", lambda b: DesktopActions.open_system_settings())
        row_settings.add_suffix(btn_settings)
        row_settings.set_activatable_widget(btn_settings)
        group_tools.add(row_settings)

        container.append(group_tools)

    def _set_theme(self, mode: str):
        """Temayı uygular ve yapılandırmaya yazar."""
        DesktopActions.set_color_scheme(mode)
        cfg = load_config()
        cfg["theme_mode"] = mode
        save_config(cfg)
