#!/bin/bash

# Exit script if any command fails
set -e

# Install required system packages
apt-get update && apt-get install -y \
  libglib2.0-0 \
  libnss3 \
  libgdk-pixbuf2.0-0 \
  libx11-xcb1 \
  libxcomposite1 \
  libxdamage1 \
  libxrandr2 \
  libasound2 \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libcups2 \
  libdbus-1-3 \
  libdrm2 \
  libxshmfence1 \
  libxfixes3 \
  libxext6 \
  libxrender1 \
  libx11-6 \
  libxtst6 \
  libsecret-1-0 \
  libgbm1 \
  libegl1 \
  libgles2 \
  libenchant-2-2 \
  wget \
  curl \
  ca-certificates \
  fonts-liberation \
  xdg-utils

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browser dependencies
npx playwright install
