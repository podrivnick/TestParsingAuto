FROM python:3.12.1-slim-bullseye as builder

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.8.2 && \
    poetry export -o requirements.prod.txt --without-hashes && \
    poetry export --with=dev -o requirements.dev.txt --without-hashes

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python:3.12.1-slim-bullseye as dev

WORKDIR /TestParsingAuto

COPY --from=builder requirements.dev.txt /TestParsingAuto


RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3-dev \
        gcc \
        musl-dev \
        libpq-dev \
        nmap \
        netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        wget \
        gnupg \
        unzip \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN set -ex; \
    apt-get update && apt-get install -y wget curl gnupg unzip fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils libu2f-udev libvulkan1; \
    wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_124.0.6367.91-1_amd64.deb; \
    apt install -y ./google-chrome-stable_124.0.6367.91-1_amd64.deb; \
    rm google-chrome-stable_124.0.6367.91-1_amd64.deb

RUN set -ex; \
    GOOGLE_CHROME_PATH=$(which google-chrome-stable || which google-chrome || true); \
    echo "Google Chrome знайдений шляхом: $GOOGLE_CHROME_PATH"; \
    if [ -z "$GOOGLE_CHROME_PATH" ]; then \
        echo "Помилка: google-chrome не знайдено"; \
        exit 1; \
    fi; \
    CHROME_MAJOR_VERSION=$($GOOGLE_CHROME_PATH --version | awk '{print $3}' | cut -d'.' -f1); \
    echo "Chrome major version: $CHROME_MAJOR_VERSION"; \
    DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE" || \
                    echo "Помилка: не вдалося отримати версію ChromeDriver"); \
    echo "Driver version: $DRIVER_VERSION"; \
    if [[ "$DRIVER_VERSION" == *"Ошибка:"* ]]; then \
        echo "Не вдалося знайти відповідну версію ChromeDriver. Програма завершена."; \
        exit 1; \
    fi; \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip"; \
    unzip /tmp/chromedriver.zip -d /usr/local/bin; \
    chmod +x /usr/local/bin/chromedriver; \
    rm /tmp/chromedriver.zip

RUN pip install --upgrade --no-cache-dir pip==24.0 && \
    pip install --no-cache-dir poetry==1.8.2 && \
    pip install --no-cache-dir -r requirements.dev.txt

COPY ./config /TestParsingAuto/config
COPY ./src /TestParsingAuto/src

EXPOSE 8000
