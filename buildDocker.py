#!/usr/local/bin/python3

import os

os.system('docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t blog_to_podcast .')