DATA_DIR = /media/xtrem/data/datasets/radio_data
BUILD_DIR = /media/xtrem/data/experiments/nicolingua-0001-language-id

.PHONY: samples features-c features-z clean-samples clean-features-c clean-features-z count-files

samples: $(BUILD_DIR)/audio_samples

features-c: ${BUILD_DIR}/wav2vec_features-c

features-z: ${BUILD_DIR}/wav2vec_features-z

clean-samples:
	rm -rf $(BUILD_DIR)/audio_samples

clean-features-c: 
	rm -rf ${BUILD_DIR}/wav2vec_features-c

clean-features-z: 
	rm -rf ${BUILD_DIR}/wav2vec_features-z

count-files:
	echo "samples: `ls $(BUILD_DIR)/audio_samples/ | wc -l`"
	echo "features-z `ls ${BUILD_DIR}/wav2vec_features-z/ | wc -l`"
	echo "features-c `ls ${BUILD_DIR}/wav2vec_features-c/ | wc -l`"

$(BUILD_DIR)/audio_samples:
	python scripts/sample_audio_segments.py $(DATA_DIR) $(BUILD_DIR)/audio_samples --worker-count 32

${BUILD_DIR}/wav2vec_features-c:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(BUILD_DIR)/audio_samples \
		--output ${BUILD_DIR}/wav2vec_features-c \
		--model /media/xtrem/code/lib/models/acoustic_models/wav2vec/wav2vec_large.pt \
		--gpu 0 \
		--split ""

${BUILD_DIR}/wav2vec_features-z:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(BUILD_DIR)/audio_samples \
		--output ${BUILD_DIR}/wav2vec_features-z \
		--model /media/xtrem/code/lib/models/acoustic_models/wav2vec/wav2vec_large.pt \
		--gpu 1 \
		--split "" \
		--use-feat




# Keywords associated with mostly musical content: "MUSIQUE" "FOLKLORES" "RETRO" "PRETETE"
# cat /media/xtrem/data/tmp-waves/samples.csv |grep -v -e "MUSIQUE" -e "FOLKLORES" -e "RETRO" -e "PRETETE" | shuf | head | awk  '{FS=","; print $2}'
