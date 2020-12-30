import sys
import os

import va_asr

from pathlib import Path
import argparse
import torch
import fairseq
import pydub
from pydub.effects import normalize
import numpy as np
import soundfile as sf

from va_asr import inference_utils
from va_asr import models
from va_asr import data
from webdemo import config


from flask import Flask, render_template, request
import json


app = Flask(__name__)



wav2vec = inference_utils.load_wav2vec(config.WAV2VEC_CHECKPOINT_PATH)
vaasr_model = inference_utils.load_vaasr_model(config.VAASR_CHECKPOINT_PATH)
class_dict = data.get_asr_class_dict_fr()


@app.route("/")
def home():
    return render_template("app.html")


@app.route("/asr", methods=["POST"])
def asr():
    # wav_input_16khz = inference_utils.load_audio_from_file(fname)
    wav_input_16khz = inference_utils.load_audio_from_file(request.files['audiodata'])
    
    sorted_class_ids, class_probs = inference_utils.get_va_asr_output(wav2vec, vaasr_model, wav_input_16khz, config.MAX_SEQUENCE_LENGTH)
    sorted_class_ids = sorted_class_ids[0]
    class_probs = class_probs[0]

    results = []
    
    for i in range(5):
        class_id = sorted_class_ids[i].item()
        results.append(
            {
                "c": class_dict[class_id],
                "p": class_probs[class_id].item()
            }
        )

    return json.dumps(results)
