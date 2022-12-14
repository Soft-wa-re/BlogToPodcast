cd $( dirname -- "$0" )

echo $(pwd)

docker scan blog_to_podcast --group-issues --json --severity high

cd -