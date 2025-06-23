FROM python:3.10-slim

ENV ENVIRONMENT=prod

RUN apt-get update && apt-get install -y \
    curl wget gnupg unzip \
    libgtk-3-0 libxss1 libasound2 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxtst6 libgbm1 libxrandr2 libu2f-udev libvulkan1 \
    fonts-liberation libappindicator3-1 libsecret-1-0 libgdk-pixbuf2.0-0 \
    libenchant-2-2 libgles2 libglib2.0-0 \
    && apt-get clean

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install playwright
RUN playwright install

EXPOSE 10000
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "--workers", "1", "app:app"]

