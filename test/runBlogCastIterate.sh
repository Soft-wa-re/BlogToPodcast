#!/bin/sh

docker run --rm -it  -v "$(pwd):/home/testuser/workspace/InputProject" \
                     -v "$(pwd)/..:/home/testuser/workspace/BlogCast" blog_to_podcast ../BlogCast/main.py
