#!/bin/bash

# Create temporary iconset directory
mkdir icon.iconset

# Convert SVG to PNG files of different sizes
for size in 16 32 64 128 256 512; do
  sips -s format png icon.svg --out icon.iconset/icon_${size}x${size}.png --resampleHeightWidth $size $size
  if [ $size -le 256 ]; then
    sips -s format png icon.svg --out icon.iconset/icon_${size}x${size}@2x.png --resampleHeightWidth $((size*2)) $((size*2))
  fi
done

# Create ICNS file
iconutil -c icns icon.iconset

# Clean up
rm -rf icon.iconset 