#!/usr/local/bin/python3

""" Python Helper for running docker """

import os

def main() -> int:
    """Start Docker"""
    os.system(
        'docker run -it -v "$(pwd):/home/testuser/workspace/InputProject" blog_to_podcast bash'
        )
    return 0

if __name__ == '__main__':
    main()
