FROM tensorflow/tensorflow:latest
RUN apt update && apt install -y vim libsndfile1-dev zsh tmux wget git libsndfile1 ffmpeg python3-venv sudo
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN pip install git+https://github.com/repodiac/german_transliterate.git#egg=german_transliterate
RUN pip install soundfile numpy pydub TensorflowTTS
RUN mkdir -m 777 /usr/nltk_data
RUN mkdir -m 777 /nltk_data                                 && \ 
    mkdir -m 777 /tmp/NUMBA_CACHE_DIR                       && \ 
    useradd -ms /bin/bash t                                 && \
    sudo python -m nltk.downloader -d /usr/local/share/nltk_data all
ENV NUMBA_CACHE_DIR=/tmp/NUMBA_CACHE_DIR/
#https://stackoverflow.com/a/44683248/298240
ARG UNAME=testuser
ARG UID=1000
ARG GID=1000
USER $UNAME
ADD . /home/$UNAME/workspace/BlogCast
USER root
RUN /home/testuser/workspace/BlogCast/setupHost.sh            && \
    groupadd -g $GID -o testuser                              && \
    useradd -m -u $UID -g $GID -o -s /bin/bash testuser       && \
    echo "testuser:testuser" | chpasswd                       && \
    adduser testuser sudo                                     && \
    sudo chown testuser /home/testuser                        && \
    sudo chown testuser /home/testuser/workspace              && \
    sudo chown testuser /home/testuser/workspace/BlogCast     
USER $UNAME
RUN cd /home/testuser/workspace/BlogCast/test                 && \
    python ../main.py
WORKDIR /home/$UNAME/workspace/InputProject
