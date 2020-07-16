python sample_audio_segments.py /media/xtrem/data/datasets/radio_data/ /media/xtrem/data/experiments/language-id/radio_data-samples
# cat /media/xtrem/data/tmp-waves/samples.csv |grep -v -e "MUSIQUE" -e "FOLKLORES" -e "RETRO" -e "PRETETE" | shuf | head | awk  '{FS=","; print $2}'

python ../fairseq/examples/wav2vec/wav2vec_featurize.py --input /media/xtrem/data/datasets/radio_data-samples/ --output /media/xtrem/data/datasets/radio_data-features --model /media/xtrem/code/lib/models/acoustic_models/wav2vec/wav2vec_large.pt --gpu 0 --split ""