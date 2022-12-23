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

markdown_files = list(Path(MY_PATH).rglob("*.markdown"))

for MD_FILE in markdown_files:
    try:
        MD_FILE = str(MD_FILE)
        if "_drafts" in MD_FILE:
            print("Directory not supported:" +MD_FILE)
            continue
        if "_postsBacklog" in MD_FILE:
            print("Directory not supported:" +MD_FILE)
            continue
        if "vendor" in MD_FILE:
            print("Directory not supported:" +MD_FILE)
            continue
        if exists(MD_FILE+".mp3"):
            print(MD_FILE+".mp3" + " exists")
            continue
        print("generating"+MD_FILE)
    except: # pylint: disable=bare-except
        print("Unexpected error:", sys.exc_info()[0])
        print("Error in file:"+MD_FILE)
        continue

    try:
        post = frontmatter.load(MD_FILE)
        if 'blogcast' not in post.metadata:
            print(MD_FILE+" does not have blogToPodcast Key")
            continue

        CONTENT = post.content
        CONTENT = CONTENT.replace("Array.prototype.indexOf(...) >= 0", "Array Dot indexOf")
        CONTENT = CONTENT.replace("String.prototype.indexOf(...) >= 0", "String Dot indexOf")
        CONTENT = CONTENT.replace("Array.prototype.includes(...) >= 0", "Array Dot includes")
        CONTENT = CONTENT.replace("String.prototype.includes(...) >= 0", "String Dot includes")
        CONTENT = CONTENT.replace(".includes(...)", "Dot includes")
        CONTENT = CONTENT.replace(".indexOf(...)", "Dot indexOf")
        WIKI_ECMA_PATH = "https://en.wikipedia.org/\
        wiki/ECMAScript#7th_Edition_%E2%80%93_ECMAScript_2016"
        CONTENT = CONTENT.replace(WIKI_ECMA_PATH, "")
        MOZILLA_PATH = "https://developer.mozilla.org/\
        en-US/docs/Web/JavaScript/Reference/Global_Objects/String/includes#polyfill"
        CONTENT = CONTENT.replace(MOZILLA_PATH, "")
        CONTENT = re.sub("```javascript.*```", "", CONTENT, re.DOTALL)
        fileTextArr = CONTENT.split('.')

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
            except: # pylint: disable=bare-except
                print("your sentence was probably too long")
                print("Unexpected error:", sys.exc_info()[0])
                print(i)
                print(len(fTxt))
                print(fTxt)

        sf.write(MD_FILE+'.wav', AUDIO_AFTER, 22050, 'PCM_24')
        wavFile = AudioSegment.from_wav(MD_FILE+'.wav')
        os.remove(MD_FILE+'.wav')
        wavFile.export(MD_FILE+'.mp3', format="mp3")

    except: # pylint: disable=bare-except
        print(MD_FILE)
        print(post.metadata)
        print(post.metadata['blogcast'])
