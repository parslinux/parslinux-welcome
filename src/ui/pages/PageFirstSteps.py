#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Adw, GLib
from src.core.DesktopActions import DesktopActions
from src.core.WallpaperManager import WallpaperManager
from src.core.I18n import _, get_current_language, set_language
from src.Config import load_config, save_config
from src.ui.Icons import Icons
from src.ui.widgets.WallpaperDialog import WallpaperDialog

class PageFirstSteps(Gtk.Box):
    """İlk Adımlar sayfası: Görsel tema seçimi, duvar kağıtları, ekran ayarları ve sistem yönetimi."""

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

        # 2. Masaüstü Duvar Kağıdı Seçicisi
        self._build_wallpaper_section(box_content)

        # 3. Ekran ve Kişiselleştirme
        self._build_customization_section(box_content)

        # 4. Sistem Yönetim ve Bakım Araçları
        self._build_management_section(box_content)

    def _build_theme_cards_section(self, container):
        """Kullanıcının tek tıkla Açık, Koyu veya Sistem temasını seçebileceği görsel kartlar."""
        group_theme = Adw.PreferencesGroup()
        group_theme.set_title(_("Görünüm ve Renk Teması"))
        group_theme.set_description(_("Masaüstü ve uygulama arayüzü renk stilinizi belirleyin"))

        # 3 sütunlu kart kutusu
        box_cards = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
        box_cards.set_homogeneous(True)
        box_cards.set_margin_top(6)

        current_theme = load_config().get("theme_mode", "system")
        self.theme_widgets = {}

        # 1. Açık Tema Kartı
        card_light = self._create_theme_card(_("Açık Tema"), "light-mode", "light", current_theme == "light")
        # 2. Koyu Tema Kartı
        card_dark = self._create_theme_card(_("Koyu Tema"), "dark-mode", "dark", current_theme == "dark")
        # 3. Sistem Varsayılanı Kartı
        card_system = self._create_theme_card(_("Sistem"), "system-mode", "system", current_theme == "system")

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

        icon = Icons.create_image(icon_name, pixel_size=36)
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

    def _build_wallpaper_section(self, container):
        """Masaüstü duvar kağıdı hızlı seçim şeridi ve tam galeriye erişim bölümü."""
        group_wp = Adw.PreferencesGroup()
        group_wp.set_title(_("Masaüstü Arka Planı"))
        group_wp.set_description(_("Pars Linux temalı veya sistem duvar kağıtlarını uygulayın"))

        all_wps = WallpaperManager.get_available_wallpapers()
        # İlk 4 tanesini (Pars Linux) şerit olarak listele
        featured_wps = all_wps[:4]
        current_wp = WallpaperManager.get_current_wallpaper()

        box_featured = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box_featured.set_homogeneous(True)
        box_featured.set_margin_top(6)
        box_featured.set_margin_bottom(10)

        self.featured_wp_cards = []

        for wp in featured_wps:
            card = self._create_featured_wallpaper_card(wp, wp["path"] == current_wp)
            box_featured.append(card)
            self.featured_wp_cards.append((card, wp))

        box_wrap = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_wrap.append(box_featured)
        group_wp.add(box_wrap)

        # Tüm Galeri Aksiyon Satırı
        row_gallery = Adw.ActionRow()
        row_gallery.set_title(_("Tüm Duvar Kağıtları Galerisi"))
        row_gallery.set_subtitle(f"{_('Mevcut')} {len(all_wps)} {_('adet duvar kağıdını inceleyin, filtreleyin ve arayın')}")
        row_gallery.set_icon_name("preferences-desktop-wallpaper-symbolic")

        btn_gallery = Gtk.Button(label=_("Galeriyi Aç"))
        btn_gallery.set_valign(Gtk.Align.CENTER)
        btn_gallery.connect("clicked", self._open_wallpaper_gallery)
        row_gallery.add_suffix(btn_gallery)
        row_gallery.set_activatable_widget(btn_gallery)
        group_wp.add(row_gallery)

        container.append(group_wp)

    def _create_featured_wallpaper_card(self, wp: dict, is_active: bool) -> Gtk.Button:
        """Hızlı seçim şeridindeki tek bir duvar kağıdı kartı."""
        btn = Gtk.Button()
        btn.add_css_class("wallpaper-card")
        if is_active:
            btn.add_css_class("active")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        pic = Gtk.Picture.new_for_filename(wp["path"])
        if hasattr(Gtk, "ContentFit"):
            pic.set_content_fit(Gtk.ContentFit.COVER)
        pic.set_size_request(140, 85)
        pic.add_css_class("wallpaper-thumb")
        box.append(pic)

        lbl = Gtk.Label(label=wp["name"])
        lbl.add_css_class("wallpaper-title")
        lbl.set_ellipsize(3)
        lbl.set_halign(Gtk.Align.CENTER)
        box.append(lbl)

        btn.set_child(box)
        btn.connect("clicked", lambda b, p=wp["path"], n=wp["name"]: self._on_featured_wp_clicked(p, n))
        return btn

    def _on_featured_wp_clicked(self, path: str, name: str):
        """Şeritteki duvar kağıdına tıklandığında uygular."""
        if WallpaperManager.set_wallpaper(path):
            self._refresh_featured_wallpapers(path)
            if hasattr(self.main_window, "show_toast"):
                self.main_window.show_toast(f"'{name}' {_('duvar kağıdı uygulandı.')}")
        else:
            if hasattr(self.main_window, "show_toast"):
                self.main_window.show_toast(_("Duvar kağıdı uygulanamadı!"))

    def _refresh_featured_wallpapers(self, current_path: str):
        """Aktif seçilen duvar kağıdına göre şerit üzerindeki rozetleri tazeler."""
        for card, wp in self.featured_wp_cards:
            if wp["path"] == current_path:
                card.add_css_class("active")
            else:
                card.remove_css_class("active")

    def _open_wallpaper_gallery(self, *args):
        """Tam ekran duvar kağıdı seçici modal penceresini açar."""
        dialog = WallpaperDialog(self.main_window, on_applied_cb=self._refresh_featured_wallpapers)
        dialog.present()

    def _build_customization_section(self, container):
        """Ekran, çözünürlük ve görünüm ayarları."""
        group_cust = Adw.PreferencesGroup()
        group_cust.set_title(_("Kişiselleştirme"))
        group_cust.set_description(_("Monitör ve ekran görüntüleme seçenekleri"))

        # Ekran Çözünürlüğü ve Ölçekleme
        row_display = Adw.ActionRow()
        row_display.set_title(_("Ekran Çözünürlüğü ve Ölçekleme"))
        row_display.set_subtitle(_("Monitör yenileme hızı, çözünürlük ve HiDPI (100% / 200%) ölçekleme"))
        row_display.set_icon_name("preferences-desktop-display-symbolic")

        btn_display = Gtk.Button(label=_("Yapılandır"))
        btn_display.set_valign(Gtk.Align.CENTER)
        btn_display.connect("clicked", lambda b: DesktopActions.open_display_settings())
        row_display.add_suffix(btn_display)
        row_display.set_activatable_widget(btn_display)
        group_cust.add(row_display)

        # Dil Seçimi (Language Selector)
        row_lang = Adw.ActionRow()
        row_lang.set_title(_("Uygulama Dili"))
        row_lang.set_subtitle(_("Karşılama merkezinin arayüz dilini belirleyin"))
        row_lang.set_icon_name("preferences-desktop-locale-symbolic")

        lang_options = [
            ("system", _("Sistem Varsayılanı")),
            ("tr", "Türkçe (TR)"),
            ("en", "English (EN)")
        ]
        lang_model = Gtk.StringList.new([opt_label for opt_code, opt_label in lang_options])
        drop_lang = Gtk.DropDown.new(lang_model, None)
        drop_lang.set_valign(Gtk.Align.CENTER)

        cur_lang = get_current_language()
        for idx, (code, name) in enumerate(lang_options):
            if code == cur_lang:
                drop_lang.set_selected(idx)
                break

        def on_lang_changed(drop, param):
            idx = drop.get_selected()
            selected_code = lang_options[idx][0]
            set_language(selected_code)
            if hasattr(self.main_window, "show_toast"):
                self.main_window.show_toast(
                    _("Dil ayarı kaydedildi. Uygulandığını görmek için pencereyi yeniden başlatın.")
                )

        drop_lang.connect("notify::selected", on_lang_changed)
        row_lang.add_suffix(drop_lang)
        group_cust.add(row_lang)

        container.append(group_cust)

    def _build_management_section(self, container):
        """Sistem bakım, güncelleme ve yedekleme araçları."""
        group_tools = Adw.PreferencesGroup()
        group_tools.set_title(_("Sistem Yönetimi ve Güvenlik"))
        group_tools.set_description(_("Güncellemeler, yedekleme ve denetim masası"))

        # Pars Update
        row_update = Adw.ActionRow()
        row_update.set_title(_("Pars Update (Paket Güncelleyici)"))
        row_update.set_subtitle(_("Dağıtım paketlerini, çekirdeği ve güvenlik yamalarını güncelleyin"))
        row_update.set_icon_name("software-update-available-symbolic")

        btn_update = Gtk.Button(label=_("Güncelle"))
        btn_update.add_css_class("suggested-action")
        btn_update.set_valign(Gtk.Align.CENTER)
        btn_update.connect("clicked", lambda b: DesktopActions.launch_pars_update())
        row_update.add_suffix(btn_update)
        row_update.set_activatable_widget(btn_update)
        group_tools.add(row_update)

        # Sistem Yedekleme
        row_backup = Adw.ActionRow()
        row_backup.set_title(_("Sistem Anlık Görüntüsü (Snapshot)"))
        row_backup.set_subtitle(_("Olası bir sistem arızasında sistemi geri yüklemek için yedek oluşturun"))
        row_backup.set_icon_name("drive-multidisk-symbolic")

        btn_backup = Gtk.Button(label=_("Yedekle"))
        btn_backup.set_valign(Gtk.Align.CENTER)
        btn_backup.connect("clicked", lambda b: DesktopActions.open_backup_tool())
        row_backup.add_suffix(btn_backup)
        row_backup.set_activatable_widget(btn_backup)
        group_tools.add(row_backup)

        # Sistem Ayarları
        row_settings = Adw.ActionRow()
        row_settings.set_title(_("Sistem Kontrol Merkezi"))
        row_settings.set_subtitle(_("Ağ, Bluetooth, ses, kullanıcılar ve tüm donanım seçenekleri"))
        row_settings.set_icon_name("preferences-system-symbolic")

        btn_settings = Gtk.Button(label=_("Ayarlar"))
        btn_settings.set_valign(Gtk.Align.CENTER)
        btn_settings.connect("clicked", lambda b: DesktopActions.open_system_settings())
        row_settings.add_suffix(btn_settings)
        row_settings.set_activatable_widget(btn_settings)
        group_tools.add(row_settings)

        container.append(group_tools)
