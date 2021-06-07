apt update
apt install -y python3.8 python-pip-whl python3-pip vim libsndfile1-dev git

pip install TensorFlowTTS
mkdir workspace
cd workspace/
pip install soundfile
pip install numpy
pip install tensorflow
pip install git+https://github.com/repodiac/german_transliterate.git#egg=german_transliterate
python3 example.py 

