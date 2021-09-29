podman build --build-arg UID=$(id -u) --build-arg GID=$(id -g) \
 -t tmbecken/blog_to_podcast .

podman login -u tmbecken -p "6o*1FAxGN"

podman push tmbecken/blog_to_podcast