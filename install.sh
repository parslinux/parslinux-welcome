#!/usr/bin/env bash
# Pars Welcome - Sisteme Kurulum Betiği

set -e

if [[ $EUID -ne 0 ]]; then
   echo "HATA: Bu betik root (sudo) yetkileri ile çalıştırılmalıdır!" >&2
   exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PREFIX="${PREFIX:-/usr}"
DATA_DIR="${INSTALL_PREFIX}/share/parslinux-welcome"
BIN_DIR="${INSTALL_PREFIX}/bin"
DESKTOP_DIR="${INSTALL_PREFIX}/share/applications"
ICON_DIR="${INSTALL_PREFIX}/share/icons/hicolor/scalable/apps"

echo "==> Pars Welcome sisteme kuruluyor..."
echo "    Hedef dizin: ${DATA_DIR}"

# 1. Dizinleri oluştur
mkdir -p "${DATA_DIR}"
mkdir -p "${BIN_DIR}"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${ICON_DIR}"

# 2. Kaynak kodları ve verileri kopyala
echo "--> Dosyalar kopyalanıyor..."
cp -r "${SCRIPT_DIR}/src" "${DATA_DIR}/"
cp -r "${SCRIPT_DIR}/data" "${DATA_DIR}/"

# 3. Başlatıcı ikiliyi (binary) oluştur
echo "--> /usr/bin/pars-welcome oluşturuluyor..."
cat << 'EOF' > "${BIN_DIR}/pars-welcome"
#!/usr/bin/env bash
exec python3 /usr/share/parslinux-welcome/src/Main.py "$@"
EOF
chmod +x "${BIN_DIR}/pars-welcome"

# 4. Masaüstü dosyasını ve ikonu yükle
echo "--> Masaüstü entegrasyonu yapılıyor..."
cp "${SCRIPT_DIR}/data/org.parslinux.welcome.desktop" "${DESKTOP_DIR}/"
chmod 644 "${DESKTOP_DIR}/org.parslinux.welcome.desktop"

if [[ -f "${SCRIPT_DIR}/data/org.parslinux.welcome.svg" ]]; then
    cp "${SCRIPT_DIR}/data/org.parslinux.welcome.svg" "${ICON_DIR}/"
    chmod 644 "${ICON_DIR}/org.parslinux.welcome.svg"
fi

# 5. Önbellekleri güncelle
echo "--> Sistem veritabanları güncelleniyor..."
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database -q "${DESKTOP_DIR}" || true
fi

if command -v gtk-update-icon-cache &>/dev/null; then
    gtk-update-icon-cache -q -t -f "${INSTALL_PREFIX}/share/icons/hicolor" || true
fi

echo "==> Kurulum başarıyla tamamlandı!"
echo "    Artık terminalden 'pars-welcome' yazarak veya uygulama menüsünden başlatabilirsiniz."
