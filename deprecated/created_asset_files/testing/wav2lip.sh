
git clone https://github.com/Rudrabha/Wav2Lip.git

pip3 uninstall tensorflow tensorflow-gpu
pip3 install -r Wav2Lip/requirements.txt


wget "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth" -O "Wav2Lip/face_detection/detection/sfd/s3fd.pth"

wget "https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA?e=n9ljGW" -O "wav2lip_gan.pth"

python3 Wav2Lip/inference.py --checkpoint_path wav2lip_gan.pth --face "test.mp4" --audio "test.wav"
