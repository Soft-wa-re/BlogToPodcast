docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) \
 -t tmbecken/blog_to_podcast .

docker login -u tmbecken -p "6o*1FAxGN"

docker push tmbecken/blog_to_podcast