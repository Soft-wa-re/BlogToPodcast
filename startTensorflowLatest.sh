

docker run -it -v ~/workspace:/workspace "${perm_conf[@]}" --runtime=nvidia tensorflow/tensorflow:latest-gpu bash
#docker run -it -v ~/workspace:/workspace "${perm_conf[@]}" tensorflow/tensorflow bash

#--runtime=nvidia tensorflow/tensorflow:2.3.1-gpu bash