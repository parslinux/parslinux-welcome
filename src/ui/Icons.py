#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gi.repository import Gtk, Gdk, GLib
from src.Config import get_data_path

# --- KOD İÇİNE GÖMÜLÜ KORUMALI SVG İKONLARI ---

SVG_LIGHT_MODE = """<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 32 32">
  <circle cx="16" cy="16" r="6.5" fill="#f6d32d" stroke="#e5a50a" stroke-width="1.5"/>
  <g stroke="#e5a50a" stroke-width="2.2" stroke-linecap="round">
    <line x1="16" y1="2" x2="16" y2="5.5"/>
    <line x1="16" y1="26.5" x2="16" y2="30"/>
    <line x1="2" y1="16" x2="5.5" y2="16"/>
    <line x1="26.5" y1="16" x2="30" y2="16"/>
    <line x1="6.1" y1="6.1" x2="8.6" y2="8.6"/>
    <line x1="23.4" y1="23.4" x2="25.9" y2="25.9"/>
    <line x1="6.1" y1="25.9" x2="8.6" y2="23.4"/>
    <line x1="23.4" y1="8.6" x2="25.9" y2="6.1"/>
  </g>
</svg>"""

SVG_DARK_MODE = """<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 32 32">
  <path d="M 23 18 C 22 23.5, 17 27, 11 26 C 8 25.5, 6 24, 4 22 C 8 22, 16 19, 18 10 C 18.5 7.5, 17.5 5, 16 3 C 21 4, 25 9.5, 23 18 Z" 
        fill="#99c1f1" stroke="#62a0ea" stroke-width="1.5"/>
  <path d="M 24 6 Q 24 8 26 8 Q 24 8 24 10 Q 24 8 22 8 Q 24 8 24 6 Z" fill="#f6d32d"/>
</svg>"""

SVG_SYSTEM_MODE = """<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 32 32">
  <circle cx="16" cy="16" r="12" fill="none" stroke="#77767b" stroke-width="2.5"/>
  <path d="M 16 4 A 12 12 0 0 1 16 28 Z" fill="#77767b"/>
</svg>"""

SVG_CPU = """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
  <rect x="8" y="8" width="16" height="16" rx="2" fill="#3584e4" stroke="#1c71d8" stroke-width="1.5"/>
  <rect x="11" y="11" width="10" height="10" rx="1" fill="#ffffff" opacity="0.3"/>
  <g stroke="#3584e4" stroke-width="2" stroke-linecap="round">
    <line x1="12" y1="4" x2="12" y2="7"/><line x1="16" y1="4" x2="16" y2="7"/><line x1="20" y1="4" x2="20" y2="7"/>
    <line x1="12" y1="25" x2="12" y2="28"/><line x1="16" y1="25" x2="16" y2="28"/><line x1="20" y1="25" x2="20" y2="28"/>
    <line x1="4" y1="12" x2="7" y2="12"/><line x1="4" y1="16" x2="7" y2="16"/><line x1="4" y1="20" x2="7" y2="20"/>
    <line x1="25" y1="12" x2="28" y2="12"/><line x1="25" y1="16" x2="28" y2="16"/><line x1="25" y1="20" x2="28" y2="20"/>
  </g>
</svg>"""

SVG_GPU = """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
  <rect x="5" y="7" width="22" height="16" rx="2" fill="#2ec27e" stroke="#26a269" stroke-width="1.5"/>
  <rect x="7" y="9" width="18" height="12" rx="1" fill="#ffffff" opacity="0.3"/>
  <circle cx="16" cy="15" r="4" fill="none" stroke="#ffffff" stroke-width="2"/>
  <line x1="10" y1="26" x2="22" y2="26" stroke="#26a269" stroke-width="3" stroke-linecap="round"/>
</svg>"""

SVG_RAM = """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
  <rect x="4" y="10" width="24" height="12" rx="2" fill="#e66100" stroke="#c64600" stroke-width="1.5"/>
  <g stroke="#ffffff" stroke-width="2">
    <line x1="9" y1="13" x2="9" y2="19"/><line x1="13" y1="13" x2="13" y2="19"/>
    <line x1="19" y1="13" x2="19" y2="19"/><line x1="23" y1="13" x2="23" y2="19"/>
  </g>
  <g stroke="#c64600" stroke-width="2" stroke-linecap="round">
    <line x1="7" y1="22" x2="7" y2="25"/><line x1="11" y1="22" x2="11" y2="25"/>
    <line x1="15" y1="22" x2="15" y2="25"/><line x1="19" y1="22" x2="19" y2="25"/>
    <line x1="23" y1="22" x2="23" y2="25"/>
  </g>
</svg>"""

SVG_DISK = """<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
  <rect x="6" y="6" width="20" height="20" rx="3" fill="#9141ac" stroke="#813d9c" stroke-width="1.5"/>
  <circle cx="16" cy="16" r="6" fill="none" stroke="#ffffff" stroke-width="2"/>
  <circle cx="16" cy="16" r="2" fill="#ffffff"/>
  <circle cx="22" cy="22" r="1.5" fill="#2ec27e"/>
</svg>"""

INTERNAL_SVGS = {
    "light-mode": SVG_LIGHT_MODE,
    "dark-mode": SVG_DARK_MODE,
    "system-mode": SVG_SYSTEM_MODE,
    "hardware-chip-symbolic": SVG_CPU,
    "video-display-symbolic": SVG_GPU,
    "drive-harddisk-symbolic": SVG_DISK,
}

SYMBOLIC_ALIASES = {
    "software-store-symbolic": "system-software-install-symbolic",
    "preferences-desktop-theme-symbolic": "preferences-desktop-appearance-symbolic",
    "external-link-symbolic": "adw-external-link-symbolic",
    "globe-symbolic": "web-browser-symbolic",
}

_texture_cache = {}

class Icons:
    """Sistem temasından bağımsız, kod içine gömülü çalışan güvenli ikon yöneticisi."""

    @classmethod
    def get_texture_from_svg(cls, svg_str: str) -> Gdk.Texture:
        """SVG metnini Gdk.Texture nesnesine dönüştürür ve bellek önbelleğinde saklar."""
        if svg_str in _texture_cache:
            return _texture_cache[svg_str]
        
        bytes_data = GLib.Bytes.new(svg_str.encode("utf-8"))
        texture = Gdk.Texture.new_from_bytes(bytes_data)
        _texture_cache[svg_str] = texture
        return texture

    @classmethod
    def create_image(cls, icon_name: str, pixel_size: int = 32) -> Gtk.Image:
        """
        Kod içine gömülü SVG'leri ve güvenli fallback haritasını önceliklendirerek
        kesintisiz ve kırılmayan Gtk.Image üretir.
        """
        # 1. Bilinen alias/eşleme kontrolü
        resolved_name = SYMBOLIC_ALIASES.get(icon_name, icon_name)

        # 2. Dahili SVG önceliği
        if resolved_name in INTERNAL_SVGS:
            texture = cls.get_texture_from_svg(INTERNAL_SVGS[resolved_name])
            img = Gtk.Image.new_from_paintable(texture)
            img.set_pixel_size(pixel_size)
            return img

        # 3. Sistem temasını kontrol et
        display = Gdk.Display.get_default()
        if display:
            theme = Gtk.IconTheme.get_for_display(display)
            if theme.has_icon(resolved_name):
                img = Gtk.Image.new_from_icon_name(resolved_name)
                img.set_pixel_size(pixel_size)
                return img

        # 4. Akıllı anahtar kelime eşleme ve fallback
        if "light" in icon_name or "sun" in icon_name or "bright" in icon_name:
            texture = cls.get_texture_from_svg(SVG_LIGHT_MODE)
            img = Gtk.Image.new_from_paintable(texture)
            img.set_pixel_size(pixel_size)
            return img
        elif "dark" in icon_name or "night" in icon_name:
            texture = cls.get_texture_from_svg(SVG_DARK_MODE)
            img = Gtk.Image.new_from_paintable(texture)
            img.set_pixel_size(pixel_size)
            return img
        elif "system" in icon_name:
            texture = cls.get_texture_from_svg(SVG_SYSTEM_MODE)
            img = Gtk.Image.new_from_paintable(texture)
            img.set_pixel_size(pixel_size)
            return img
        elif "chip" in icon_name or "cpu" in icon_name:
            texture = cls.get_texture_from_svg(SVG_CPU)
            img = Gtk.Image.new_from_paintable(texture)
            img.set_pixel_size(pixel_size)
            return img
        elif "video" in icon_name or "display" in icon_name or "gpu" in icon_name:
            texture = cls.get_texture_from_svg(SVG_GPU)
            img = Gtk.Image.new_from_paintable(texture)
            img.set_pixel_size(pixel_size)
            return img
        elif "disk" in icon_name or "drive" in icon_name:
            texture = cls.get_texture_from_svg(SVG_DISK)
            img = Gtk.Image.new_from_paintable(texture)
            img.set_pixel_size(pixel_size)
            return img

        # 5. Güvenli genel fallback (soru işareti göstermemek için)
        if display:
            theme = Gtk.IconTheme.get_for_display(display)
            for fallback in ["application-x-executable-symbolic", "package-x-generic-symbolic"]:
                if theme.has_icon(fallback):
                    img = Gtk.Image.new_from_icon_name(fallback)
                    img.set_pixel_size(pixel_size)
                    return img

        img = Gtk.Image.new_from_icon_name("application-x-executable-symbolic")
        img.set_pixel_size(pixel_size)
        return img

    @classmethod
    def create_app_image(cls, app: dict, pixel_size: int = 34) -> Gtk.Image:
        """
        Uygulamalar sayfası için yerel paketlenmiş yüksek kaliteli SVG/PNG ikonlarını
        veya sistem ikonlarını kullanarak net, kırılmayan bir Gtk.Image üretir.
        """
        app_id = app.get("id", "")
        icon_name = app.get("icon", "")

        # 1. data/icons/apps/ altındaki yerel yüksek kaliteli ikon dosyalarını kontrol et
        candidates = [
            f"icons/apps/{app_id}.svg",
            f"icons/apps/{app_id}.png",
            f"icons/apps/{icon_name}.svg",
            f"icons/apps/{icon_name}.png",
        ]
        for candidate in candidates:
            path = get_data_path(candidate)
            if os.path.exists(path):
                img = Gtk.Image.new_from_file(path)
                img.set_pixel_size(pixel_size)
                return img

        # 2. Sistem temasını kontrol et
        display = Gdk.Display.get_default()
        if display and icon_name:
            theme = Gtk.IconTheme.get_for_display(display)
            if theme.has_icon(icon_name):
                img = Gtk.Image.new_from_icon_name(icon_name)
                img.set_pixel_size(pixel_size)
                return img

        # 3. Kategoriye göre genel yedek simge
        category_fallbacks = {
            "internet": "applications-internet-symbolic",
            "development": "applications-development-symbolic",
            "multimedia": "applications-multimedia-symbolic",
            "office": "applications-office-symbolic"
        }
        fallback_icon = category_fallbacks.get(app.get("category", ""), "application-x-executable-symbolic")
        return cls.create_image(fallback_icon, pixel_size=pixel_size)
