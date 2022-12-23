#!/usr/local/bin/python

""" Python Helper for running docker """

import os

def main() -> int:
    """Start Docker"""
    os.system('docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t blog_to_podcast .')
    return 0

if __name__ == '__main__':
    main()
