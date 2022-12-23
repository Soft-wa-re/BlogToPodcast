#!/usr/local/bin/python3

""" Python Helper for running docker """

import os

DOCKER_CMD = """
    docker run --rm -it 
        -v "$(pwd):/home/testuser/workspace/InputProject" blog_to_podcast ../BlogCast/main.py
"""

def main() -> int:
    """Start Docker"""
    os.system(DOCKER_CMD)
    return 0

if __name__ == '__main__':
    main()
