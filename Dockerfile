FROM python:3.8-slim-buster as base

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

USER root

# Library versions
ARG WKHTMLTOX_VERSION
ENV WKHTMLTOX_VERSION ${WKHTMLTOX_VERSION:-"0.12.5"}

ARG WKHTMLTOPDF_CHECKSUM
ENV WKHTMLTOPDF_CHECKSUM ${WKHTMLTOPDF_CHECKSUM:-"1140b0ab02aa6e17346af2f14ed0de807376de475ba90e1db3975f112fbd20bb"}

# Use noninteractive to get rid of apt-utils message
ENV DEBIAN_FRONTEND=noninteractive
# Install odoo deps

RUN apt-get update && apt-get install -y supervisor

RUN apt-get -qq update \
    && apt-get -qq install -y --no-install-recommends \
    curl \
    && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/${WKHTMLTOX_VERSION}/wkhtmltox_${WKHTMLTOX_VERSION}-1.stretch_amd64.deb \
    && echo "${WKHTMLTOPDF_CHECKSUM} wkhtmltox.deb" | sha256sum -c - \
    && apt-get install -y --no-install-recommends ./wkhtmltox.deb \
    && apt-get -qq install -y --no-install-recommends \
    ca-certificates \
    chromium \
    git-core \
    gnupg \
    htop \
    ffmpeg \
    fonts-liberation2 \
    fonts-noto-cjk \
    locales \
    lsb-release \
    node-less \
    npm \
    python3-num2words \
    python3-pip \
    python3-phonenumbers \
    python3-pyldap \
    python3-qrcode \
    python3-renderpm \
    python3-setuptools \
    python3-slugify \
    python3-vobject \
    python3-watchdog \
    python3-xlrd \
    python3-xlwt

RUN apt-get -qq update \
    && apt-get -qq install -y --no-install-recommends \
    apt-utils dialog \
    apt-transport-https \
    build-essential \
    libfreetype6-dev \
    libfribidi-dev \
    libghc-zlib-dev \
    libharfbuzz-dev \
    libjpeg-dev \
    libgeoip-dev \
    libmaxminddb-dev \
    liblcms2-dev \
    libldap2-dev \
    libopenjp2-7-dev \
    libssl-dev \
    libsasl2-dev \
    libtiff5-dev \
    libxml2-dev \
    libxslt1-dev \
    libpq-dev \
    libwebp-dev \
    lsb-release \
    tcl-dev \
    tk-dev \
    zlib1g-dev \
    && apt-get autopurge -yqq \
    && rm -Rf /var/lib/apt/lists/* /tmp/*

# Install rtlcss (on Debian buster)
RUN npm install -g rtlcss \
    && rm -Rf ~/.npm /tmp/*


COPY requirements.txt /
RUN pip3 --no-cache-dir install --upgrade pip setuptools
RUN pip3 --no-cache-dir install -r requirements.txt && mkdir -p /var/log/apps

COPY conf/supervisor/ /etc/supervisor.d/

COPY . /webapps/service

WORKDIR /webapps/service
