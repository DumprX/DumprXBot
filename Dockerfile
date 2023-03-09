#
# Copyright (C) 2023 The DumprX Project
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# Base Image
FROM archlinux:latest

# Image Maintainer
LABEL maintainer="Sushrut1101 <guptasushrut@gmail.com>"

# Install dependencies
RUN pacman -Syyu --noconfirm
RUN pacman -S --noconfirm \
	git curl wget \
	python python-pip python-setuptools \
	neofetch tmate speedtest-cli

# Working Directory
RUN mkdir /app && chmod 777 /app
WORKDIR /app

# Expose a port
EXPOSE 5000

# Copy sources
COPY . /app/

# Install python dependencies
RUN pip install -U --no-cache-dir -r requirements.txt

# Set the deploy command
CMD ["python", "-m", "DumprXBot"]
