#!/usr/bin/env bash
# Pars Welcome - Sistemden Kaldırma Betiği

set -e

if [[ $EUID -ne 0 ]]; then
   echo "HATA: Bu betik root (sudo) yetkileri ile çalıştırılmalıdır!" >&2
   exit 1
fi

INSTALL_PREFIX="${PREFIX:-/usr}"
DATA_DIR="${INSTALL_PREFIX}/share/parslinux-welcome"
BIN_FILE="${INSTALL_PREFIX}/bin/pars-welcome"
DESKTOP_FILE="${INSTALL_PREFIX}/share/applications/org.parslinux.welcome.desktop"
ICON_FILE="${INSTALL_PREFIX}/share/icons/hicolor/scalable/apps/org.parslinux.welcome.svg"

echo "==> Pars Welcome sistemden kaldırılıyor..."

# Dosyaları temizle
rm -rf "${DATA_DIR}"
rm -f "${BIN_FILE}"
rm -f "${DESKTOP_FILE}"
rm -f "${ICON_FILE}"

# Önbellekleri güncelle
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database -q "${INSTALL_PREFIX}/share/applications" || true
fi

if command -v gtk-update-icon-cache &>/dev/null; then
    gtk-update-icon-cache -q -t -f "${INSTALL_PREFIX}/share/icons/hicolor" || true
fi

echo "==> Pars Welcome sistemden tamamen kaldırıldı!"
