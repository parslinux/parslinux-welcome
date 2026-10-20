# Maintainer: Pars Linux Team <info@parslinux.org>
pkgname=parslinux-welcome
pkgver=1.0.0
pkgrel=1
pkgdesc="Pars Linux modern GTK4/Libadwaita karşılama ve başlangıç merkezi"
arch=('any')
url="https://github.com/parslinux/parslinux-welcome"
license=('GPL3')
depends=('python' 'python-gobject' 'gtk4' 'libadwaita')
optdepends=(
    'pars-update: Sistem güncelleme yöneticisi entegrasyonu'
    'timeshift: Sistem anlık görüntü ve yedekleme desteği'
    'flatpak: Ek uygulama mağaza desteği'
)
source=("$pkgname-$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir"
    if [ -d "$pkgname-$pkgver" ]; then
        cd "$pkgname-$pkgver"
    fi
    
    # Hedef dizinler
    install -d "$pkgdir/usr/share/$pkgname"
    install -d "$pkgdir/usr/bin"
    install -d "$pkgdir/usr/share/applications"
    install -d "$pkgdir/usr/share/icons/hicolor/scalable/apps"

    # Kaynak dosyaları kopyala
    cp -r src "$pkgdir/usr/share/$pkgname/"
    cp -r data "$pkgdir/usr/share/$pkgname/"

    # Çalıştırılabilir ikiliyi oluştur
    cat << 'EOF' > "$pkgdir/usr/bin/pars-welcome"
#!/usr/bin/env bash
exec python3 /usr/share/parslinux-welcome/src/Main.py "$@"
EOF
    chmod 755 "$pkgdir/usr/bin/pars-welcome"

    # Desktop ve ikon kurulumu
    install -Dm644 data/org.parslinux.welcome.desktop "$pkgdir/usr/share/applications/"
    if [ -f data/org.parslinux.welcome.svg ]; then
        install -Dm644 data/org.parslinux.welcome.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/"
    fi
    if [ -d data/icons/hicolor ]; then
        cp -r data/icons/hicolor/* "$pkgdir/usr/share/icons/hicolor/"
    fi
    if [ -d data/locale ]; then
        mkdir -p "$pkgdir/usr/share/locale"
        cp -r data/locale/* "$pkgdir/usr/share/locale/"
    fi
}
