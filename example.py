import numpy as np
import soundfile as sf
import yaml
import tensorflow as tf
import os
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor
from pydub import AudioSegment
from os import listdir
from os.path import isfile, join
import sys
from glob import glob
from pathlib import Path

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

#mypath = "../Blog_TbeckenhauerGithubIo/"
#mypath = "../tbeckenhauer.github.io/"
mypath = "."

onlyfiles = list(Path(mypath).rglob("*.markdown"))

for f in onlyfiles:
    f = str(f)
    if "_drafts" in f:
        continue
    if "_postsBacklog" in f:
        continue
    if "vendor" in f:
        continue
    else:
        print("generating"+f)

    openFile = open(f,"r")
    fileTextArr = openFile.readlines()
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]
    frontMatterIndexes = get_indexes("---\n", fileTextArr);
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

    sf.write(f+'.wav', audio_after, 22050, 'PCM_24')
    wavFile = AudioSegment.from_wav(f+'.wav')
    wavFile.export(f+'.mp3', format="mp3")



