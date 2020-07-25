DATA_DIR = /media/xtrem/data/datasets/radio_data
BUILD_DIR = /media/xtrem/data/experiments/nicolingua-0001-language-id

export CUDA_VISIBLE_DEVICES=0,1

.PHONY: samples features-c features-z clean-samples clean-features-c clean-features-z count-files

samples: $(BUILD_DIR)/audio_samples

samples-annotation-space: $(BUILD_DIR)/audio_samples_annotation_space

features-c: ${BUILD_DIR}/wav2vec_features-c
retrained-features-c: ${BUILD_DIR}/retrained-wav2vec_features-c

features-z: ${BUILD_DIR}/wav2vec_features-z
retrained-features-z: ${BUILD_DIR}/retrained-wav2vec_features-z

clean-samples:
	rm -rf $(BUILD_DIR)/audio_samples

clean-features-c: 
	rm -rf ${BUILD_DIR}/wav2vec_features-c

clean-features-z: 
	rm -rf ${BUILD_DIR}/wav2vec_features-z

clean-retrained-features-c: 
	rm -rf ${BUILD_DIR}/retrained-wav2vec_features-c


clean-retrained-features-z: 
	rm -rf ${BUILD_DIR}/retrained-wav2vec_features-z

count-files:
	echo "samples: `ls $(BUILD_DIR)/audio_samples/ | wc -l`"
	echo "features-z `ls ${BUILD_DIR}/wav2vec_features-z/ | wc -l`"
	echo "features-c `ls ${BUILD_DIR}/wav2vec_features-c/ | wc -l`"

$(BUILD_DIR)/audio_samples:
	python scripts/sample_audio_segments.py $(DATA_DIR) $(BUILD_DIR)/audio_samples --worker-count 32


$(BUILD_DIR)/audio_samples_annotation_space:
	# split files into mostly music and mostly speech

# original features
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

# retrained features
${BUILD_DIR}/retrained-wav2vec_features-c:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(BUILD_DIR)/audio_samples \
		--output ${BUILD_DIR}/retrained-wav2vec_features-c \
		--model $(BUILD_DIR)/wav2vec-training-exp-01/checkpoints/checkpoint_best.pt \
		--gpu 0 \
		--split ""

${BUILD_DIR}/retrained-wav2vec_features-z:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(BUILD_DIR)/audio_samples \
		--output ${BUILD_DIR}/retrained-wav2vec_features-z \
		--model $(BUILD_DIR)/wav2vec-training-exp-01/checkpoints/checkpoint_best.pt \
		--gpu 1 \
		--split "" \
		--use-feat



# Keywords associated with mostly musical content: "MUSIQUE" "FOLKLORES" "RETRO" "PRETETE"
# cat /media/xtrem/data/tmp-waves/samples.csv |grep -v -e "MUSIQUE" -e "FOLKLORES" -e "RETRO" -e "PRETETE" | shuf | head | awk  '{FS=","; print $2}'




# wav2vec training

# wav
train-01-manifest:
	mkdir -p $(BUILD_DIR)/wav2vec-training-exp-01/manifest/
	python ../fairseq/examples/wav2vec/wav2vec_manifest.py \
		$(BUILD_DIR)/audio_samples \
		--dest $(BUILD_DIR)/wav2vec-training-exp-01/manifest/ \
		--ext wav

train-01-train-wav2vec:
	mkdir -p $(BUILD_DIR)/wav2vec-training-exp-01/checkpoints/
	mkdir -p $(BUILD_DIR)/wav2vec-training-exp-01/logs/
	python ../fairseq/train.py \
		$(BUILD_DIR)/wav2vec-training-exp-01/manifest/ \
		--save-dir $(BUILD_DIR)/wav2vec-training-exp-01/checkpoints/ \
		--tensorboard-logdir $(BUILD_DIR)/wav2vec-training-exp-01/logs/ \
		--num-workers 6 \
		--max-update 400000 \
		--save-interval 1 \
		--no-epoch-checkpoints \
		--arch wav2vec \
		--task audio_pretraining \
		--lr 1e-06 \
		--min-lr 1e-09 \
		--optimizer adam \
		--max-lr 0.005 \
		--lr-scheduler cosine \
		--conv-feature-layers "[(512, 10, 5), (512, 8, 4), (512, 4, 2), (512, 4, 2), (512, 4, 2), (512, 1, 1), (512, 1, 1)]" \
		--conv-aggregator-layers "[(512, 2, 1), (512, 3, 1), (512, 4, 1), (512, 5, 1), (512, 6, 1), (512, 7, 1), (512, 8, 1), (512, 9, 1), (512, 10, 1), (512, 11, 1), (512, 12, 1), (512, 13, 1)]" \
		--skip-connections-agg \
		--residual-scale 0.5 \
		--log-compression \
		--warmup-updates 500 \
		--warmup-init-lr 1e-07 \
		--criterion binary_cross_entropy \
		--num-negatives 10 \
		--max-sample-size 150000 \
		--max-tokens 1500000 \
		--skip-invalid-size-inputs-valid-test 

# NOTE: your device does NOT support faster training with --fp16,please switch to FP32 which is likely to be faster

# --restore-file /media/xtrem/code/lib/models/acoustic_models/wav2vec/wav2vec_large.pt 



# Tag editor tool

start-tag-editor:
	cd html && python3.6 -m http.server


extract-id3v2-metadata:
	python scripts/extract_annotations.py \
		/Users/moussadoumbouya/git/datasets/language-id-annotation/audio_samples/ \
		/Users/moussadoumbouya/git/datasets/language-id-annotation/metadata.csv

	cat /Users/moussadoumbouya/git/datasets/language-id-annotation/metadata.csv

	cat /Users/moussadoumbouya/git/datasets/language-id-annotation/metadata.csv | wc -l

copy-unknown-lg:
	python scripts/copy_files_by_annotation.py \
		/Users/moussadoumbouya/git/datasets/language-id-annotation/audio_samples/ \
		/Users/moussadoumbouya/git/datasets/language-id-annotation/audio_samples_unknown_lg \
		--tag lng-unknown

clean-unknown-lg:
	rm -rf /Users/moussadoumbouya/git/datasets/language-id-annotation/audio_samples_unknown_lg


tag-frequencies:
	python scripts/compute_tag_frequencies.py\
		/Users/moussadoumbouya/git/datasets/language-id-annotation/audio_samples/ \
		/Users/moussadoumbouya/git/datasets/language-id-annotation/tag_frequencies.csv



# other notes
# 0a505ae8-b3b1-4b47-a84c-75298caf6f39.wav (multilingual utterance telephone)
# 0a978fe1-7bad-4ea7-be32-f88f40de085a.wav (dialog)
# mispelled tag multilingual-named-endity
# 0b4df82d-a7db-4dd8-9960-de97d68406ab.wav arabic utterances
# 0d46c65b-b573-4b58-b46e-4688f6946c27.wav health education
# 0dc8839b-2a8e-468b-b5c8-f483fb5d80a3.wav background islamic reading
# 
# 0c73a83d-c0fc-4ac4-994c-a2b14ede31cb.wav background koran reading
# 0c69ed59-27b9-4af9-97c3-2087f882917b.wav background islamic singing
# 0e3f5243-69d5-42e0-ae79-dacda5f79d3a.wav background islaming reading
# 000ec3a1-f7da-4eb8-b0a9-df7b81d9e6b3.wav (la daba)
# 0f4c3c2e-5e44-4c7a-a2b7-95799919ee07.wav background islamic reading
# 0f28ee0c-b462-4ffa-9faf-f6f343466d9f.wav background islamic reading
# Notes:
# 
# 
# Assertions:
# Assert that multilinqual-* tagged clips contain more than 1 language
# non speech and non forground music
# non speech and non song



# 0facc456-9ccd-4643-a19d-fc4cab4b9273.wav (CENI education election)

# --restore-file /media/xtrem/code/lib/models/acoustic_models/wav2vec/wav2vec_large.pt \


######
### Clustering
######

cluster-with-original-wav2vec:
	python scripts/cluster_audio_features.py

cluster-with-retrained-wav2vec:

