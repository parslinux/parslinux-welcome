#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Adw, GLib
from src.core.SystemInfo import SystemInfo
from src.core.DesktopActions import DesktopActions
from src.ui.widgets.InfoCard import StatCard
from src.Config import get_data_path
import os

class PageWelcome(Gtk.Box):
    """Modern Karşılama ve Sistem Kontrol Merkezi sayfası."""

    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.main_window = main_window

        # Kaydırılabilir kapsayıcı
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

        # 1. Hero Karşılama Bölümü
        self._build_hero_section(box_content)

        # 2. Donanım & Sistem Dashboard Grid'i
        self._build_dashboard_grid(box_content)

        # 3. Hızlı Başlangıç Eylemleri
        self._build_quick_actions(box_content)

    def _build_hero_section(self, container):
        """Üst kısımda göz alıcı Pars Linux Hero banner'ı oluşturur."""
        hero = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        hero.add_css_class("welcome-hero")

        # Sol Pars Logo
        png_path = get_data_path("org.parslinux.welcome.png")
        svg_path = get_data_path("org.parslinux.welcome.svg")
        logo_path = png_path if os.path.exists(png_path) else svg_path

        if os.path.exists(logo_path):
            img_logo = Gtk.Image.new_from_file(logo_path)
            img_logo.set_pixel_size(84)
            img_logo.add_css_class("welcome-logo")
            img_logo.set_valign(Gtk.Align.CENTER)
            hero.append(img_logo)
        else:
            img_logo = Gtk.Image.new_from_icon_name("distributor-logo")
            img_logo.set_pixel_size(76)
            hero.append(img_logo)

        # Sağ Metin ve Aksiyon Bölümü
        vbox_text = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox_text.set_hexpand(True)
        vbox_text.set_valign(Gtk.Align.CENTER)

        lbl_title = Gtk.Label(label="Pars Linux'a Hoş Geldiniz")
        lbl_title.add_css_class("welcome-title")
        lbl_title.set_halign(Gtk.Align.START)
        vbox_text.append(lbl_title)

        info = SystemInfo.get_all_summary()
        lbl_sub = Gtk.Label(
            label=f"{info['os_name']} ile modern, hızlı ve güvenli bir masaüstü deneyimi."
        )
        lbl_sub.add_css_class("welcome-subtitle")
        lbl_sub.set_halign(Gtk.Align.START)
        lbl_sub.set_wrap(True)
        vbox_text.append(lbl_sub)

        # Etiket rozetleri (DE ve Kernel)
        badges_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        badges_box.set_margin_top(4)

        b_de = Gtk.Label(label=f"Masaüstü: {info['desktop']}")
        b_de.add_css_class("pill-badge")
        b_de.add_css_class("available")

        b_kernel = Gtk.Label(label=info['kernel'])
        b_kernel.add_css_class("pill-badge")
        b_kernel.add_css_class("installed")

        badges_box.append(b_de)
        badges_box.append(b_kernel)
        vbox_text.append(badges_box)

        hero.append(vbox_text)
        container.append(hero)

    def _build_dashboard_grid(self, container):
        """2 sütunlu modern donanım ve kaynak kullanım kartları."""
        group_dash = Adw.PreferencesGroup()
        group_dash.set_title("Sistem ve Donanım Durumu")
        group_dash.set_description("Bilgisayarınızın temel donanım ve kaynak kullanımı")

        grid = Gtk.Grid()
        grid.set_column_spacing(12)
        grid.set_row_spacing(12)
        grid.set_column_homogeneous(True)
        grid.set_margin_top(8)

        info = SystemInfo.get_all_summary()

        # Kart 1: İşlemci (CPU)
        card_cpu = StatCard(
            title="İşlemci",
            value=info["cpu"],
            icon_name="hardware-chip-symbolic",
            subtitle=f"Mimari: {info['arch']}"
        )
        grid.attach(card_cpu, 0, 0, 1, 1)

        # Kart 2: Grafik Kartı (GPU)
        card_gpu = StatCard(
            title="Grafik Kartı",
            value=info["gpu"],
            icon_name="video-display-symbolic",
            subtitle="Donanım Hızlandırma Aktif"
        )
        grid.attach(card_gpu, 1, 0, 1, 1)

        # Kart 3: Bellek (RAM) - Canlı Doluluk Çubuğu ile
        ram_pct = int(info["ram_fraction"] * 100)
        card_ram = StatCard(
            title="Bellek (RAM)",
            value=info["ram_text"],
            icon_name="drive-harddisk-symbolic",
            subtitle=f"%{ram_pct} Kullanımda",
            fraction=info["ram_fraction"]
        )
        grid.attach(card_ram, 0, 1, 1, 1)

        # Kart 4: Depolama (Disk) - Canlı Doluluk Çubuğu ile
        disk_pct = int(info["disk_fraction"] * 100)
        card_disk = StatCard(
            title="Depolama (/ Kök)",
            value=info["disk_text"],
            icon_name="drive-harddisk-symbolic",
            subtitle=f"%{disk_pct} Dolu",
            fraction=info["disk_fraction"]
        )
        grid.attach(card_disk, 1, 1, 1, 1)

        # Group içine grid yerleştirme
        box_wrap = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_wrap.append(grid)
        group_dash.add(box_wrap)

        container.append(group_dash)

    def _build_quick_actions(self, container):
        """Hızlı eylemler tercih grubu."""
        group_quick = Adw.PreferencesGroup()
        group_quick.set_title("Hızlı Başlangıç")
        group_quick.set_description("Sisteminizi özelleştirmeye başlayın")

        # 1. Pars Update Satırı
        row_update = Adw.ActionRow()
        row_update.set_title("Sistemi Güncelle (Pars Update)")
        row_update.set_subtitle("Güvenlik ve paket güncellemelerini anında denetleyin")
        row_update.set_icon_name("software-update-available-symbolic")

        btn_update = Gtk.Button(label="Güncelle")
        btn_update.add_css_class("suggested-action")
        btn_update.set_valign(Gtk.Align.CENTER)
        btn_update.connect("clicked", lambda b: DesktopActions.launch_pars_update())
        row_update.add_suffix(btn_update)
        row_update.set_activatable_widget(btn_update)
        group_quick.add(row_update)

        # 2. İlk Adımlar Sekmesine Geçiş
        row_steps = Adw.ActionRow()
        row_steps.set_title("Görünüm ve İlk Adımlar")
        row_steps.set_subtitle("Karanlık/Aydınlık tema, ekran ayarları ve sistem yedekleme")
        row_steps.set_icon_name("preferences-desktop-theme-symbolic")

        btn_steps = Gtk.Button(label="Yapılandır")
        btn_steps.set_valign(Gtk.Align.CENTER)
        btn_steps.connect("clicked", lambda b: self.main_window.switch_page("first_steps"))
        row_steps.add_suffix(btn_steps)
        row_steps.set_activatable_widget(btn_steps)
        group_quick.add(row_steps)

        # 3. Popüler Uygulamalar Sekmesine Geçiş
        row_apps = Adw.ActionRow()
        row_apps.set_title("Önerilen Uygulamaları Keşfet")
        row_apps.set_subtitle("Tarayıcılar, ofis, kodlama ve eğlence paketlerini tek tıkla kurun")
        row_apps.set_icon_name("software-store-symbolic")

        btn_apps = Gtk.Button(label="Uygulamalar")
        btn_apps.set_valign(Gtk.Align.CENTER)
        btn_apps.connect("clicked", lambda b: self.main_window.switch_page("apps"))
        row_apps.add_suffix(btn_apps)
        row_apps.set_activatable_widget(btn_apps)
        group_quick.add(row_apps)

        container.append(group_quick)
