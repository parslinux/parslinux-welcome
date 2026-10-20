#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Adw, Gio
from src.Config import APP_NAME, VERSION, APP_ID
from src.core.AutostartManager import AutostartManager
from src.core.DesktopActions import DesktopActions
from src.ui.pages.PageWelcome import PageWelcome
from src.ui.pages.PageFirstSteps import PageFirstSteps
from src.ui.pages.PageApps import PageApps
from src.ui.pages.PageCommunity import PageCommunity

class MainWindowAdw(Adw.ApplicationWindow):
    """Pars Welcome ana uygulama penceresi (Libadwaita)."""

    def __init__(self, app):
        super().__init__(application=app, title=APP_NAME)
        self.set_default_size(940, 660)
        self.set_size_request(680, 500)

        # Ana dikey kutu
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)

        # 1. Başlık Çubuğu (HeaderBar)
        header = Adw.HeaderBar()
        main_box.append(header)

        # ViewStack (Sayfa Yığını)
        self.stack = Adw.ViewStack()
        self.stack.set_vexpand(True)

        # ViewSwitcher (Başlık ortasındaki modern sekme geçişi)
        switcher = Adw.ViewSwitcher()
        switcher.set_stack(self.stack)
        switcher.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        header.set_title_widget(switcher)

        # Başlık sağ butonları: Hakkında butonu
        btn_about = Gtk.Button()
        btn_about.set_icon_name("help-about-symbolic")
        btn_about.set_tooltip_text("Hakkında")
        btn_about.connect("clicked", self._on_about_clicked)
        header.pack_end(btn_about)

        # 2. Sayfaları Ekle
        self.page_welcome = PageWelcome(self)
        self.page_first_steps = PageFirstSteps(self)
        self.page_apps = PageApps(self)
        self.page_community = PageCommunity(self)

        self.stack.add_titled_with_icon(
            self.page_welcome, "welcome", "Genel Bakış", "user-home-symbolic"
        )
        self.stack.add_titled_with_icon(
            self.page_first_steps, "first_steps", "İlk Adımlar", "preferences-system-symbolic"
        )
        self.stack.add_titled_with_icon(
            self.page_apps, "apps", "Uygulamalar", "software-store-symbolic"
        )
        self.stack.add_titled_with_icon(
            self.page_community, "community", "Topluluk", "system-users-symbolic"
        )

        main_box.append(self.stack)

        # 3. Alt Durum ve Otomatik Başlatma Çubuğu
        bottom_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        bottom_bar.add_css_class("toolbar")
        bottom_bar.set_margin_start(16)
        bottom_bar.set_margin_end(16)
        bottom_bar.set_margin_top(8)
        bottom_bar.set_margin_bottom(10)

        self.chk_autostart = Gtk.CheckButton(label="Sistem açılışında bu pencereyi göster")
        self.chk_autostart.set_active(AutostartManager.is_enabled())
        self.chk_autostart.connect("toggled", self._on_autostart_toggled)
        bottom_bar.append(self.chk_autostart)

        # Sağ alta minik sürüm etiketi
        lbl_ver = Gtk.Label(label=f"Pars Linux • v{VERSION}")
        lbl_ver.set_hexpand(True)
        lbl_ver.set_halign(Gtk.Align.END)
        lbl_ver.add_css_class("dim-label")
        bottom_bar.append(lbl_ver)

        main_box.append(bottom_bar)

    def switch_page(self, page_name: str):
        """İstenen sayfaya programatik olarak geçiş yapar."""
        self.stack.set_visible_child_name(page_name)

    def _on_autostart_toggled(self, checkbutton: Gtk.CheckButton):
        """Açılışta başlatma ayarını değiştirir."""
        is_active = checkbutton.get_active()
        AutostartManager.set_enabled(is_active)

    def _on_about_clicked(self, button):
        """Modern Adw.AboutWindow diyaloğunu açar."""
        about = Adw.AboutWindow(transient_for=self)
        about.set_application_name(APP_NAME)
        about.set_version(VERSION)
        about.set_developer_name("Pars Linux Ekibi")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_website("https://parslinux.org")
        about.set_issue_url("https://github.com/parslinux/parslinux-welcome/issues")
        about.set_comments(
            "Pars Linux kullanıcıları için tasarlanmış modern karşılama ve başlangıç merkezi."
        )
        about.set_application_icon("org.parslinux.welcome")
        about.present()
