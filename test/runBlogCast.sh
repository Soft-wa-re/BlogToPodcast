#!/bin/sh

docker run --rm -it -v "$(pwd):/home/testuser/workspace/InputProject" blog_to_podcast ../BlogCast/main.py