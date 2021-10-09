podman build --build-arg UID=$(id -u) --build-arg GID=$(id -g) \
 -t tmbecken/blog_to_podcast .
DOCKER_PASSWORD_VAR=$(echo $DOCKER_PASSWORD | base64 -d)
podman login -u tmbecken -p $DOCKER_PASSWORD_VAR

podman push tmbecken/blog_to_podcast