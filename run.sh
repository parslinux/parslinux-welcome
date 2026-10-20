#!/usr/bin/env bash
# Pars Welcome - Yerel Çalıştırma Betiği

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Pars Welcome başlatılıyor..."

# Python kontrolü
if ! command -v python3 &>/dev/null; then
    echo "HATA: python3 sistemde bulunamadı!" >&2
    exit 1
fi

# GTK4 ve Libadwaita kontrolü
python3 -c "
import sys
try:
    import gi
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw
except Exception as e:
    print('HATA: GTK4 veya Libadwaita bulunamadı: ' + str(e), file=sys.stderr)
    print('Lütfen bağımlılıkları yükleyin: python-gobject, gtk4, libadwaita', file=sys.stderr)
    sys.exit(1)
" || exit 1

# Uygulamayı başlat
exec python3 "$SCRIPT_DIR/pars-welcome" "$@"
