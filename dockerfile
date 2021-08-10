FROM tensorflow/tensorflow:latest
RUN apt update && apt install -y vim libsndfile1-dev zsh tmux wget git libsndfile1 ffmpeg python3-venv sudo
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN pip install git+https://github.com/repodiac/german_transliterate.git#egg=german_transliterate
RUN pip install soundfile numpy pydub TensorflowTTS
RUN mkdir -m 777 /nltk_data
RUN mkdir -m 777 /tmp/NUMBA_CACHE_DIR
ENV NUMBA_CACHE_DIR=/tmp/NUMBA_CACHE_DIR/
RUN useradd -ms /bin/bash t
#https://stackoverflow.com/a/44683248/298240
ARG UNAME=testuser
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME && useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME && echo "testuser:testuser" | chpasswd && adduser testuser sudo
USER $UNAME
WORKDIR /home/$UNAME


#docker run -it -v ~/workspace:/workspace "${perm_conf[@]}" --runtime=nvidia tensorflow/tensorflow:latest-gpu bash
#docker run -it -v ~/workspace:/workspace "${perm_conf[@]}" --runtime=nvidia tensorflow/tensorflow:2.3.1-gpu bash
#if ! command -v nvidia-smi &> /dev/null
#then
#	docker run -it -v ~/Sync/_workspace:/workspace "${perm_conf[@]}" tensorflow/tensorflow:latest bash
#else
#	docker run -it -v ~/Sync/_workspace:/workspace "${perm_conf[@]}" --runtime=nvidia 9fb490a67746 bash
#fi
# apt update
# apt install -y vim libsndfile1-dev zsh tmux wget git libsndfile1 ffmpeg
# /usr/bin/python3 -m pip install --upgrade pip
# pip install soundfile numpy pydub
# pip install git+https://github.com/repodiac/german_transliterate.git#egg=german_transliterate
# pip install TensorflowTTS
#pip install git+https://github.com/TensorSpeech/TensorflowTTS.git
