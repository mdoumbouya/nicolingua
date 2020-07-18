DATA_DIR = /media/xtrem/data/datasets/radio_data
BUILD_DIR = /media/xtrem/data/experiments/nicolingua-0001-language-id
export CUDA_VISIBLE_DEVICES=0,1

.PHONY: samples features-c features-z clean-samples clean-features-c clean-features-z count-files

samples: $(BUILD_DIR)/audio_samples

samples-annotation-space: $(BUILD_DIR)/audio_samples_annotation_space

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


$(BUILD_DIR)/audio_samples_annotation_space:
	# split files into mostly music and mostly speech


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