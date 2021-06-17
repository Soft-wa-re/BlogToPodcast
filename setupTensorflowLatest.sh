apt update
apt install -y vim libsndfile1-dev zsh tmux wget git libsndfile1
apt install ffmpeg
/usr/bin/python3 -m pip install --upgrade pip

pip install soundfile
pip install numpy
pip install git+https://github.com/repodiac/german_transliterate.git#egg=german_transliterate
pip install git+https://github.com/TensorSpeech/TensorflowTTS.git
pip install pydub

