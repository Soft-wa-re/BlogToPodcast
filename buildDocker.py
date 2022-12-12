#!/usr/local/bin/python3

<<<<<<< HEAD
import subprocess

subprocess.run("docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t blog_to_podcast .", shell=True, check=True)
=======
import os

os.system('docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t blog_to_podcast .')
>>>>>>> da0541c21b6b98423ac955e2da68022d93825967
