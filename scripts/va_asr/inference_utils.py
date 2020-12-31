from pathlib import Path
import argparse
import torch
import fairseq
import pydub
from pydub.effects import normalize
import numpy as np
import soundfile as sf
from io import BytesIO

from va_asr import models
from va_asr import data




def load_wav2vec(checkpoint_path):
    model, cfg, task = fairseq.checkpoint_utils.load_model_ensemble_and_task([checkpoint_path])
    model = model[0]
    model.eval()
    return model


def get_wav2vec_context_feature(model, wav, max_sequence_length):
    x = torch.from_numpy(wav).float().unsqueeze(0)
    z = model.feature_extractor(x)
    c = model.feature_aggregator(z)
    c = torch.transpose(c, 1, 2)
    padded_features = torch.zeros((1, max_sequence_length, 512), dtype=c.dtype)
    padded_features[0, :c.shape[1], :] = c[0, :max_sequence_length, :]
    return padded_features


def get_wav2vec_latent_feature(model, wav):
    z = model.feature_extractor(wav)
    return z


def load_vaasr_model(checkpoint_path):
    return models.load_model(checkpoint_path)


def get_va_asr_output(wav2vec_model, va_asr_model, wav, max_sequence_length):
    c = get_wav2vec_context_feature(wav2vec_model, wav, max_sequence_length)
    logits = va_asr_model(c)
    class_probs = torch.softmax(logits, dim=1)
    sorted_class_ids = torch.argsort(class_probs, dim=1, descending=True)
    return sorted_class_ids, class_logits, class_probs


def read_audio(fname):
    """ Load an audio file and return PCM along with the sample rate """
    wav, sr = sf.read(fname)
    print(fname, sr)
    assert sr == 16e3
    return wav

def load_audio_from_file(fname, channels=1, frame_rate=16000):
    sound = pydub.AudioSegment.from_file(fname)
    sound = normalize(sound)
    sound = sound.set_frame_rate(frame_rate)
    sound = sound.set_channels(channels)
    return np.array(sound.get_array_of_samples())


def load_audio_from_webm_blob(opus_audio_bytes, channels=1, frame_rate=16000):
    bio = BytesIO(opus_audio_bytes)
    sound = pydub.AudioSegment.from_file(bio, coded='opus')
    sound = normalize(sound)
    sound = sound.set_frame_rate(frame_rate)
    sound = sound.set_channels(channels)
    return np.array(sound.get_array_of_samples())
