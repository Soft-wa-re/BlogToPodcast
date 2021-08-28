FROM tensorflow/tensorflow:latest
RUN apt update && apt install -y vim libsndfile1-dev zsh tmux wget git libsndfile1 ffmpeg python3-venv sudo
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN pip install git+https://github.com/repodiac/german_transliterate.git#egg=german_transliterate
RUN pip install soundfile numpy pydub TensorflowTTS
RUN mkdir -m 777 /usr/nltk_data
RUN mkdir -m 777 /nltk_data                                 && \ 
RUN mkdir -m 777 /tmp/NUMBA_CACHE_DIR                       && \ # for numba
    useradd -ms /bin/bash t
ENV NUMBA_CACHE_DIR=/tmp/NUMBA_CACHE_DIR/
#https://stackoverflow.com/a/44683248/298240
ARG UNAME=testuser
ARG UID=1000
ARG GID=1000
USER $UNAME
ADD . /home/$UNAME/workspace/BlogCast
USER root
RUN /home/$UNAME/workspace/BlogCast/setupHost.sh            && \
    groupadd -g $GID -o $UNAME                              && \
    useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME       && \
    echo "testuser:testuser" | chpasswd                     && \
    adduser testuser sudo                                   && \
    sudo chown testuser /home/$UNAME                        && \
    sudo chown testuser /home/$UNAME/workspace              && \
    sudo chown testuser /home/$UNAME/workspace/BlogCast
USER $UNAME
WORKDIR /home/$UNAME/workspace/InputProject
