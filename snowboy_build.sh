git clone https://github.com/Kitt-AI/snowboy.git
cd snowboy

sudo apt-get install -y python-pyaudio python3-pyaudio sox
sudo pip install pyaudio
sudo apt-get install -y libatlas-base-dev swig portaudio19-dev flac

cd swig/Python
make
