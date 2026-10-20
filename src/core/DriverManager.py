#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import shutil
from src.core.I18n import _

class DriverManager:
    """Ekran kartı (GPU) ve Wi-Fi sürücüsü tespit ve yönetim motoru."""

    @staticmethod
    def _is_arch():
        """Sistemin Arch Linux tabanlı olup olmadığını denetler."""
        return shutil.which("pacman") is not None

    @staticmethod
    def _run_cmd(cmd_list):
        """Güvenli bir şekilde alt süreç çalıştırıp çıktıyı döndürür."""
        try:
            return subprocess.check_output(cmd_list, stderr=subprocess.DEVNULL, universal_newlines=True).strip()
        except Exception:
            return ""

    @classmethod
    def get_pci_devices(cls):
        """Sistemdeki tüm PCI aygıtlarını bloklar halinde ayrıştırır."""
        devices = []
        try:
            out = cls._run_cmd(["lspci", "-nnk"])
            if not out:
                return devices
            curr = []
            for line in out.splitlines():
                if re.match(r"^[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.", line):
                    if curr:
                        devices.append(curr)
                    curr = [line]
                else:
                    if curr:
                        curr.append(line)
            if curr:
                devices.append(curr)
        except Exception:
            pass
        return devices

    @classmethod
    def get_gpus(cls):
        """Sistemdeki ekran kartlarını (GPU) ve aktif sürücülerini tespit eder."""
        gpus = []
        devices = cls.get_pci_devices()
        is_arch = cls._is_arch()

        for dev in devices:
            first_line = dev[0]
            if not re.search(r"vga compatible|3d controller|display controller", first_line, re.IGNORECASE):
                continue

            driver = None
            modules = []
            subsystem = ""

            for l in dev[1:]:
                clean_l = l.strip()
                if clean_l.lower().startswith("kernel driver in use:"):
                    driver = clean_l.split(":", 1)[-1].strip()
                elif clean_l.lower().startswith("kernel modules:"):
                    modules = [m.strip() for m in clean_l.split(":", 1)[-1].split(",") if m.strip()]
                elif clean_l.lower().startswith("subsystem:"):
                    subsystem = clean_l.split(":", 1)[-1].strip()

            # Model adını temizleme
            # Örnek: 00:02.0 VGA compatible controller [0300]: Intel Corporation Alder Lake-P GT1 [UHD Graphics] [8086:46a3] (rev 0c)
            parts = first_line.split(":", 2)
            raw_model = parts[-1].strip() if len(parts) >= 3 else first_line
            # Köşeli parantez içindeki PCI ID'leri ve rev bilgisi haricinde sade model adı
            model_clean = re.sub(r"\[[0-9a-fA-F]{4}:[0-9a-fA-F]{4}\]", "", raw_model)
            model_clean = re.sub(r"\(rev\s+[0-9a-fA-F]+\)", "", model_clean).strip()

            # Üretici tespiti
            vendor = "Other"
            icon = "video-display-symbolic"
            if re.search(r"nvidia", raw_model, re.IGNORECASE):
                vendor = "NVIDIA"
            elif re.search(r"intel", raw_model, re.IGNORECASE):
                vendor = "Intel"
            elif re.search(r"amd|radeon|\bati\b", raw_model, re.IGNORECASE):
                vendor = "AMD"
            elif re.search(r"vmware|virtualbox|qemu", raw_model, re.IGNORECASE):
                vendor = "Virtual"

            # Durum ve önerilen sürücü paketi
            can_install_proprietary = False
            recommended_pkg = None
            status_text = ""
            badge_type = "installed"

            if vendor == "NVIDIA":
                if driver == "nvidia":
                    ver = cls._get_nvidia_version()
                    status_text = _("Özel NVIDIA Sürücüsü Aktif") + (f" ({ver})" if ver else "")
                    badge_type = "installed"
                elif driver == "nouveau":
                    status_text = _("Açık Kaynak (Nouveau)")
                    badge_type = "available"
                    can_install_proprietary = True
                    recommended_pkg = "nvidia nvidia-utils" if is_arch else "nvidia-driver"
                else:
                    status_text = _("Sürücü Yüklenmedi / Eksik")
                    badge_type = "available"
                    can_install_proprietary = True
                    recommended_pkg = "nvidia nvidia-utils" if is_arch else "nvidia-driver"
            elif vendor == "AMD":
                drv_name = driver or "amdgpu"
                status_text = _("Açık Kaynak Mesa / {drv} (Entegre)").format(drv=drv_name)
                badge_type = "installed"
            elif vendor == "Intel":
                drv_name = driver or "i915"
                status_text = _("Açık Kaynak Intel Mesa / {drv} (Entegre)").format(drv=drv_name)
                badge_type = "installed"
            elif vendor == "Virtual":
                status_text = _("Sanal Makine Ekran Sürücüsü ({drv})").format(drv=driver or "vboxvideo")
                badge_type = "installed"
            else:
                status_text = _("Aktif Sürücü: {drv}").format(drv=driver or _("Bilinmiyor"))
                badge_type = "installed" if driver else "available"

            gpus.append({
                "model": model_clean or raw_model,
                "subsystem": subsystem,
                "vendor": vendor,
                "driver": driver or _("Yok"),
                "modules": modules,
                "status": status_text,
                "badge_type": badge_type,
                "can_install_proprietary": can_install_proprietary,
                "recommended_pkg": recommended_pkg,
                "icon": icon
            })

        return gpus

    @classmethod
    def _get_nvidia_version(cls):
        """Yüklü NVIDIA özel sürücüsünün sürümünü okur."""
        version_file = "/proc/driver/nvidia/version"
        if os.path.exists(version_file):
            try:
                with open(version_file, "r") as f:
                    content = f.read()
                    match = re.search(r"NVRM version:\s+NVIDIA.*?([\d\.]+)", content)
                    if match:
                        return match.group(1)
            except Exception:
                pass
        # Fallback to nvidia-smi
        out = cls._run_cmd(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"])
        if out:
            return out.splitlines()[0].strip()
        return ""

    @classmethod
    def get_wifis(cls):
        """Sistemdeki kablosuz ağ bağdaştırıcılarını (Wi-Fi) ve durumlarını tespit eder."""
        wifis = []
        devices = cls.get_pci_devices()
        is_arch = cls._is_arch()

        # 1. PCI Wi-Fi Aygıtları
        pci_wifis = []
        for dev in devices:
            first_line = dev[0]
            if re.search(r"network controller|wireless", first_line, re.IGNORECASE) and not re.search(r"ethernet", first_line, re.IGNORECASE):
                subsystem = ""
                driver = None
                modules = []
                for l in dev[1:]:
                    clean_l = l.strip()
                    if clean_l.lower().startswith("subsystem:"):
                        subsystem = clean_l.split(":", 1)[-1].strip()
                    elif clean_l.lower().startswith("kernel driver in use:"):
                        driver = clean_l.split(":", 1)[-1].strip()
                    elif clean_l.lower().startswith("kernel modules:"):
                        modules = [m.strip() for m in clean_l.split(":", 1)[-1].split(",") if m.strip()]

                parts = first_line.split(":", 2)
                raw_model = parts[-1].strip() if len(parts) >= 3 else first_line
                chosen_name = subsystem or raw_model
                model_clean = re.sub(r"\[[0-9a-fA-F]{4}:[0-9a-fA-F]{4}\]", "", chosen_name)
                model_clean = re.sub(r"\(rev\s+[0-9a-fA-F]+\)", "", model_clean).strip()

                pci_wifis.append({
                    "model": model_clean or raw_model,
                    "driver": driver,
                    "modules": modules
                })

        # 2. Ağ Arayüzleri (/sys/class/net)
        wireless_ifaces = []
        net_dir = "/sys/class/net"
        if os.path.exists(net_dir):
            for iface in os.listdir(net_dir):
                iface_path = os.path.join(net_dir, iface)
                is_wireless = os.path.exists(os.path.join(iface_path, "wireless")) or os.path.exists(os.path.join(iface_path, "phy80211"))
                if is_wireless:
                    operstate = "unknown"
                    state_file = os.path.join(iface_path, "operstate")
                    if os.path.exists(state_file):
                        try:
                            with open(state_file, "r") as f:
                                operstate = f.read().strip()
                        except Exception:
                            pass
                    wireless_ifaces.append({
                        "interface": iface,
                        "operstate": operstate
                    })

        # Birleştirme ve Durum Raporu
        if pci_wifis:
            for idx, pci in enumerate(pci_wifis):
                iface_info = wireless_ifaces[idx] if idx < len(wireless_ifaces) else None
                driver = pci["driver"]
                is_connected = iface_info and iface_info["operstate"] == "up"

                needs_driver = False
                recommended_pkg = None
                if not driver:
                    needs_driver = True
                    # Broadcom tespiti
                    if re.search(r"broadcom|bcm43", pci["model"], re.IGNORECASE):
                        recommended_pkg = "broadcom-wl" if is_arch else "broadcom-wl-dkms"
                    status_text = _("Sürücü Yüklenmedi / Eksik")
                    badge_type = "available"
                else:
                    if is_connected:
                        status_text = _("Bağlı ve Aktif ({drv})").format(drv=driver)
                    else:
                        status_text = _("Sürücü Aktif ({drv})").format(drv=driver)
                    badge_type = "installed"

                wifis.append({
                    "model": pci["model"],
                    "interface": iface_info["interface"] if iface_info else "wlan",
                    "driver": driver or _("Yok"),
                    "connected": is_connected,
                    "status": status_text,
                    "badge_type": badge_type,
                    "needs_driver": needs_driver,
                    "recommended_pkg": recommended_pkg,
                    "icon": "network-wireless-signal-excellent-symbolic" if is_connected else "network-wireless-symbolic"
                })
        elif wireless_ifaces:
            # USB Wi-Fi veya PCI listesinde çıkmayan adaptör
            for iface in wireless_ifaces:
                is_connected = iface["operstate"] == "up"
                wifis.append({
                    "model": _("Kablosuz Ağ Arayüzü ({iface})").format(iface=iface["interface"]),
                    "interface": iface["interface"],
                    "driver": _("Etkin"),
                    "connected": is_connected,
                    "status": _("Bağlı ve Aktif") if is_connected else _("Arayüz Hazır"),
                    "badge_type": "installed",
                    "needs_driver": False,
                    "recommended_pkg": None,
                    "icon": "network-wireless-signal-excellent-symbolic" if is_connected else "network-wireless-symbolic"
                })

        return wifis
