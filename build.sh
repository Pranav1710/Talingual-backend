#!/bin/bash
# apt-get update && apt-get install -y \
#   libglib2.0-0 \
#   libnss3 \
#   libgdk-pixbuf2.0-0 \
#   libx11-xcb1 \
#   libxcomposite1 \
#   libxdamage1 \
#   libxrandr2 \
#   libasound2 \
#   libatk1.0-0 \
#   libatk-bridge2.0-0 \
#   libcups2 \
#   libdbus-1-3 \
#   libdrm2 \
#   libxshmfence1 \
#   libxfixes3 \
#   libxext6 \
#   libxrender1 \
#   libx11-6 \
#   libxtst6 \
#   libsecret-1-0 \
#   libgbm1 \
#   libegl1 \
#   libgles2 \
#   libenchant-2-2 \
#   libgtk-4-1 \
#   libgraphene-1.0-0 \
#   libgstgl-1.0-0 \
#   libgstcodecparsers-1.0-0 \
#   libgstreamer-gl1.0-0 \
#   libgstreamer-plugins-base1.0-0 \
#   libgstreamer-plugins-bad1.0-0 \
#   libmanette-0.2-0 \
#   libpango-1.0-0 \
#   libcairo2 \
#   fonts-liberation \
#   xdg-utils \
#   ca-certificates \
#   wget \
#   curl

pip install -r requirements.txt

npx playwright install chromium
npx playwright install webkit
npx playwright install firefox


