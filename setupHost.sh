curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
apt-get update
apt-get install -y nvidia-docker2
pkill -SIGHUP dockerd
nvidia-container-cli --load-kmods info
pip install python-frontmatter
pip install frontmatter
pip install --upgrade tensorflow==2.10.0
python /home/testuser/workspace/BlogCast/setup.py install
#docker run -it -v ~/workspace:/workspace "${perm_conf[@]}" --runtime=nvidia tensorflow/tensorflow:latest-gpu bash

