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
from webdemo.dialog_manager import dialog_model


from flask import Flask, render_template, request
import json


app = Flask(__name__)



wav2vec = inference_utils.load_wav2vec(config.WAV2VEC_CHECKPOINT_PATH).eval()
vaasr_model = inference_utils.load_vaasr_model(config.VAASR_CHECKPOINT_PATH).eval()
class_dict = data.get_asr_class_dict_fr()


@app.route("/")
def home():
    return render_template("app.html")


@app.route("/asr", methods=["POST"])
def asr():
    current_state = int(request.form['current_state'])
    current_language = request.form['current_language']
    wav_input_16khz = inference_utils.load_audio_from_file(request.files['audiodata'])
    
    sorted_class_ids, class_logits, class_probs = inference_utils.get_va_asr_output(wav2vec, vaasr_model, wav_input_16khz, config.MAX_SEQUENCE_LENGTH)
    class_id, class_prob, new_state_id, new_language, reply_clips = dialog_model(current_state, current_language, sorted_class_ids[0].tolist(), class_logits[0].tolist())

    result = {
        "class_id": class_id,
        "class_description": class_dict[class_id],
        "class_prob_orig": class_probs[0].tolist()[class_id],
        "class_prob_ctx": class_prob,
        "new_state": new_state_id,
        "new_language": new_language,
        "reply_clips": reply_clips 
    }
    
    return json.dumps(result)
