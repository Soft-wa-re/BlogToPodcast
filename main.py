#!/usr/bin/env python3

"""Main Module: This module has basically everything even though it shouldn't """

from pathlib import Path
import re
import sys
from os.path import exists
import os
import soundfile as sf
import tensorflow as tf
import frontmatter
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor
from pydub import AudioSegment

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}
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

MY_PATH = "."

onlyfiles = list(Path(MY_PATH).rglob("*.markdown"))

for f in onlyfiles:
    try:
        f = str(f)
        if "_drafts" in f:
            print("Directory not supported:" +f)
            continue
        if "_postsBacklog" in f:
            print("Directory not supported:" +f)
            continue
        if "vendor" in f:
            print("Directory not supported:" +f)
            continue
        if exists(f+".mp3"):
            print(f+".mp3" + " exists")
            continue
        else:
            print("generating"+f)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Error in file:"+f)
        continue

    try:
        post = frontmatter.load(f)
        if 'blogcast' not in post.metadata:
            print(f+" does not have blogToPodcast Key")
            continue

        content = post.content
        content = content.replace("Array.prototype.indexOf(...) >= 0", "Array Dot indexOf")
        content = content.replace("String.prototype.indexOf(...) >= 0", "String Dot indexOf")
        content = content.replace("Array.prototype.includes(...) >= 0", "Array Dot includes")
        content = content.replace("String.prototype.includes(...) >= 0", "String Dot includes")
        content = content.replace(".includes(...)", "Dot includes")
        content = content.replace(".indexOf(...)", "Dot indexOf")
        wikiEcmaPath = "https://en.wikipedia.org/\
        wiki/ECMAScript#7th_Edition_%E2%80%93_ECMAScript_2016"
        content = content.replace(wikiEcmaPath, "")
        mozillaPath = "https://developer.mozilla.org/\
        en-US/docs/Web/JavaScript/Reference/Global_Objects/String/includes#polyfill"
        content = content.replace(mozillaPath, "")
        content = re.sub("```javascript.*```", "", content, re.DOTALL)
        fileTextArr = content.split('.')

        AUDIO_BEFORE = None
        AUDIO_AFTER = None

        for i, fTxt in enumerate(fileTextArr):
            try:
                if 0 < len(fTxt):
                    ids = processor.text_to_sequence(fTxt+".")

                    mel_before, mel_after, duration_outputs, _, _ = fastspeech2.inference(
                        input_ids=tf.expand_dims(tf.convert_to_tensor(ids, dtype=tf.int32), 0),
                        speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
                        speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
                        f0_ratios =tf.convert_to_tensor([1.0], dtype=tf.float32),
                        energy_ratios =tf.convert_to_tensor([1.0], dtype=tf.float32),
                    )

                    # melgan inference
                    if None is AUDIO_BEFORE:
                        AUDIO_BEFORE = mb_melgan.inference(mel_before)[0, :, 0]
                        AUDIO_AFTER = mb_melgan.inference(mel_after)[0, :, 0]
                    else:
                        AUDIO_BEFORE = tf.concat([
                            AUDIO_BEFORE,
                            mb_melgan.inference(mel_before)[0, :, 0]], 0)
                        AUDIO_AFTER = tf.concat([
                            AUDIO_AFTER,
                            mb_melgan.inference(mel_after)[0, :, 0]], 0)
            except:
                print("your sentence was probably too long")
                print("Unexpected error:", sys.exc_info()[0])
                print(i)
                print(len(fTxt))
                print(fTxt)

        sf.write(f+'.wav', AUDIO_AFTER, 22050, 'PCM_24')
        wavFile = AudioSegment.from_wav(f+'.wav')
        os.remove(f+'.wav')
        wavFile.export(f+'.mp3', format="mp3")

    except:
        print(f)
        print(post.metadata)
        print(post.metadata['blogcast'])
