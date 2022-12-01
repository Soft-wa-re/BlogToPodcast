cd $( dirname -- "$0" )

echo $(pwd)

docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t blog_to_podcast .

cd -