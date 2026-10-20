#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Adw
from src.core.SystemInfo import SystemInfo
from src.core.DesktopActions import DesktopActions

class PageWelcome(Gtk.Box):
    """Karşılama sayfası: Hoş geldiniz mesajı, sistem bilgileri ve hızlı eylemler."""

    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.main_window = main_window

        # Kaydırılabilir alan
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.append(scroll)

        # İçerik kapsayıcısı (Clamp ile geniş ekranlarda derli toplu durur)
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

        # 1. Modern Karşılama Banner'ı
        banner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        banner_box.add_css_class("welcome-banner")
        
        lbl_title = Gtk.Label(label="Pars Linux'a Hoş Geldiniz")
        lbl_title.add_css_class("welcome-title")
        lbl_title.set_halign(Gtk.Align.START)
        banner_box.append(lbl_title)

        lbl_subtitle = Gtk.Label(
            label="Hafif, güvenli, kararlı ve modern Linux deneyiminiz için her şey hazır."
        )
        lbl_subtitle.add_css_class("welcome-subtitle")
        lbl_subtitle.set_halign(Gtk.Align.START)
        banner_box.append(lbl_subtitle)

        box_content.append(banner_box)

        # 2. Hızlı Başlangıç Aksiyonları
        group_quick = Adw.PreferencesGroup()
        group_quick.set_title("Hızlı Başlangıç")
        group_quick.set_description("Sisteminizi kullanmaya başlamak için ilk adımlar")

        # Güncelleme Satırı
        row_update = Adw.ActionRow()
        row_update.set_title("Sistemi Güncelle")
        row_update.set_subtitle("Pars Update ile sistem paketlerini en son sürüme yükseltin")
        row_update.set_icon_name("software-update-available-symbolic")

        btn_update = Gtk.Button(label="Güncelle")
        btn_update.add_css_class("suggested-action")
        btn_update.set_valign(Gtk.Align.CENTER)
        btn_update.connect("clicked", lambda b: DesktopActions.launch_pars_update())
        row_update.add_suffix(btn_update)
        row_update.set_activatable_widget(btn_update)
        group_quick.add(row_update)

        # İlk Adımlar Sekmesine Geçiş Satırı
        row_steps = Adw.ActionRow()
        row_steps.set_title("İlk Adımları İncele")
        row_steps.set_subtitle("Tema, donanım sürücüleri ve sistem yedeklemesini yapılandırın")
        row_steps.set_icon_name("preferences-system-symbolic")

        btn_steps = Gtk.Button(label="İncele")
        btn_steps.set_valign(Gtk.Align.CENTER)
        btn_steps.connect("clicked", lambda b: self.main_window.switch_page("first_steps"))
        row_steps.add_suffix(btn_steps)
        row_steps.set_activatable_widget(btn_steps)
        group_quick.add(row_steps)

        box_content.append(group_quick)

        # 3. Sistem Bilgisi Grubu
        self._build_system_info_group(box_content)

    def _build_system_info_group(self, container):
        """Sistem özetini Adw.PreferencesGroup içine yerleştirir."""
        group_sys = Adw.PreferencesGroup()
        group_sys.set_title("Sistem Bilgileri")
        group_sys.set_description("Mevcut donanım ve yazılım yapılandırmanız")

        info = SystemInfo.get_all_summary()

        # Dağıtım & Sürüm
        row_os = Adw.ActionRow()
        row_os.set_title("İşletim Sistemi")
        row_os.set_subtitle(f"{info['os_name']} ({info['arch']})")
        row_os.set_icon_name("computer-symbolic")
        group_sys.add(row_os)

        # Çekirdek (Kernel)
        row_kernel = Adw.ActionRow()
        row_kernel.set_title("Linux Çekirdeği")
        row_kernel.set_subtitle(info["kernel"])
        row_kernel.set_icon_name("application-x-executable-symbolic")
        group_sys.add(row_kernel)

        # Masaüstü Ortamı
        row_desktop = Adw.ActionRow()
        row_desktop.set_title("Masaüstü Ortamı")
        row_desktop.set_subtitle(info["desktop"])
        row_desktop.set_icon_name("preferences-desktop-display-symbolic")
        group_sys.add(row_desktop)

        # İşlemci
        row_cpu = Adw.ActionRow()
        row_cpu.set_title("İşlemci")
        row_cpu.set_subtitle(info["cpu"])
        row_cpu.set_icon_name("hardware-chip-symbolic")
        group_sys.add(row_cpu)

        # Bellek & Disk
        row_memory = Adw.ActionRow()
        row_memory.set_title("Bellek ve Disk")
        row_memory.set_subtitle(f"{info['ram']}  •  {info['disk']}")
        row_memory.set_icon_name("drive-harddisk-symbolic")
        group_sys.add(row_memory)

        container.append(group_sys)
