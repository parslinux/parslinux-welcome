#!/usr/bin/env bash
# Pars Welcome - Otomatik Paketleme Betiği

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PKG_NAME="parslinux-welcome"
VERSION="1.0.0"
DIST_DIR="$SCRIPT_DIR/dist"

echo "=========================================="
echo "  Pars Welcome Paketleyici - v${VERSION}"
echo "=========================================="

mkdir -p "$DIST_DIR"

# 1. Kaynak Tarball (.tar.gz) Oluşturma
TARBALL="${DIST_DIR}/${PKG_NAME}-${VERSION}.tar.gz"
echo "==> [1/3] Kaynak arşivi oluşturuluyor: ${TARBALL}..."
tar --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='dist' \
    --exclude='.vscode' \
    --exclude='.pytest_cache' \
    -czf "${TARBALL}" \
    --transform "s,^,${PKG_NAME}-${VERSION}/," \
    src data tests pars-welcome README.md LICENSE PKGBUILD run.sh install.sh uninstall.sh 2>/dev/null || \
tar --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='dist' \
    --exclude='.vscode' \
    --exclude='.pytest_cache' \
    -czf "${TARBALL}" \
    src data tests pars-welcome README.md PKGBUILD run.sh install.sh uninstall.sh

echo "    Kaynak arşivi hazır: ${TARBALL}"

# 2. Arch Linux / Pars Linux (makepkg) Paketi
if command -v makepkg &>/dev/null; then
    echo "==> [2/3] Arch / Pars Linux paketi (makepkg) derleniyor..."
    # Geçici dizinde derle
    BUILD_DIR="/tmp/build_${PKG_NAME}_$$"
    mkdir -p "${BUILD_DIR}"
    cp PKGBUILD "${BUILD_DIR}/"
    cp "${TARBALL}" "${BUILD_DIR}/${PKG_NAME}-${VERSION}.tar.gz"
    
    (
        cd "${BUILD_DIR}"
        makepkg -f --nodeps --skipinteg
        cp *.pkg.tar* "${DIST_DIR}/"
    )
    rm -rf "${BUILD_DIR}"
    echo "    Arch paketi hazır: $(ls ${DIST_DIR}/*.pkg.tar* 2>/dev/null || echo 'Oluşturulamadı')"
else
    echo "==> [2/3] makepkg bulunamadı, Arch paketleme adımı atlandı."
fi

# 3. Debian / Ubuntu (.deb) Paketi
if command -v dpkg-deb &>/dev/null; then
    echo "==> [3/3] Debian / Ubuntu paketi (.deb) oluşturuluyor..."
    DEB_ROOT="/tmp/deb_${PKG_NAME}_$$"
    mkdir -p "${DEB_ROOT}/DEBIAN"
    mkdir -p "${DEB_ROOT}/usr/share/${PKG_NAME}"
    mkdir -p "${DEB_ROOT}/usr/bin"
    mkdir -p "${DEB_ROOT}/usr/share/applications"
    mkdir -p "${DEB_ROOT}/usr/share/icons/hicolor/scalable/apps"

    # Control dosyası
    cat << EOF > "${DEB_ROOT}/DEBIAN/control"
Package: ${PKG_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-gi, gir1.2-gtk-4.0, gir1.2-adw-1
Maintainer: Pars Linux Team <info@parslinux.org>
Description: Pars Linux modern GTK4/Libadwaita karsilama merkezi
 Pars Linux kullanicilari icin baslangic ayarlari, sistem ozeti
 ve one cikan uygulamalari yoneten modern Libadwaita karsilama araci.
EOF

    # Dosyaları yerleştir
    cp -r src "${DEB_ROOT}/usr/share/${PKG_NAME}/"
    cp -r data "${DEB_ROOT}/usr/share/${PKG_NAME}/"

    cat << 'EOF' > "${DEB_ROOT}/usr/bin/pars-welcome"
#!/usr/bin/env bash
exec python3 /usr/share/parslinux-welcome/src/Main.py "$@"
EOF
    chmod 755 "${DEB_ROOT}/usr/bin/pars-welcome"

    cp data/org.parslinux.welcome.desktop "${DEB_ROOT}/usr/share/applications/"
    chmod 644 "${DEB_ROOT}/usr/share/applications/org.parslinux.welcome.desktop"

    if [[ -f data/org.parslinux.welcome.svg ]]; then
        cp data/org.parslinux.welcome.svg "${DEB_ROOT}/usr/share/icons/hicolor/scalable/apps/"
        chmod 644 "${DEB_ROOT}/usr/share/icons/hicolor/scalable/apps/org.parslinux.welcome.svg"
    fi

    DEB_FILE="${DIST_DIR}/${PKG_NAME}_${VERSION}_all.deb"
    dpkg-deb --build "${DEB_ROOT}" "${DEB_FILE}" >/dev/null
    rm -rf "${DEB_ROOT}"
    echo "    Debian paketi hazır: ${DEB_FILE}"
else
    echo "==> [3/3] dpkg-deb bulunamadı, Debian paketleme adımı atlandı."
fi

echo ""
echo "=========================================="
echo "  Paketleme Tamamlandı! Çıktılar (dist/):"
ls -lh "$DIST_DIR"
echo "=========================================="
