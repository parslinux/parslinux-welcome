#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gi.repository import Gtk, Adw, GLib, Gio
from src.core.WallpaperManager import WallpaperManager
from src.core.I18n import _

class WallpaperDialog(Adw.Window):
    """Masaüstü duvar kağıtlarını listeleyen, aratan ve tek tıkla uygulayan modern galeri penceresi."""

    def __init__(self, parent_window, on_applied_cb=None):
        super().__init__()
        self.set_transient_for(parent_window)
        self.set_modal(True)
        self.set_default_size(880, 620)
        self.set_title(_("Duvar Kağıtları Galerisi"))

        self.parent_window = parent_window
        self.on_applied_cb = on_applied_cb
        self.current_wp_path = WallpaperManager.get_current_wallpaper()

        self.all_wallpapers = WallpaperManager.get_available_wallpapers()
        self.card_widgets = []  # (button, wp_dict, card_box)

        # Ana Kutu
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)

        # 1. HeaderBar
        header = Adw.HeaderBar()
        main_box.append(header)

        # Dosyadan Ekle Butonu
        btn_add = Gtk.Button()
        btn_add.set_icon_name("list-add-symbolic")
        btn_add.set_tooltip_text(_("Dosyadan Özel Duvar Kağıdı Ekle"))
        btn_add.connect("clicked", self._on_add_custom_clicked)
        header.pack_end(btn_add)

        # 2. Arama ve Filtre Çubuğu
        filter_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        filter_box.set_margin_start(18)
        filter_box.set_margin_end(18)
        filter_box.set_margin_top(10)
        filter_box.set_margin_bottom(10)

        # Arama kutusu
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text(_("Duvar kağıdı adı veya kategori ara..."))
        self.search_entry.connect("search-changed", self._on_filter_changed)
        filter_box.append(self.search_entry)

        # Kategori Hap Filtreleri
        cat_scroll = Gtk.ScrolledWindow()
        cat_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        cat_scroll.set_min_content_height(38)

        self.cat_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        cat_scroll.set_child(self.cat_box)
        filter_box.append(cat_scroll)

        self.selected_category = "Tümü"
        self._build_category_buttons()

        main_box.append(filter_box)

        # 3. Kaydırılabilir Galeri (FlowBox)
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_box.append(scroll)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(860)
        clamp.set_tightening_threshold(640)
        scroll.set_child(clamp)

        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(4)
        self.flowbox.set_min_children_per_line(2)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_homogeneous(True)
        self.flowbox.set_column_spacing(12)
        self.flowbox.set_row_spacing(14)
        self.flowbox.set_margin_start(16)
        self.flowbox.set_margin_end(16)
        self.flowbox.set_margin_top(8)
        self.flowbox.set_margin_bottom(24)
        clamp.set_child(self.flowbox)

        # Duvar kağıdı kartlarını doldur
        self._populate_wallpapers()

    def _build_category_buttons(self):
        """Mevcut duvar kağıtlarının kategorilerinden filtre hapları üretir."""
        all_label = _("Tümü")
        categories = [all_label]
        for wp in self.all_wallpapers:
            cat = wp.get("category", "")
            if cat and cat not in categories:
                categories.append(cat)

        self.cat_buttons = {}
        for cat in categories:
            btn = Gtk.Button(label=cat)
            btn.add_css_class("pill-badge")
            if cat == all_label:
                btn.add_css_class("suggested-action")
            else:
                btn.add_css_class("flat")
            btn.connect("clicked", lambda b, c=cat: self._on_category_clicked(c))
            self.cat_box.append(btn)
            self.cat_buttons[cat] = btn

    def _on_category_clicked(self, cat: str):
        """Kategori filtresini günceller."""
        self.selected_category = cat
        all_label = _("Tümü")
        for c, btn in self.cat_buttons.items():
            if c == cat:
                btn.add_css_class("suggested-action")
                btn.remove_css_class("flat")
            else:
                btn.remove_css_class("suggested-action")
                btn.add_css_class("flat")
        self._on_filter_changed()

    def _populate_wallpapers(self):
        """Tüm duvar kağıtlarını FlowBox içerisine kart olarak ekler."""
        for wp in self.all_wallpapers:
            card = self._create_wallpaper_card(wp)
            self.flowbox.append(card)
            self.card_widgets.append((card, wp))

    def _create_wallpaper_card(self, wp: dict) -> Gtk.Button:
        """Tek bir duvar kağıdı için önizlemeli modern kart oluşturur."""
        btn = Gtk.Button()
        btn.add_css_class("wallpaper-card")
        
        is_active = (wp["path"] == self.current_wp_path)
        if is_active:
            btn.add_css_class("active")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Thumbnail Görseli
        pic = Gtk.Picture.new_for_filename(wp["path"])
        if hasattr(Gtk, "ContentFit"):
            pic.set_content_fit(Gtk.ContentFit.COVER)
        pic.set_size_request(180, 110)
        pic.add_css_class("wallpaper-thumb")
        box.append(pic)

        # Başlık ve Rozet Kutusu
        row_info = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        
        lbl_title = Gtk.Label(label=wp["name"])
        lbl_title.add_css_class("wallpaper-title")
        lbl_title.set_halign(Gtk.Align.START)
        lbl_title.set_ellipsize(3)  # PANGO_ELLIPSIZE_END
        lbl_title.set_hexpand(True)
        row_info.append(lbl_title)

        if is_active:
            badge = Gtk.Label(label=_("Aktif"))
            badge.add_css_class("pill-badge")
            badge.add_css_class("installed")
            row_info.append(badge)

        box.append(row_info)
        btn.set_child(box)

        btn.connect("clicked", lambda b, w=wp: self._on_card_clicked(b, w))
        return btn

    def _on_card_clicked(self, clicked_btn: Gtk.Button, wp: dict):
        """Duvar kağıdını anında uygular ve arayüzü günceller."""
        success = WallpaperManager.set_wallpaper(wp["path"])
        if success:
            self.current_wp_path = wp["path"]
            
            # Kartların aktif durumlarını tazele
            for card, item in self.card_widgets:
                is_cur = (item["path"] == self.current_wp_path)
                if is_cur:
                    card.add_css_class("active")
                else:
                    card.remove_css_class("active")

                # Rozeti güncelle
                box = card.get_child()
                if box:
                    last_child = box.get_last_child()
                    if isinstance(last_child, Gtk.Box):
                        # Varsa eski rozeti temizle
                        if last_child.get_last_child() and isinstance(last_child.get_last_child(), Gtk.Label) and last_child.get_last_child().get_text() == _("Aktif"):
                            last_child.remove(last_child.get_last_child())
                        if is_cur:
                            b = Gtk.Label(label=_("Aktif"))
                            b.add_css_class("pill-badge")
                            b.add_css_class("installed")
                            last_child.append(b)

            if hasattr(self.parent_window, "show_toast"):
                self.parent_window.show_toast(f"'{wp['name']}' {_('duvar kağıdı uygulandı.')}")

            if self.on_applied_cb:
                self.on_applied_cb(wp["path"])
        else:
            if hasattr(self.parent_window, "show_toast"):
                self.parent_window.show_toast(_("Duvar kağıdı uygulanamadı!"))

    def _on_filter_changed(self, *args):
        """Arama metni ve seçilen kategoriye göre kartları filtreler."""
        query = self.search_entry.get_text().strip().lower()
        selected_cat = self.selected_category
        all_label = _("Tümü")

        for card, wp in self.card_widgets:
            name_match = query in wp["name"].lower() if query else True
            cat_match = (selected_cat == all_label or wp.get("category", "") == selected_cat)
            
            card.set_visible(name_match and cat_match)

    def _on_add_custom_clicked(self, button):
        """Kullanıcının kendi yerel diskindeki bir resmi seçmesi için dosya seçici açar."""
        if hasattr(Gtk, "FileDialog"):
            dialog = Gtk.FileDialog()
            dialog.set_title(_("Duvar Kağıdı Resmi Seç"))
            
            # Resim filtresi
            f_img = Gtk.FileFilter()
            f_img.set_name(_("Resim Dosyaları (*.jpg, *.png, *.svg, *.webp)"))
            for mime in ["image/png", "image/jpeg", "image/svg+xml", "image/webp"]:
                f_img.add_mime_type(mime)
            
            filters = Gio.ListStore.new(Gtk.FileFilter)
            filters.append(f_img)
            dialog.set_filters(filters)
            dialog.set_default_filter(f_img)

            dialog.open(self, None, self._on_file_dialog_finish)
        else:
            chooser = Gtk.FileChooserNative.new(
                "Duvar Kağıdı Resmi Seç",
                self,
                Gtk.FileChooserAction.OPEN,
                "Seç ve Uygula",
                "İptal"
            )
            f = Gtk.FileFilter()
            f.set_name("Resim Dosyaları")
            f.add_mime_type("image/png")
            f.add_mime_type("image/jpeg")
            f.add_mime_type("image/svg+xml")
            f.add_mime_type("image/webp")
            chooser.add_filter(f)
            chooser.connect("response", self._on_native_chooser_response)
            chooser.show()

    def _on_file_dialog_finish(self, dialog, result):
        """Gtk.FileDialog tamamlandığında seçilen dosyayı uygular."""
        try:
            gfile = dialog.open_finish(result)
            if gfile:
                path = gfile.get_path()
                self._apply_custom_file(path)
        except Exception as e:
            print(f"Dosya seçme iptal veya hata: {e}")

    def _on_native_chooser_response(self, chooser, response_id):
        """Gtk.FileChooserNative tamamlandığında dosyayı uygular."""
        if response_id == Gtk.ResponseType.ACCEPT:
            gfile = chooser.get_file()
            if gfile:
                self._apply_custom_file(gfile.get_path())

    def _apply_custom_file(self, path: str):
        """Seçilen harici resmi kaydeder, kart oluşturur ve arka plan olarak ayarlar."""
        if not path or not os.path.exists(path):
            return
        
        WallpaperManager.add_custom_wallpaper(path)
        fname = os.path.basename(path)
        clean_name = fname.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()
        
        new_wp = {
            "id": fname,
            "name": clean_name,
            "path": path,
            "category": "Özel",
            "is_bundled": False
        }
        
        # Kartı oluştur ve listeye ekle
        card = self._create_wallpaper_card(new_wp)
        self.flowbox.prepend(card)
        self.card_widgets.insert(0, (card, new_wp))
        
        # Anında uygula
        self._on_card_clicked(card, new_wp)
