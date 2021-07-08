FROM tensorflow/tensorflow:latest
RUN apt update && apt install -y vim libsndfile1-dev zsh tmux wget git libsndfile1 ffmpeg
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN pip install git+https://github.com/repodiac/german_transliterate.git#egg=german_transliterate
RUN pip install soundfile numpy pydub TensorflowTTS