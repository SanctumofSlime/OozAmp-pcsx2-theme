#!/bin/bash
# OozAmp Gel · Neon Vat for PCSX2 — installer (macOS)
# Copies the images into PCSX2's data folder, writes custom.qss with the full
# image paths Qt needs, and installs the three fonts for your user.
set -e
cd "$(dirname "$0")"

PCSX2_DIR="$HOME/Library/Application Support/PCSX2"
ASSETS="$PCSX2_DIR/oozamp"

if [ ! -d "$PCSX2_DIR" ]; then
  echo "Couldn't find $PCSX2_DIR"
  echo "Open PCSX2 once (so it creates its folder), then run this again."
  read -n 1 -s -r -p "Press any key to close."
  exit 1
fi

mkdir -p "$ASSETS"
cp oozamp/* "$ASSETS/"

if [ -f "$PCSX2_DIR/custom.qss" ] && ! grep -q "OozAmp" "$PCSX2_DIR/custom.qss"; then
  cp "$PCSX2_DIR/custom.qss" "$PCSX2_DIR/custom.qss.backup"
  echo "Backed up your existing custom.qss to custom.qss.backup"
fi
sed "s#@OOZ@#$ASSETS#g" custom.qss.in > "$PCSX2_DIR/custom.qss"

mkdir -p "$HOME/Library/Fonts"
cp fonts/*.ttf "$HOME/Library/Fonts/"

echo ""
echo "OozAmp installed."
echo "In PCSX2: Settings > Interface > Theme > \"custom.qss [Drop in PCSX2 Folder]\""
echo "(If PCSX2 was open, restart it so it picks up the new fonts.)"
read -n 1 -s -r -p "Press any key to close."
