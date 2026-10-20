#!/usr/bin/env bash
# Pars Welcome - i18n Çoklu Dil Çeviri Güncelleme ve Derleme Betiği

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Dil şablonu (POT) üretiliyor..."
xgettext --from-code=UTF-8 --language=Python --keyword=_ \
    --output=po/parslinux-welcome.pot \
    src/Main.py \
    src/ui/MainWindowAdw.py \
    src/ui/pages/PageWelcome.py \
    src/ui/pages/PageFirstSteps.py \
    src/ui/pages/PageApps.py \
    src/ui/pages/PageCommunity.py \
    src/ui/widgets/WallpaperDialog.py

echo "==> İkili çeviri dosyaları (MO) derleniyor..."
mkdir -p data/locale/tr/LC_MESSAGES data/locale/en/LC_MESSAGES
msgfmt po/tr.po -o data/locale/tr/LC_MESSAGES/parslinux-welcome.mo
msgfmt po/en.po -o data/locale/en/LC_MESSAGES/parslinux-welcome.mo

echo "==> Çeviriler başarıyla güncellendi ve derlendi!"
