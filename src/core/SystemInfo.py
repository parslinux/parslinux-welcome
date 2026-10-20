#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import shutil
import subprocess
from typing import Dict

class SystemInfo:
    """Pars Linux sistem, donanım ve masaüstü bilgilerini toplayan sınıf."""

    @staticmethod
    def get_os_info() -> Dict[str, str]:
        """İşletim sistemi adı, sürümü ve logosunu /etc/os-release üzerinden alır."""
        info = {
            "name": "Pars Linux",
            "version": "",
            "codename": "",
            "id": "parslinux",
            "pretty_name": "Pars Linux"
        }
        
        os_release_path = "/etc/os-release"
        if os.path.exists(os_release_path):
            try:
                with open(os_release_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            v = v.strip('"\'')
                            if k == "NAME":
                                info["name"] = v
                            elif k == "VERSION":
                                info["version"] = v
                            elif k == "VERSION_CODENAME":
                                info["codename"] = v
                            elif k == "ID":
                                info["id"] = v
                            elif k == "PRETTY_NAME":
                                info["pretty_name"] = v
            except Exception:
                pass
                
        return info

    @staticmethod
    def get_kernel() -> str:
        """Çekirdek sürümünü döner."""
        return platform.release()

    @staticmethod
    def get_desktop_environment() -> str:
        """Kullanılan masaüstü ortamını (GNOME, XFCE, KDE vb.) tespit eder."""
        xdg_current = os.environ.get("XDG_CURRENT_DESKTOP", "")
        if xdg_current:
            # Örn: "GNOME", "XFCE", "KDE"
            return xdg_current.split(":")[-1].strip()
        desktop_session = os.environ.get("DESKTOP_SESSION", "")
        if desktop_session:
            return desktop_session.capitalize()
        return "Bilinmiyor"

    @staticmethod
    def get_cpu_info() -> str:
        """İşlemci model adını döner."""
        cpu_name = "Bilinmiyor"
        try:
            if os.path.exists("/proc/cpuinfo"):
                with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                    for line in f:
                        if "model name" in line:
                            cpu_name = line.split(":", 1)[1].strip()
                            break
        except Exception:
            cpu_name = platform.processor() or "İşlemci"
            
        # Gereksiz boşlukları ve patent sembollerini temizle
        clean_name = cpu_name.replace("(R)", "").replace("(TM)", "").replace("CPU", "").strip()
        return " ".join(clean_name.split())

    @staticmethod
    def get_ram_info() -> str:
        """Toplam ve kullanılabilir RAM miktarını döner (GB formatında)."""
        try:
            total_kb = 0
            if os.path.exists("/proc/meminfo"):
                with open("/proc/meminfo", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("MemTotal:"):
                            total_kb = int(line.split()[1])
                            break
            if total_kb > 0:
                total_gb = round(total_kb / (1024 * 1024), 1)
                return f"{total_gb} GB RAM"
        except Exception:
            pass
        return "Bellek Bilgisi Alınamadı"

    @staticmethod
    def get_disk_info() -> str:
        """Kök (/) dizini için toplam ve boş disk alanını döner."""
        try:
            total, used, free = shutil.disk_usage("/")
            total_gb = round(total / (1024**3), 1)
            free_gb = round(free / (1024**3), 1)
            return f"{free_gb} GB boş / {total_gb} GB"
        except Exception:
            return "Disk Bilgisi Alınamadı"

    @classmethod
    def get_all_summary(cls) -> Dict[str, str]:
        """Tüm sistem özetini tek bir sözlükte toplar."""
        os_info = cls.get_os_info()
        return {
            "os_name": os_info["pretty_name"],
            "kernel": f"Linux {cls.get_kernel()}",
            "desktop": cls.get_desktop_environment(),
            "cpu": cls.get_cpu_info(),
            "ram": cls.get_ram_info(),
            "disk": cls.get_disk_info(),
            "arch": platform.machine()
        }
