
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


from os import listdir
from os.path import isfile, join
mypath = "./posts"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for f in onlyfiles:
    print(f)
    print(f+".wav")
    file1 = open("./posts/"+f,"r")
    fileText = file1.readlines()
    fileText = (" ".join(line.strip() for line in fileText))


    ids = processor.text_to_sequence(fileText)
    #408 seems to be the character limit, I don't see that in the documenation, may be a memory issue, but I've got a ton of memory unless docker is doing something funky.
    #ids = processor.text_to_sequence("Recent research at Harvard has shown meditating for as little as 8 weeks, can actually increase the grey matter in the parts of the brain responsible for emotional regulation, and learning.")
    # fastspeech inference

    mel_before, mel_after, duration_outputs, _, _ = fastspeech2.inference(
        input_ids=tf.expand_dims(tf.convert_to_tensor(ids, dtype=tf.int32), 0),
        speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
        speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        f0_ratios =tf.convert_to_tensor([1.0], dtype=tf.float32),
        energy_ratios =tf.convert_to_tensor([1.0], dtype=tf.float32),
    )

    # melgan inference
    #audio_before = mb_melgan.inference(mel_before)[0, :, 0]
    audio_after = mb_melgan.inference(mel_after)[0, :, 0]

    # save to file
    #sf.write(f+'.before.wav', audio_before, 22050, "PCM_16")
    sf.write(f+'.after.wav', audio_after, 22050, "PCM_16")

