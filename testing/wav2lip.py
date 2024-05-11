#@title Dub it!
#@markdown 1. Choose audio (you can also enter a YouTube or similar URL, or a manually uploaded file name):
audio = 'Dangerous time' #@param ['Dangerous time', 'Go home', 'Sound of victory', 'Ernie and Bert (2 speakers)', '11,780 votes (3 speakers)', 'מלפפונים חמוצים', 'שונאת שמאלנים', 'אני שולה', 'אריק ובנץ (2 דוברים)', 'אריק ובנץ וגנץ (3 דוברים)', 'Grab from uploaded video'] {allow-input: true}
#@markdown 2. Optionally untick "smooth_face_detection" to disable temporal smoothing of face coordinates:
smooth_face_detection = True #@param {type: "boolean"}
#@markdown 3. Optionally tick "override_face_detection" to manually asign face coordinates:
override_face_detection = False #@param {type: "boolean"}
left = 0# @param {type: "integer"}
top = 0# @param {type: "integer"}
width = 1080 #@param {type: "integer"}
height = 1920 #@param {type: "integer"}
#@markdown 4. Optionally tick "switch_speakers" to switch between visual media files with the change of speakers:
switch_speakers = False #@param {type: "boolean"}
#@markdown 5. Choose model for speaker diarization:
model = 'pyannote-audio DIHARD' #@param ['pyAudioAnalysis', 'pyannote-audio DIHARD','pyannote-audio AMI']
#@markdown 6. Optionally tick "reuse_files" to reuse previously uploaded files:
reuse_files = False #@param {type: "boolean"}
#@markdoצwn 7. Press the play (triangle) button on the left.
#@markdown 8. Press "Browse" or "Choose files" below, and upload image(s) or video(s) (if not reusing files).
#@markdown 9. If the resulting videos are too large, the Colab might disconnect, but you may still manually download the .mp4 from the folder on the left (click "Refresh" if missing).

from google.colab import files
try:
  inputs
except NameError:
  reuse_files = False

if not reuse_files:
  %cd /content/sample_data
  !rm -rf *
  inputs = files.upload()

if inputs:
  %cd /content
  !git clone --depth 1 https://github.com/eyaler/Wav2Lip
  import os
  !pip install librosa==0.9.2
  !pip install -U gdown
  if not os.path.exists('/content/Wav2Lip/checkpoints/wav2lip_gan.pth'):
    !gdown https://drive.google.com/uc?id=1dwHujX7RVNCvdR1RR93z0FS2T2yzqup9 -O /content/Wav2Lip/checkpoints/wav2lip_gan.pth
  !wget --no-check-certificate -nc https://eyalgruss.com/fomm/wav2lip_gan.pth -O /content/Wav2Lip/checkpoints/wav2lip_gan.pth
  #!wget --no-check-certificate -nc https://eyalgruss.com/fomm/wav2lip.pth -O /content/Wav2Lip/checkpoints/wav2lip.pth
  !wget --no-check-certificate -nc https://eyalgruss.com/fomm/s3fd-619a316812.pth -O /content/Wav2Lip/face_detection/detection/sfd/s3fd.pth
  !pip install -U git+https://github.com/ytdl-org/youtube-dl
  grab = False
  manual = False
  if '://' in audio:
    if os.path.exists('/content/custom.mp3'):
      os.remove('/content/custom.mp3')
    !youtube-dl --no-playlist --extract-audio --audio-format mp3 "$audio" -o "/content/custom.%(ext)s"
    audio = 'custom'
  elif audio=='Dangerous time':
    audio = 'dangerous'
    if not os.path.exists('/content/dangerous.mp3'):
      !youtube-dl --no-playlist --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=cQ54GDm1eL0 -o "/content/dangerous.%(ext)s"
  elif audio=='Go home':
    audio = 'gohome'
    !wget --no-check-certificate -nc https://eyalgruss.com/fomm/gohome.mp3
  elif audio=='Sound of victory':
    audio = 'victory'
    if not os.path.exists('/content/victory.mp3'):
      !youtube-dl --no-playlist --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=Nu96Fhl1Gjo -o "/content/victory.%(ext)s"
  elif audio=='Ernie and Bert (2 speakers)':
    audio = 'dialog_eng'
    if not os.path.exists('/content/dialog_eng.mp3'):
      !youtube-dl --no-playlist --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=I78YAciQpr0 -o "/content/dialog_eng.%(ext)s"
  elif audio == '11,780 votes (3 speakers)':
    audio = 'trialog_eng'
    if not os.path.exists('/content/trialog_eng.mp3'):
      !youtube-dl --no-playlist --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=o3hrN0cP58Y -o "/content/trialog_heb.%(ext)s"
  elif audio == 'מלפפונים חמוצים':
    audio = 'melaflefon'
    !wget --no-check-certificate -nc https://eyalgruss.com/fomm/melaflefon.mp3
  elif audio == 'שונאת שמאלנים':
    audio = 'sonet'
    !wget --no-check-certificate -nc https://eyalgruss.com/fomm/sonet.mp3
  elif audio == 'אני שולה':
    audio = 'shoula'
    !wget --no-check-certificate -nc https://eyalgruss.com/fomm/shoula.mp3
  elif audio == 'אריק ובנץ (2 דוברים)':
    audio = 'dialog_heb'
    if not os.path.exists('/content/dialog_heb.mp3'):
      !youtube-dl --no-playlist --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=rrZ3bo4VmpQ -o "/content/dialog_heb.%(ext)s"
  elif audio == 'אריק ובנץ וגנץ (3 דוברים)':
    audio = 'trialog_heb'
    if not os.path.exists('/content/trialog_heb.mp3'):
      !youtube-dl --no-playlist --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=HOKJnkG5MXQ -o "/content/trialog_heb.%(ext)s"
  elif audio == 'Grab from uploaded video':
    grab = True
  elif audio == '':
    audio = 'custom'
  else:
    manual = True
  audio = '/content/'+audio
  if manual:
    for ext in ['mp3','wav','m4a','aac','ogg','flac','wma','aiff','opus','amr','ac3','mp4']:
      if os.path.exists(audio+'.'+ext):
        audio += '.'+ext
        break
      if os.path.exists(audio+'.'+ext.upper()):
        audio += '.'+ext.upper()
        break
  else:
    audio += '.mp3'
  assert grab or os.path.exists(audio), 'Error: could not find audio file: '+audio

  %cd /content/Wav2Lip
  outputs = []
  for im in inputs:
    !rm -rf /content/Wav2Lip/temp/*
    infile = '/content/sample_data/'+im
    ext = infile.rsplit('.',1)[1]
    if ext != ext.lower() or "'" in infile or ' ' in infile:
      ext = ext.lower()
      lower = infile.rsplit('.',1)[0].replace("'",'').replace(' ','_')+'.'+ext
      !rm -rf "$lower"
      os.rename(infile, lower)
      infile = lower
    outfile = '/content/'+im.rsplit('.',1)[0].replace("'",'').replace(' ','_')+'_out.mp4'
    !rm -rf "$outfile"
    if grab:
      audio = infile
    elif "'" in audio:
      fix = audio.replace("'",'').replace(' ','_')
      !rm -rf "$fix"
      os.rename(audio, fix)
      audio = fix
    if not override_face_detection:
      nosmooth = '' if smooth_face_detection else '--nosmooth'
      !python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "$infile" --audio \"\"$audio\"\" --pads 0 20 0 0 $nosmooth --outfile \"\"$outfile\"\"
    if override_face_detection or os.path.exists('/content/Wav2Lip/temp/faulty_frame.jpg'):
      import cv2
      if override_face_detection:
        print('\nOverriding face detection')
      else:
        print('\nFace not detected - will use whole frame')
      if ext in ['jpg', 'png', 'jpeg']:
        frame = cv2.imread(infile)
      else:
        video_stream = cv2.VideoCapture(infile)
        still_reading, frame = video_stream.read()
      y2,x2 = frame.shape[:2]
      if override_face_detection:
        x1 = left
        y1 = top
        x2 = min(left+width, x2)
        y2 = min(top+height, y2)
      else:
        x1 = y1 = 0
        if x2>y2:
          x1 = (x2-y2)//2
          x2 = x1+y2
      !python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "$infile" --audio \"\"$audio\"\" --box $y1 $y2 $x1 $x2 --pads 0 20 0 0 --outfile \"\"$outfile\"\"
    outputs.append(outfile)

  wav = None
  if switch_speakers and len(outputs)>1 and not grab:
    wav = audio.rsplit('.',1)[0]+'.wav'
    !ffmpeg -i "$audio" "$wav" -y
    min_dt = 0.5
    if model.startswith('pyannote-audio'):
      !pip install pyannote.audio==1.1.1
      import torch
      import pyannote.core #https://github.com/pyannote/pyannote-audio/issues/561
      from pyannote.audio.features.utils import get_audio_duration
      if model.endswith('AMI'):
        pipeline = torch.hub.load('pyannote/pyannote-audio', 'dia_ami')
      else:
        pipeline = torch.hub.load('pyannote/pyannote-audio', 'dia')
      cls = pipeline({'audio':wav})
      tmp_segs = [((s.start,s.end),l) for s,_,l in cls.itertracks(yield_label=True)]
      segs = []
      prev_ind = None
      prev_start = None
      for (start,end),ind in tmp_segs+[((get_audio_duration({'audio':wav}),None),None)]:
        if ind!=prev_ind:
          if prev_ind is not None:
            segs.append([(prev_start,start),prev_ind])
          prev_ind = ind
          prev_start = start
    elif model=='pyAudioAnalysis':
      !pip install hmmlearn==0.2.8
      !pip install eyeD3==0.9.5
      !pip install pydub==0.24.0
      !pip install pyAudioAnalysis
      from pyAudioAnalysis import audioSegmentation as aS
      mid_window=2
      mid_step=0.2
      short_window=0.05
      lda_dim=0 #35
      cls = aS.speaker_diarization(wav, len(outputs), mid_window=mid_window, mid_step=mid_step, short_window=short_window, lda_dim=lda_dim)
      segs = list(zip(*aS.labels_to_segments(cls, mid_step)))
    deleted = 0
    unified = 0
    if min_dt:
      for i in range(len(segs)-1,0,-1):
        if segs[i][0][1]-segs[i][0][0]<min_dt:
          if i+1<len(segs) and segs[i-1][1] == segs[i+1][1]:
            segs[i-1] = ((segs[i-1][0][0],segs[i+1][0][1]),segs[i-1][1])
            del segs[i+1]
            unified += 1
          else:
            segs[i-1] = ((segs[i-1][0][0],segs[i][0][1]),segs[i-1][1])
          del segs[i]
          deleted += 1
    inds = {}
    my_ind = 0
    with open('/content/list.txt','w',encoding='utf8') as f:
      for i,((start,end),ind) in enumerate(segs):
        if ind not in inds:
          inds[ind] = my_ind%len(outputs)
          my_ind += 1
        f.write("file '%s'\n"%outputs[inds[ind]])
        if i>0:
          f.write('inpoint %f\n'%start)
        if i<len(segs)-1:
          f.write('outpoint %f\n'%end)
    !ffmpeg -f concat -safe 0 -i /content/list.txt -i "{outputs[0]}" -map 0:v -map 1:a -c:v libx264 -c:a aac -vf "crop=trunc(iw/2)*2:trunc(ih/2)*2" -pix_fmt yuv420p -profile:v baseline -movflags +faststart /content/combined.mp4 -y
    new_outputs = ['/content/combined.mp4']
    if len(outputs)==2:
      with open('/content/list2.txt','w',encoding='utf8') as f:
        for i,((start,end),ind) in enumerate(segs):
          f.write("file '%s'\n"%outputs[1-inds[ind]])
          if i>0:
            f.write('inpoint %f\n'%start)
          if i<len(segs)-1:
            f.write('outpoint %f\n'%end)
      !ffmpeg -f concat -safe 0 -i /content/list2.txt -i "{outputs[1]}" -map 0:v -map 1:a -c:v libx264 -c:a aac -vf "crop=trunc(iw/2)*2:trunc(ih/2)*2" -pix_fmt yuv420p -profile:v baseline -movflags +faststart /content/combined2.mp4 -y
      new_outputs.append('/content/combined2.mp4')
    outputs = new_outputs

  from IPython.display import HTML, clear_output
  from base64 import b64encode

  clear_output()
  if wav:
    print('speakers=%d segments=%d deleted=%d unified=%d'%(len(inds), len(segs),deleted,unified))
  muted = 'muted'
  for i,file in enumerate(reversed(outputs)):
    if i==len(outputs)-1:
      muted = ''
    try:
      with open(file, 'rb') as f:
        data_url = "data:video/mp4;base64," + b64encode(f.read()).decode()
      display(HTML("""
      <video width=600 controls autoplay loop %s>
            <source src="%s" type="video/mp4">
      </video>""" % (muted,data_url)))
    except Exception:
      pass
  if wav:
    print('speakers=%d segments=%d deleted=%d unified=%d'%(len(inds), len(segs),deleted,unified))
  for file in outputs:
    try:
      files.download(file)
    except Exception:
      pass
