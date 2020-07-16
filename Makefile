DATA_DIR = /media/xtrem/data/datasets/radio_data
BUILD_DIR = /media/xtrem/data/experiments/nicolingua-0001-language-id


phony samples: $(BUILD_DIR)/audio_samples

phony clean-samples:
	rm -rf $(BUILD_DIR)/audio_samples

phony features-c: ${BUILD_DIR}/wav2vec_features-c

phony features-z: ${BUILD_DIR}/wav2vec_features-z

$(BUILD_DIR)/audio_samples:
	python scripts/sample_audio_segments.py $(DATA_DIR) $(BUILD_DIR)/audio_samples --worker-count 32

${BUILD_DIR}/wav2vec_features-c:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input /media/xtrem/data/datasets/radio_data-samples/ \
		--output ${BUILD_DIR}/wav2vec_features-c \
		--model /media/xtrem/code/lib/models/acoustic_models/wav2vec/wav2vec_large.pt \
		--gpu 0 \
		--split ""

${BUILD_DIR}/wav2vec_features-z:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input /media/xtrem/data/datasets/radio_data-samples/ \
		--output ${BUILD_DIR}/wav2vec_features-z \
		--model /media/xtrem/code/lib/models/acoustic_models/wav2vec/wav2vec_large.pt \
		--gpu 1 \
		--split "" \
		--use-feat




# Keywords associated with mostly musical content: "MUSIQUE" "FOLKLORES" "RETRO" "PRETETE"
# cat /media/xtrem/data/tmp-waves/samples.csv |grep -v -e "MUSIQUE" -e "FOLKLORES" -e "RETRO" -e "PRETETE" | shuf | head | awk  '{FS=","; print $2}'
