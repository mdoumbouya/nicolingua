from pathlib import Path
import argparse
import torch
import fairseq
import models
import data
import pydub
from pydub.effects import normalize
import numpy as np
import soundfile as sf
import inference_utils



def main(args):
    wav2vec = inference_utils.load_wav2vec(args.wav2vec_checkpoint)
    vaasr_model = inference_utils.load_vaasr_model(args.vaasr_checkpoint)
    class_dict = data.get_asr_class_dict()

    for fname in Path(args.input_audio_dir).iterdir():
        if fname.suffix not in {".wav", ".mp3"}:
            continue

        
        # wav_input_16khz = read_audio(fname)
        wav_input_16khz = inference_utils.load_audio_from_file(fname)
        
        sorted_class_ids, class_probs = inference_utils.get_va_asr_output(wav2vec, vaasr_model, wav_input_16khz, args.max_sequence_length)
        
        for n in range(sorted_class_ids.shape[0]):
            for i in range(5):
                class_id = sorted_class_ids[n][i].item()
                print("{}  -> {} : {}".format(
                    fname.stem,
                    class_dict[class_id],
                    class_probs[n][class_id])
                )


def parse_arguments():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--input-audio-dir", default="/media/xtrem/data/experiments/nicolingua-0004-va-asr/datasets/gn_va_asr_dataset_2020-09-04_01/annotated_segments/")
    parser.add_argument("--input-audio-dir", default="/home/xtrem/test_asr")    
    parser.add_argument("--wav2vec-checkpoint", default="/media/xtrem/data/experiments/nicolingua-0003-wa-wav2vec/wav2vec-training-exp-01/checkpoints/checkpoint_best.pt")
    parser.add_argument("--vaasr-checkpoint", default="/media/xtrem/code/git/nicolingua/notebooks/E400/results_400/checkpoints/VAASRCNN3PoolMaxAggMax/retrained-wav2vec_features-c_0_checkpoints/1000.pt")
    parser.add_argument("--frame-rate", default=16000)
    parser.add_argument("--channels", default=1)
    parser.add_argument("--max-sequence-length", type=int, default=300)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)