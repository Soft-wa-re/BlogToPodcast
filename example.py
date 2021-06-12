
import numpy as np
import soundfile as sf
import yaml

import tensorflow as tf

from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor

import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)

# initialize fastspeech2 model.
fastspeech2 = TFAutoModel.from_pretrained("tensorspeech/tts-fastspeech2-ljspeech-en")


# initialize mb_melgan model
mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-ljspeech-en")


# inference
processor = AutoProcessor.from_pretrained("tensorspeech/tts-fastspeech2-ljspeech-en")


from pydub import AudioSegment
from os import listdir
from os.path import isfile, join
import sys
from glob import glob
from pathlib import Path
mypath = "../tbeckenhauer.github.io/"
onlyfiles = list(Path(mypath).rglob("*.markdown"))
#print(onlyfiles)
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


for f in onlyfiles:
    f = str(f)
    print(f)
    if "_postsBacklog" in f:
        continue
    else:
        print(f)
    file1 = open(f,"r")
    fileTextArr = file1.readlines()
    fileTextArr = (" ".join(line.strip() for line in fileTextArr))
    fileTextArr = fileTextArr.split('.')
    audio_before = None
    audio_after = None

    for i, fTxt in enumerate(fileTextArr): 
        try:
            if(0 < len(fTxt)):
                ids = processor.text_to_sequence(fTxt+".")

                mel_before, mel_after, duration_outputs, _, _ = fastspeech2.inference(
                    input_ids=tf.expand_dims(tf.convert_to_tensor(ids, dtype=tf.int32), 0),
                    speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
                    speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
                    f0_ratios =tf.convert_to_tensor([1.0], dtype=tf.float32),
                    energy_ratios =tf.convert_to_tensor([1.0], dtype=tf.float32),
                )

                # melgan inference
                if None == audio_before:
                    audio_before = mb_melgan.inference(mel_before)[0, :, 0]
                    audio_after = mb_melgan.inference(mel_after)[0, :, 0]
                else:
                    audio_before = tf.concat([audio_before, mb_melgan.inference(mel_before)[0, :, 0]], 0)
                    audio_after = tf.concat([audio_after, mb_melgan.inference(mel_after)[0, :, 0]], 0)

        except:
            print("your sentence was probably too long")
            print("Unexpected error:", sys.exc_info()[0])
            print(i)
            print(len(fTxt))
            print(fTxt)

    # save to file
    #sf.write('./audio/'+f+'.before.wav', audio_before, 22050, "PCM_16")
    #sf.write('./audio/'+f+'.after.wav', audio_after, 22050, "PCM_16")
    #sf.write('./audio/'+f+'.before.wav', audio_before, 22050, "FLAC")
    sf.write(f+'.after.wav', audio_after, 22050, 'PCM_24')
    wavFile = AudioSegment.from_wav(f+'.after.wav')
    wavFile.export(f+'.after.mp3', format="mp3")



