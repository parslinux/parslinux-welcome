#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, GLib, Pango

class StatCard(Gtk.Box):
    """Modern dashboard donanım istatistik kartı."""

    def __init__(self, title: str, value: str, icon_name: str, subtitle: str = "", fraction: float = -1.0):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.add_css_class("stat-card")
        self.set_hexpand(True)

        # Sol İkon Kutusu
        icon_img = Gtk.Image.new_from_icon_name(icon_name)
        icon_img.set_pixel_size(32)
        icon_img.set_valign(Gtk.Align.CENTER)
        self.append(icon_img)

        # Sağ İçerik Kutusu
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        content_box.set_hexpand(True)
        self.append(content_box)

        # Başlık (Küçük, büyük harf)
        lbl_title = Gtk.Label(label=title)
        lbl_title.add_css_class("stat-card-title")
        lbl_title.set_halign(Gtk.Align.START)
        content_box.append(lbl_title)

        # Ana Değer
        lbl_val = Gtk.Label(label=value)
        lbl_val.add_css_class("stat-card-value")
        lbl_val.set_halign(Gtk.Align.START)
        lbl_val.set_wrap(True)
        lbl_val.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        content_box.append(lbl_val)

        # İlerleme Çubuğu (Varsa)
        if fraction >= 0.0:
            pbar = Gtk.ProgressBar()
            pbar.add_css_class("stat-bar")
            pbar.set_fraction(fraction)
            content_box.append(pbar)

        # Alt Bilgi (Subtitle)
        if subtitle:
            lbl_sub = Gtk.Label(label=subtitle)
            lbl_sub.add_css_class("dim-label")
            lbl_sub.set_halign(Gtk.Align.START)
            content_box.append(lbl_sub)
