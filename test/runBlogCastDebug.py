import os

os.system('docker run --rm -it  -v "$(pwd):/home/testuser/workspace/InputProject" -v "$(pwd)/../Blog_BlogToPodcast:/home/testuser/workspace/BlogCast" blog_to_podcast bash')
