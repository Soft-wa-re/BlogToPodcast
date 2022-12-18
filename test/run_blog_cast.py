#!/usr/local/bin/python3

""" Python Helper for running docker """

import os

DOCKER_CMD = """
    docker run --rm -it 
        -v "$(pwd):/home/testuser/workspace/InputProject" blog_to_podcast ../BlogCast/main.py
"""

os.system(DOCKER_CMD)
