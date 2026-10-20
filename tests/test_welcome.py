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

if __name__ == "__main__":
    unittest.main()
