#docker run -it -v ~/workspace:/workspace "${perm_conf[@]}" --runtime=nvidia tensorflow/tensorflow:latest-gpu bash

#docker run -it -v ~/workspace:/workspace "${perm_conf[@]}" --runtime=nvidia tensorflow/tensorflow:2.3.1-gpu bash


docker run -it -v ~/Sync/_workspace:/workspace "${perm_conf[@]}" blog_to_podcast bash
#if ! command -v nvidia-smi &> /dev/null
#then
#	docker run -it -v ~/Sync/_workspace:/workspace "${perm_conf[@]}" tensorflow/tensorflow:latest bash
#else
#	docker run -it -v ~/Sync/_workspace:/workspace "${perm_conf[@]}" --runtime=nvidia 9fb490a67746 bash
#fi

