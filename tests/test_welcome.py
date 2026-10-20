#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json
import os
from src.core.SystemInfo import SystemInfo
from src.core.AutostartManager import AutostartManager
from src.Config import load_config, get_data_path

class TestParsWelcome(unittest.TestCase):
    """Pars Welcome temel mantık ve yapılandırma testleri."""

    def test_system_info_summary(self):
        info = SystemInfo.get_all_summary()
        self.assertIn("os_name", info)
        self.assertIn("kernel", info)
        self.assertIn("desktop", info)
        self.assertIn("cpu", info)
        self.assertIn("ram", info)
        self.assertIn("disk", info)
        self.assertIn("arch", info)
        self.assertTrue(len(info["kernel"]) > 0)

    def test_apps_json_schema(self):
        apps_file = get_data_path("apps.json")
        self.assertTrue(os.path.exists(apps_file), "apps.json bulunamadı!")
        with open(apps_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("categories", data)
        self.assertGreater(len(data["categories"]), 0)
        for cat in data["categories"]:
            self.assertIn("name", cat)
            self.assertIn("apps", cat)
            for app in cat["apps"]:
                self.assertIn("name", app)
                self.assertIn("desc", app)

    def test_links_json_schema(self):
        links_file = get_data_path("links.json")
        self.assertTrue(os.path.exists(links_file), "links.json bulunamadı!")
        with open(links_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("links", data)
        self.assertGreater(len(data["links"]), 0)
        for link in data["links"]:
            self.assertIn("title", link)
            self.assertIn("url", link)
            self.assertTrue(link["url"].startswith("http"))

    def test_config_defaults(self):
        cfg = load_config()
        self.assertIn("show_on_startup", cfg)
        self.assertIn("theme_mode", cfg)

    def test_wallpaper_manager(self):
        from src.core.WallpaperManager import WallpaperManager
        wps = WallpaperManager.get_available_wallpapers()
        self.assertIsInstance(wps, list)
        self.assertGreater(len(wps), 0, "En az bir duvar kağıdı bulunmalıdır!")
        
        # Pars Linux dahili duvar kağıdı varlığını doğrula
        bundled = [w for w in wps if w.get("is_bundled")]
        self.assertGreaterEqual(len(bundled), 2, "Pars Linux dahili duvar kağıtları yüklenmeli!")
        for wp in bundled:
            self.assertTrue(os.path.exists(wp["path"]))
            self.assertIn("Pars", wp["name"])

        # get_current_wallpaper metodu hata vermemeli
        cur = WallpaperManager.get_current_wallpaper()
        self.assertIsInstance(cur, str)

    def test_i18n_support(self):
        from src.core.I18n import set_language, _, get_current_language
        
        # MO dosyaları varlığı
        tr_mo = get_data_path("locale/tr/LC_MESSAGES/parslinux-welcome.mo")
        en_mo = get_data_path("locale/en/LC_MESSAGES/parslinux-welcome.mo")
        self.assertTrue(os.path.exists(tr_mo), "tr.mo dosyası bulunamadı!")
        self.assertTrue(os.path.exists(en_mo), "en.mo dosyası bulunamadı!")

        # İngilizce çeviri testi
        set_language("en", save=False)
        self.assertEqual(_("İlk Adımlar"), "First Steps")
        self.assertEqual(_("Uygulamalar"), "Applications")
        self.assertEqual(_("Genel Bakış"), "Overview")

        # Türkçe çeviri testi
        set_language("tr", save=False)
        self.assertEqual(_("İlk Adımlar"), "İlk Adımlar")
        self.assertEqual(_("Uygulamalar"), "Uygulamalar")

    def test_driver_manager(self):
        from src.core.DriverManager import DriverManager
        gpus = DriverManager.get_gpus()
        self.assertIsInstance(gpus, list)
        self.assertGreater(len(gpus), 0, "Sistemde en az bir ekran kartı tespit edilmelidir!")
        for g in gpus:
            self.assertIn("model", g)
            self.assertIn("vendor", g)
            self.assertIn("driver", g)
            self.assertIn("status", g)
            self.assertIn("badge_type", g)

        wifis = DriverManager.get_wifis()
        self.assertIsInstance(wifis, list)
        for w in wifis:
            self.assertIn("model", w)
            self.assertIn("driver", w)
            self.assertIn("status", w)
            self.assertIn("badge_type", w)

if __name__ == "__main__":
    unittest.main()
