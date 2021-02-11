# DATA_DIR = /media/xtrem/data/datasets/radio_data
# BUILD_DIR = /media/xtrem/data/experiments/nicolingua-0001-language-id
# VA_ASR_DIR = /media/xtrem/data/experiments/nicolingua-0002-va-asr/datasets/gn_va_asr_dataset_2020-08-26_01

# export CUDA_VISIBLE_DEVICES=0,1
# include default.conf
include datasets_refresh_2.conf

.PHONY: samples features-c features-z clean-samples clean-features-c clean-features-z count-files

samples: $(BUILD_DIR)/audio_samples

samples-annotation-space: $(BUILD_DIR)/audio_samples_annotation_space

features-z: ${BUILD_DIR}/wav2vec_features-z
features-c: ${BUILD_DIR}/wav2vec_features-c
retrained-features-z: ${BUILD_DIR}/retrained-wav2vec_features-z
retrained-features-c: ${BUILD_DIR}/retrained-wav2vec_features-c

test-features-z: ${BUILD_DIR}/test/wav2vec_features-z
test-features-c: ${BUILD_DIR}/test/wav2vec_features-c
test-retrained-features-z: ${BUILD_DIR}/test/retrained-wav2vec_features-z
test-retrained-features-c: ${BUILD_DIR}/test/retrained-wav2vec_features-c
test-counts:
	echo "wav2vec_features-z: `ls ${BUILD_DIR}/test/wav2vec_features-z | wc -l`"
	echo "wav2vec_features-c: `ls ${BUILD_DIR}/test/wav2vec_features-c | wc -l`"
	echo "retrained-wav2vec_features-z: `ls ${BUILD_DIR}/test/retrained-wav2vec_features-z | wc -l`"
	echo "retrained-wav2vec_features-c: `ls ${BUILD_DIR}/test/retrained-wav2vec_features-c | wc -l`"
	


# features-vq: ${BUILD_DIR}/wav2vec-vq_features
# retrained-features-vq: ${BUILD_DIR}/retrained-wav2vec-vq_features


#clean-samples:
#	rm -rf $(BUILD_DIR)/audio_samples

# Radio Corpus
clean-features-c: 
	rm -rf ${BUILD_DIR}/wav2vec_features-c

clean-features-z: 
	rm -rf ${BUILD_DIR}/wav2vec_features-z

clean-retrained-features-c: 
	rm -rf ${BUILD_DIR}/retrained-wav2vec_features-c

clean-retrained-features-z: 
	rm -rf ${BUILD_DIR}/retrained-wav2vec_features-z


# Radio Corpus Test set
clean-test-features-c: 
	rm -rf ${BUILD_DIR}/test/wav2vec_features-c

clean-test-features-z: 
	rm -rf ${BUILD_DIR}/test/wav2vec_features-z

clean-test-retrained-features-c: 
	rm -rf ${BUILD_DIR}/test/retrained-wav2vec_features-c

clean-test-retrained-features-z: 
	rm -rf ${BUILD_DIR}/test/retrained-wav2vec_features-z


count-files:
	echo "samples: `ls $(BUILD_DIR)/audio_samples/ | wc -l`"
	echo "features-z `ls ${BUILD_DIR}/wav2vec_features-z/ | wc -l`"
	echo "features-c `ls ${BUILD_DIR}/wav2vec_features-c/ | wc -l`"

$(BUILD_DIR)/audio_samples:
	python scripts/sample_audio_segments.py $(DATA_DIR) $(BUILD_DIR)/audio_samples --worker-count 32 ${SAMPLE_AUDIO_SEGMENTS_EXTRA_PARAMS}


$(BUILD_DIR)/audio_samples_annotation_space:
	# split files into mostly music and mostly speech

# original features - wav2vec
${BUILD_DIR}/wav2vec_features-c:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(BUILD_DIR)/audio_samples \
		--output ${BUILD_DIR}/wav2vec_features-c \
		--model $(WAV2VEC_BASELINE_CHECKPOINT) \
		--gpu 0 \
		--split ""

${BUILD_DIR}/wav2vec_features-z:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(BUILD_DIR)/audio_samples \
		--output ${BUILD_DIR}/wav2vec_features-z \
		--model $(WAV2VEC_BASELINE_CHECKPOINT) \
		--gpu 1 \
		--split "" \
		--use-feat


# original features - wav2vec - test set
${BUILD_DIR}/test/wav2vec_features-c:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(BUILD_DIR)/test/audio_samples \
		--output ${BUILD_DIR}/test/wav2vec_features-c \
		--model $(WAV2VEC_BASELINE_CHECKPOINT) \
		--gpu 0 \
		--split ""

${BUILD_DIR}/test/wav2vec_features-z:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(BUILD_DIR)/test/audio_samples \
		--output ${BUILD_DIR}/test/wav2vec_features-z \
		--model $(WAV2VEC_BASELINE_CHECKPOINT) \
		--gpu 1 \
		--split "" \
		--use-feat

# original features - wav2vec vq
#${BUILD_DIR}/wav2vec-vq_features:
#	python ../fairseq/examples/wav2vec/vq-wav2vec_featurize.py \
#		--data-dir $(BUILD_DIR)/audio_samples \
#		--output-dir ${BUILD_DIR}/wav2vec-vq_features \
#		--checkpoint /media/xtrem/code/lib/models/acoustic_models/wav2vec/vq-wav2vec.pt \
#		--split "" \
#		--extension wav




# retrained features wav2vec
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

# retrained features wav2vec - test set
${BUILD_DIR}/test/retrained-wav2vec_features-c:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(BUILD_DIR)/test/audio_samples \
		--output ${BUILD_DIR}/test/retrained-wav2vec_features-c \
		--model $(BUILD_DIR)/wav2vec-training-exp-01/checkpoints/checkpoint_best.pt \
		--gpu 0 \
		--split ""

${BUILD_DIR}/test/retrained-wav2vec_features-z:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(BUILD_DIR)/test/audio_samples \
		--output ${BUILD_DIR}/test/retrained-wav2vec_features-z \
		--model $(BUILD_DIR)/wav2vec-training-exp-01/checkpoints/checkpoint_best.pt \
		--gpu 1 \
		--split "" \
		--use-feat


# retrained features - wav2vec vq
#${BUILD_DIR}/retrained-wav2vec-vq_features:
#	python ../fairseq/examples/wav2vec/vq-wav2vec_featurize.py \
#		--data-dir $(BUILD_DIR)/audio_samples \
#		--output-dir ${BUILD_DIR}/retrained-wav2vec-vq_features \
#		--checkpoint $(BUILD_DIR)/wav2vec-training-exp-01/checkpoints-vq/checkpoint_best.pt \
#		--split "" \
#		--extension wav

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




train-01-train-vq-wav2vec:
	python ../fairseq/train.py \
		$(BUILD_DIR)/wav2vec-training-exp-01/manifest/ \
		--save-dir $(BUILD_DIR)/wav2vec-training-exp-01/checkpoints-vq/ \
		--tensorboard-logdir $(BUILD_DIR)/wav2vec-training-exp-01/logs-vq/ \
		--num-workers 6 \
		--fp16 \
		--max-update 1000000 \
		--save-interval 1 \
		--no-epoch-checkpoints \
		--arch wav2vec \
		--task audio_pretraining \
		--lr 1e-06 \
		--min-lr 1e-09 \
		--optimizer adam \
		--max-lr 1e-05 \
		--lr-scheduler cosine \
		--conv-feature-layers "[(512, 10, 5), (512, 8, 4), (512, 4, 2), (512, 4, 2), (512, 4, 2), (512, 1, 1), (512, 1, 1), (512, 1, 1)]" \
		--conv-aggregator-layers "[(512, 2, 1), (512, 3, 1), (512, 4, 1), (512, 5, 1), (512, 6, 1), (512, 7, 1), (512, 8, 1), (512, 9, 1), (512, 10, 1), (512, 11, 1), (512, 12, 1), (512, 13, 1)]" \
		--activation gelu \
		--offset auto \
		--skip-connections-agg \
		--residual-scale 0.5 \
		--vq-type gumbel \
		--vq-groups 2 \
		--vq-depth 2 \
		--combine-groups \
		--vq-vars 320 \
		--vq-temp "(2,0.5,0.999995)" \
		--prediction-steps 12 \
		--warmup-updates 1000 \
		--warmup-init-lr 1e-07 \
		--criterion binary_cross_entropy \
		--num-negatives 10 \
		--max-sample-size 150000 \
		--max-tokens 300000 \
		--cross-sample-negatives 0 \
		--update-freq 1 \
		--seed 2 \
		--skip-invalid-size-inputs-valid-test


train-02-train-wav2vec:
	mkdir -p $(BUILD_DIR)/wav2vec-training-exp-02-small/checkpoints/
	mkdir -p $(BUILD_DIR)/wav2vec-training-exp-02-small/logs/
	python ../fairseq/train.py \
		$(BUILD_DIR)/wav2vec-training-exp-01/manifest/ \
		--save-dir $(BUILD_DIR)/wav2vec-training-exp-02-small/checkpoints/ \
		--tensorboard-logdir $(BUILD_DIR)/wav2vec-training-exp-02-small/logs/ \
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
		--conv-feature-layers "[(512, 10, 5), (512, 8, 4), (512, 4, 2), (512, 4, 2), (512, 4, 2)]" \
		--conv-aggregator-layers "[(512, 3, 1), (512, 3, 1), (512, 3, 1), (512, 3, 1), (512, 3, 1), (512, 3, 1), (512, 3, 1), (512, 3, 1), (512, 3, 1)]" \
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
# VQ --log-keys ["prob_perplexity","code_perplexity","temp"] \
# NOTE: your device does NOT support faster training with --fp16,please switch to FP32 which is likely to be faster

# --restore-file /media/xtrem/code/lib/models/acoustic_models/wav2vec/wav2vec_large.pt 



# Tag editor tool

start-tag-editor:
	cd html && python3.6 -m http.server


test-samples:
	python scripts/extract_annotations.py \
		${TEST_DATA_DIR} \
		${BUILD_DIR}/test \
		--output-audio-files
		

copy-unknown-lg:
	python scripts/copy_files_by_annotation.py \
		/Users/moussadoumbouya/git/datasets/language-id-annotation/audio_samples/ \
		/Users/moussadoumbouya/git/datasets/language-id-annotation/audio_samples_unknown_lg \
		--tag lng-unknown

clean-unknown-lg:
	rm -rf /Users/moussadoumbouya/git/datasets/language-id-annotation/audio_samples_unknown_lg


tag-frequencies:
	python scripts/compute_tag_frequencies.py\
		$(BUILD_DIR)/language-id-annotations/audio_samples/ #\
		#--output-file $(BUILD_DIR)/language-id-annotations/tag_frequencies.csv



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


va-asr-segments: $(VA_ASR_DIR)/annotated_segments/metadata.csv

va-asr-features-z: ${VA_ASR_DIR}/wav2vec_features-z
va-asr-features-c: ${VA_ASR_DIR}/wav2vec_features-c

va-asr-retrained-features-z: ${VA_ASR_DIR}/retrained-wav2vec_features-z
va-asr-retrained-features-c: ${VA_ASR_DIR}/retrained-wav2vec_features-c

va-asr-counts:
	echo "va-asr-features-z: `ls ${VA_ASR_DIR}/wav2vec_features-z | wc -l`"
	echo "va-asr-features-c: `ls ${VA_ASR_DIR}/wav2vec_features-c | wc -l`"
	echo "va-asr-retrained-features-z: `ls ${VA_ASR_DIR}/retrained-wav2vec_features-z | wc -l`"
	echo "va-asr-retrained-features-c: `ls ${VA_ASR_DIR}/retrained-wav2vec_features-c | wc -l`"



clean-va-asr-segments: 
	rm -rf $(VA_ASR_DIR)/annotated_segments/

clean-va-asr-features-z: 
	rm -rf ${VA_ASR_DIR}/wav2vec_features-z

clean-va-asr-retrained-features-z: 
	rm -rf ${VA_ASR_DIR}/retrained-wav2vec_features-z

clean-va-asr-features-c: 
	rm -rf ${VA_ASR_DIR}/wav2vec_features-c

clean-va-asr-retrained-features-c: 
	rm -rf ${VA_ASR_DIR}/retrained-wav2vec_features-c



$(VA_ASR_DIR)/annotated_segments/metadata.csv:
	python scripts/va_asr/extract_audacity_annotations.py \
		--padding-ms 100 \
		$(VA_ASR_DIR)/curation/ \
		$(VA_ASR_DIR)/annotated_segments

	python scripts/va_asr/anonymize_csv.py \
		$(VA_ASR_DIR)/curation/meta/recording_sessions.csv --column-name name > $(VA_ASR_DIR)/curation/meta/recording_sessions_a.csv

	python scripts/va_asr/anonymize_csv.py \
		$(VA_ASR_DIR)/curation/meta/devices.csv --column-name user > $(VA_ASR_DIR)/curation/meta/devices_a.csv

	python scripts/va_asr/anonymize_csv.py \
		$(VA_ASR_DIR)/curation/meta/speakers.csv --column-name name > $(VA_ASR_DIR)/curation/meta/speakers_a.csv

# baseline features - wav2vec
${VA_ASR_DIR}/wav2vec_features-c:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(VA_ASR_DIR)/annotated_segments \
		--output ${VA_ASR_DIR}/wav2vec_features-c \
		--model $(WAV2VEC_BASELINE_CHECKPOINT) \
		--gpu 0 \
		--split ""

${VA_ASR_DIR}/wav2vec_features-z:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(VA_ASR_DIR)/annotated_segments \
		--output ${VA_ASR_DIR}/wav2vec_features-z \
		--model $(WAV2VEC_BASELINE_CHECKPOINT) \
		--gpu 1 \
		--split "" \
		--use-feat

# retrained features wav2vec
${VA_ASR_DIR}/retrained-wav2vec_features-c:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(VA_ASR_DIR)/annotated_segments \
		--output ${VA_ASR_DIR}/retrained-wav2vec_features-c \
		--model $(BUILD_DIR)/wav2vec-training-exp-01/checkpoints/checkpoint_best.pt \
		--gpu 0 \
		--split ""

${VA_ASR_DIR}/retrained-wav2vec_features-z:
	python ../fairseq/examples/wav2vec/wav2vec_featurize.py \
		--input $(VA_ASR_DIR)/annotated_segments \
		--output ${VA_ASR_DIR}/retrained-wav2vec_features-z \
		--model $(BUILD_DIR)/wav2vec-training-exp-01/checkpoints/checkpoint_best.pt \
		--gpu 1 \
		--split "" \
		--use-feat


run-va-asr-experiments-102-cnn1:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN1 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E102/results_102 \
	--epochs 1000 \
	--gpu-id 0 \
	--fold-count 5 \
	--objective-types voice_cmd \

run-va-asr-experiments-102-cnn2:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN2 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E102/results_102 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 5 \
	--objective-types voice_cmd \


run-va-asr-experiments-102-cnn3:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E102/results_102 \
	--epochs 1000 \
	--gpu-id 0 \
	--fold-count 5 \
	--objective-types voice_cmd \


run-va-asr-experiments-102-cnn3-dropout-0.6:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E102/results_102 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--conv-dropout-probabilities 0.6 \
	--fc-dropout-probabilities 0.6 \


run-va-asr-experiments-102-cnn3-dropout-0.7:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E102/results_102 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--conv-dropout-probabilities 0.7 \
	--fc-dropout-probabilities 0.7 \


run-va-asr-experiments-102-cnn3-spectrogram:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E102/results_102 \
	--epochs 1000 \
	--gpu-id 0 \
	--fold-count 5 \
	--feature-names mel_spectrogram \
	--max-sequence-length 200 \
	--input-channels 128 \
	--objective-types voice_cmd \
	--conv-dropout-probabilities 0.5 0.6 0.7 \
	--fc-dropout-probabilities 0.5 0.6 0.7 \


# Experiemnts E103: Remove french from language set
run-va-asr-experiments-103-cnn3:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E103/results_103 \
	--epochs 1000 \
	--gpu-id 0 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--selected-languages _language_independent maninka pular susu \


run-va-asr-experiments-103-cnn3-dropout-0.7:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E103/results_103 \
	--epochs 1000 \
	--gpu-id 0 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--selected-languages _language_independent maninka pular susu \
	--conv-dropout-probabilities 0.7 \
	--fc-dropout-probabilities 0.7 \


# Experiemnts E104: Remove french and first names. Only keep maninka, pular, susu
run-va-asr-experiments-104-cnn2-dropout-0.5:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN2 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E104/results_104 \
	--epochs 1000 \
	--gpu-id 0 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--selected-languages maninka pular susu \
	--conv-dropout-probabilities 0.5 \
	--fc-dropout-probabilities 0.5 \

run-va-asr-experiments-104-cnn2-spectrogram-dropout-0.5:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN2 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E104/results_104 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 5 \
	--feature-names mel_spectrogram \
	--max-sequence-length 200 \
	--input-channels 128 \
	--objective-types voice_cmd \
	--selected-languages maninka pular susu \
	--conv-dropout-probabilities 0.5 \
	--fc-dropout-probabilities 0.5 \


# Experiments 105. Multi-objective (langid + asr) voice command and language id
run-va-asr-experiments-105-cnn3-voice_simult_obj_dropout-0.6:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E105/results_105 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 5 \
	--objective-types voice_cmd__and__voice_cmd_lng \
	--conv-dropout-probabilities 0.6 \
	--fc-dropout-probabilities 0.6 \



# Experiments 106. Conv Pooling and Aggregate Pooling variants
run-va-asr-experiments-106-cnn3-pool-avg-aggmax-dropout-0.6:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3PoolAvgAggMax \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E106/results_106 \
	--epochs 1000 \
	--gpu-id 0 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--conv-dropout-probabilities 0.6 \
	--fc-dropout-probabilities 0.6 \

run-va-asr-experiments-106-cnn3-pool-max-aggmax-dropout-0.6:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3PoolMaxAggMax \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E106/results_106 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--conv-dropout-probabilities 0.6 \
	--fc-dropout-probabilities 0.6 \



##### Experiments with datasets and wawav2vec refresh2
# 20x lang id
# E209 (see jupyter notebookx)

# 30x ASR Experiments
run-va-asr-experiments-302-cnn3-dropout-0.6:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3 \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E302/results_302 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--conv-dropout-probabilities 0.6 \
	--fc-dropout-probabilities 0.6 \
	--max-sequence-length 300 \


run-va-asr-experiments-306-cnn3-pool-avg-aggmax-dropout-0.6:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3PoolAvgAggMax \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E306/results_306 \
	--epochs 1000 \
	--gpu-id 0 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--conv-dropout-probabilities 0.6 \
	--fc-dropout-probabilities 0.6 \
	--max-sequence-length 300 \

run-va-asr-experiments-306-cnn3-pool-avg-aggmax-spectrogram-dropout-0.6:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3PoolAvgAggMax \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E306/results_306 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--conv-dropout-probabilities 0.6 \
	--fc-dropout-probabilities 0.6 \
	--max-sequence-length 300 \
	--input-channels 128 \
	--feature-names mel_spectrogram \


# Experiemnts E104: Remove french and first names. Only keep maninka, pular, susu
run-va-asr-experiments-307-cnn3-pool-avg-aggmax-guinean-only-dropout-0.6:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3PoolAvgAggMax \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E307/results_307 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 5 \
	--objective-types voice_cmd \
	--selected-languages maninka pular susu \
	--conv-dropout-probabilities 0.6 \
	--fc-dropout-probabilities 0.6 \
	--max-sequence-length 300 \




# Experiments E400: Demo ASR Prototype Models
run-va-asr-experiments-400-demo-prototype:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3PoolMaxAggMax \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E400/results_400 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 1 \
	--train-percent 0.8 \
	--objective-types voice_cmd \
	--conv-dropout-probabilities 0.6 \
	--fc-dropout-probabilities 0.6 \
	--max-sequence-length 300 \
	--input-channels 512 \
	--feature-names retrained-wav2vec_features-c retrained-wav2vec_features-z \
	--persistence-interval 10 \

run-va-asr-experiments-401-demo-prototype:
	python scripts/va_asr/train_va_asr.py \
	--model-name VAASRCNN3PoolAvgAggMax \
	--data-dir $(VA_ASR_DIR) \
	--output-dir notebooks/E401/results_401 \
	--epochs 1000 \
	--gpu-id 1 \
	--fold-count 1 \
	--train-percent 0.8 \
	--objective-types voice_cmd \
	--conv-dropout-probabilities 0.6 \
	--fc-dropout-probabilities 0.6 \
	--max-sequence-length 300 \
	--input-channels 512 \
	--feature-names retrained-wav2vec_features-c retrained-wav2vec_features-z \
	--persistence-interval 10 \


# Data setup for Google Cloud
cloud-nicolingua-data:
	mkdir ../nicolingua-data/
	gsutil rsync -r gs://nicolingua ../nicolingua-data/	
	tar -xf ../nicolingua-data/experiments/nicolingua-0002-va-asr/datasets/gn_va_asr_dataset_2020-08-26_01.tar.gz --directory ../nicolingua-data/experiments/nicolingua-0002-va-asr/datasets/



create-ssl-cert:
	mkdir certificates
	openssl req -nodes -x509 -newkey rsa:4096 -keyout certificates/key.pem -out certificates/cert.pem -days 365

run-web-demo:
	#export FLASK_APP=webdemo.va_asr_demo_web.py  && flask run --host 0.0.0.0 --cert=certificates/cert.pem --key=certificates/key.pem
	gunicorn webdemo.va_asr_demo_web:app --bind 0.0.0.0 --certfile=certificates/cert.pem --keyfile=certificates/key.pem --reload --reload-extra-file=scripts/webdemo --capture-output 
	
run-web-demo-coud:
	gunicorn webdemo.va_asr_demo_web:app --bind 0.0.0.0 --certfile=certificates/cert.pem --keyfile=certificates/key.pem --daemon


setup-gcloud-machine: create-ssl-cert
	sudo apt-get -y update
	sudo apt-get -y install python3.6
	sudo apt-get -y install python3-venv
	sudo apt-get -y install python3.6-dev
	sudo apt-get -y install python3.6-venv
	sudo apt-get -y install build-essential
	sudo apt-get -y install libsndfile1
	sudo apt-get -y install ffmpeg
	gcloud init --project piechlab
	mkdir ../acousticmodels   
	gsutil cp gs://nicolingua/experiments/nicolingua-0003-wa-wav2vec/wav2vec-training-exp-01/checkpoints/checkpoint_best.pt ../acousticmodels/wawav2vec_0003_checkpoint_best.pt     
	gsutil cp gs://nicolingua/experiments/nicolingua-0004-va-asr/E401/results_401/checkpoints/VAASRCNN3PoolAvgAggMax/retrained-wav2vec_features-c_0_checkpoints/0800.pt ../acousticmodels/vaasr_401_0800.pt 
	echo ""  >> scripts/webdemo/config.py
	echo "WAV2VEC_CHECKPOINT_PATH = \"/home/doumbouya_moussa/git/acousticmodels/wawav2vec_0003_checkpoint_best.pt\"" >> scripts/webdemo/config.py
	echo "VAASR_CHECKPOINT_PATH = \"/home/doumbouya_moussa/git/acousticmodels/vaasr_401_0800.pt\""  >> scripts/webdemo/config.py
	sudo fallocate -l 4G /swapfile
	sudo chmod 600 /swapfile 
	sudo mkswap /swapfile 
	sudo swapon /swapfile
	python3.6 -m venv .venv36
	source .venv36/bin/activate
	pip install -U pip wheel
	pip install -r requirements.txt

   


# Public Release Temp Scripts
sync-nicolingua-to-s3:
	aws s3 sync \
		/media/xtrem/data/experiments/nicolingua/ \
		s3://nicolingua/


	
	
