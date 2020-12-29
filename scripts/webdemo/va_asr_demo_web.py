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


from flask import Flask, render_template, request
import json

app = Flask(__name__)

WAV2VEC_CHECKPOINT_PATH = "/media/xtrem/data/experiments/nicolingua-0003-wa-wav2vec/wav2vec-training-exp-01/checkpoints/checkpoint_best.pt"
VAASR_CHECKPOINT_PATH = "/media/xtrem/code/git/nicolingua/notebooks/E400/results_400/checkpoints/VAASRCNN3PoolMaxAggMax/retrained-wav2vec_features-c_0_checkpoints/1000.pt"
MAX_SEQUENCE_LENGTH = 300

wav2vec = inference_utils.load_wav2vec(WAV2VEC_CHECKPOINT_PATH)
vaasr_model = inference_utils.load_vaasr_model(VAASR_CHECKPOINT_PATH)
class_dict = data.get_asr_class_dict()


@app.route("/")
def home():
    return render_template("app.html")


@app.route("/asr", methods=["POST"])
def asr():
    # wav_input_16khz = inference_utils.load_audio_from_file(fname)
    wav_input_16khz = inference_utils.load_audio_from_file(request.files['audiodata'])
    
    sorted_class_ids, class_probs = inference_utils.get_va_asr_output(wav2vec, vaasr_model, wav_input_16khz, MAX_SEQUENCE_LENGTH)
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


