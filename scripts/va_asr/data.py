import logging
from pathlib import Path
import itertools
import csv
import numpy as np
import h5py
import torch
from torch.utils.data import TensorDataset, DataLoader
import torchaudio


def load_metadata(args):
    annotations_path = Path(args.data_dir) / "annotated_segments" / "metadata.csv"
    with open(annotations_path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r['language'] in set(args.selected_languages):
                r['spoken_in_mothertongue'] = r['speaker_mothertongue'] == r['language']

                yield r



def count_by_attribute(records, attribute_names):
    attribute_name_instances = {}
    for attribute_name in attribute_names:
        attribute_name_instances[attribute_name] = {r[attribute_name] for r in records}
        
    l = [attribute_name_instances[attribute_name] for attribute_name in attribute_names]
    
    
    
    for attribute_values in sorted(itertools.product(*l)):
        
        def record_match(r):
            for i in range(len(attribute_names)):
                if r[attribute_names[i]] != attribute_values[i]:
                    return False
            return True
            
        record_instances = [r for r in records if record_match(r)]
        count = len(record_instances)
        
        yield (attribute_values, count)

def log_data_stats(metadata_records):
    logging.info(
        "RECORDS BY DEVICE\n" +
        "\n".join([f"\t{r}" for r in sorted(count_by_attribute(metadata_records, ['device_id']))])
    )

    logging.info(
        "RECORDS BY LANGUAGE\n" +
        "\n".join([f"\t{r}" for r in sorted(count_by_attribute(metadata_records, ['language']))])
    )
    
    logging.info(
        "RECORDS BY GENDER\n" +
        "\n".join([f"\t{r}" for r in sorted(count_by_attribute(metadata_records, ['speaker_gender']))])
    )
    
    logging.info(
        "RECORDS BY AGE\n" +
        "\n".join([f"\t{r}" for r in sorted(count_by_attribute(metadata_records, ['speaker_age']))])
    )

    logging.info(
        "RECORDS BY SPEAKER\n" +
        "\n".join([f"\t{r}" for r in sorted(count_by_attribute(metadata_records, ['speaker_id']))])
    )
    
    logging.info(
        "RECORDS BY SPEAKER BY LANGUAGE\n" +
        "\n".join([f"\t{r}" for r in sorted(count_by_attribute(metadata_records, ['speaker_id', 'language']))])
    )

    logging.info(
        "RECORDS BY SPOKEN IN MOTHERTONGUE\n" +
        "\n".join([f"\t{r}" for r in sorted(count_by_attribute(metadata_records, ['spoken_in_mothertongue']))])
    )

    

    logging.info(
        "RECORDS BY SPEAKER BY LABEL\n" +
        "\n".join([f"\t{r}" for r in sorted(count_by_attribute(metadata_records, ['label']))])
    )


def generate_class_dictionaries(args):
    metadata_records = list(load_metadata(args))
    log_data_stats(metadata_records)

    # voice commands
    voice_cmd_class_names = sorted({r['label'] for r in metadata_records})
    voice_cmd_class_count = len(voice_cmd_class_names)
    voice_cmd_class_id_by_name = {c:i for i, c in enumerate(voice_cmd_class_names)}

    
    str_classes = "\n".join([f"{v:4}: {k}" for k,v in voice_cmd_class_id_by_name.items()])   
    logging.info(f"Classes - Voice Commands:\n{str_classes}")

    # VOICE COMMAND LANGUAGES
    voice_cmd_lng_class_names = sorted({r['language'] for r in metadata_records})
    voice_cmd_lng_class_count = len(voice_cmd_lng_class_names)
    voice_cmd_lng_class_id_by_name = {c:i for i, c in enumerate(voice_cmd_lng_class_names)}

    
    str_classes = "\n".join([f"{v:3}: {k}" for k,v in voice_cmd_lng_class_id_by_name.items()])
    logging.info(f"Classes - Voice Command Languages:\n{str_classes}")

    # SPEAKER MOTHERTONGUE
    spkr_mothertongue_class_names = sorted({r['speaker_mothertongue'] for r in metadata_records})
    spkr_mothertongue_class_count = len(spkr_mothertongue_class_names)
    spkr_mothertongue_class_id_by_name = {c:i for i,c in enumerate(spkr_mothertongue_class_names)}

    str_classes = "\n".join([f"{v:3}: {k}" for k,v in spkr_mothertongue_class_id_by_name.items()])
    logging.info(f"Classes - Speaker Mothertongues:\n{str_classes}")
    
    # SPEAKER GENDER
    spkr_gender_class_names = sorted({r['speaker_gender'] for r in metadata_records})
    spkr_gender_class_count = len(spkr_gender_class_names)
    spkr_gender_class_id_by_name = {c:i for i, c in enumerate(spkr_gender_class_names)}

    logging.info("Classes - Speaker Gender")
    _ = [logging.info(f"{v:3}: {k}") for k,v in spkr_gender_class_id_by_name.items()]

    return (
        voice_cmd_class_id_by_name, 
        voice_cmd_lng_class_id_by_name, 
        spkr_mothertongue_class_id_by_name, 
        spkr_gender_class_id_by_name
    )



def generate_train_test_records_per_fold(args):
    all_records = list(load_metadata(args))
    
    records_per_fold = {}
    
    all_speaker_languages = sorted({(r['speaker_id'], r['language']) for r in all_records})

    sl_count = len(all_speaker_languages)
    all_sl_indices = range(sl_count)
    train_sl_count = int(np.ceil(sl_count*args.train_percent))
    test_sl_count = sl_count - train_sl_count

    for fold_index in range(args.fold_count):
        fold_rsampler = np.random.RandomState(seed=fold_index)

        train_sl_index_set = set(fold_rsampler.choice(all_sl_indices, train_sl_count, replace=False))
        train_sl_set = {all_speaker_languages[i] for i in train_sl_index_set}

        test_sl_index_set = set(all_sl_indices).difference(train_sl_index_set)
        test_sl_set = {all_speaker_languages[i] for i in test_sl_index_set}

        train_records = [r for r in all_records if (r['speaker_id'], r['language']) in train_sl_set]
        test_records = [r for r in all_records if (r['speaker_id'], r['language']) in test_sl_set]
        
        
        records_per_fold[fold_index] = {
            "train_records": train_records,
            "test_records": test_records
        }
    
    return records_per_fold


def load_features(records, feature_name, args):
    if feature_name == 'mel_spectrogram':
        return load_mel_spectrogram_features(records, args)
    return load_saved_features(records, feature_name, args)


def load_saved_features(records, feature_name, args):
    features_list = []
    features_input_dir = Path(args.data_dir) / feature_name

    for r in records:
        feature_file_name = r['file'].replace(".wav", ".h5context")
        feature_path = Path(features_input_dir) / feature_file_name
        with h5py.File(feature_path, 'r') as f:
            features_shape = f['info'][1:].astype(int)
            features = np.array(f['features'][:]).reshape(features_shape)
            
            padded_features = np.zeros((args.max_sequence_length, 512), dtype=features.dtype)
            padded_features[:features_shape[0], :] = features
            
            features_list.append(padded_features)
    return features_list


def load_mel_spectrogram_features(records, args):
    audio_base_dir = Path(args.data_dir) / "annotated_segments"

    features_list = []
    for r in records:
        audio_file_path = audio_base_dir / r['file']

        waveform, sample_rate = torchaudio.load(audio_file_path)
        specgram = torchaudio.transforms.MelSpectrogram()(waveform).numpy()
        
        assert specgram.shape[0] == 1
        specgram = specgram[0, :, :].T
        
        padded_features = np.zeros((args.max_sequence_length, specgram.shape[1]), dtype=specgram.dtype)
        padded_features[:specgram.shape[0],:] = specgram
        

        features_list.append(padded_features)

    return features_list





def get_bias_categories(metadata_records):
    bias_category_fields = [
        "device_id"
        ,"language"
        ,"speaker_gender"
        ,"speaker_mothertongue"
        ,"spoken_in_mothertongue"
    ]

    bias_categories = {}
    for c in bias_category_fields:
        bias_categories[c] = sorted({r[c] for r in metadata_records})

    return bias_categories


def get_bias_category_labels(records):
    bias_category_labels = {}
    
    bias_categories = get_bias_categories(records)

    for cat in bias_categories:
        for cat_val in bias_categories[cat]:
            bias_category_labels[f"{cat}__{cat_val}"] = [1 if r[cat]==cat_val else 0 for r in records]
            
    return bias_category_labels


def get_data_for_fold(fold_id, feature_name, args):
    (
        voice_cmd_class_id_by_name, 
        voice_cmd_lng_class_id_by_name, 
        spkr_mothertongue_class_id_by_name, 
        spkr_gender_class_id_by_name
    ) = generate_class_dictionaries(args)

    records_per_fold = generate_train_test_records_per_fold(args)
    
    train_records = records_per_fold[fold_id]["train_records"]
    test_records = records_per_fold[fold_id]["test_records"]
    
    train_features = load_features(train_records, feature_name, args)
    test_features = load_features(test_records, feature_name, args)
    
    train_x = np.array(train_features)
    test_x = np.array(test_features)
    
    train_y = {}
    train_y['voice_cmd'] = np.array([voice_cmd_class_id_by_name[r['label']] for r in train_records])
    train_y['voice_cmd_lng'] = np.array([voice_cmd_lng_class_id_by_name[r['language']] for r in train_records])
    train_y['spkr_mothertongue'] = np.array([spkr_mothertongue_class_id_by_name[r['speaker_mothertongue']] for r in train_records])
    train_y['spkr_gender'] = np.array([spkr_gender_class_id_by_name[r['speaker_gender']] for r in train_records])
    
    

    
    test_y = {}
    test_y['voice_cmd'] = np.array([voice_cmd_class_id_by_name[r['label']] for r in test_records])
    test_y['voice_cmd_lng'] = np.array([voice_cmd_lng_class_id_by_name[r['language']] for r in test_records])
    test_y['spkr_mothertongue'] = np.array([spkr_mothertongue_class_id_by_name[r['speaker_mothertongue']] for r in test_records])
    test_y['spkr_gender'] = np.array([spkr_gender_class_id_by_name[r['speaker_gender']] for r in test_records])

    train_bias_category_labels = get_bias_category_labels(train_records)
    test_bias_category_labels = get_bias_category_labels(test_records)
    
    return train_x, train_y, test_x, test_y, train_bias_category_labels, test_bias_category_labels

    
def get_loaders_for_fold(fold_id, feature_name, batch_size, args):
    
    train_x, train_y, test_x, test_y, train_bias_category_labels, test_bias_category_labels = \
        get_data_for_fold(fold_id, feature_name, args)
    
    train_dataset = TensorDataset(
        torch.tensor(train_x), 
        torch.tensor(train_y['voice_cmd']),
        torch.tensor(train_y['voice_cmd_lng']),
        # torch.tensor(train_y['spkr_mothertongue']),
        # torch.tensor(train_y['spkr_gender']),
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size)

    test_dataset = TensorDataset(
        torch.tensor(test_x), 
        torch.tensor(test_y['voice_cmd']),
        torch.tensor(test_y['voice_cmd_lng']),
        # torch.tensor(test_y['spkr_mothertongue']),
        # torch.tensor(test_y['spkr_gender']),
    )

    test_loader = DataLoader(test_dataset, batch_size=batch_size)
    
    return train_loader, test_loader, train_bias_category_labels, test_bias_category_labels


def get_asr_class_dict():
    return {
        0: "101_wake_word__francais",
        1: "101_wake_word__maninka",
        2: "101_wake_word__pular",
        3: "101_wake_word__susu",
        4: "201_add_contact__francais",
        5: "201_add_contact__maninka",
        6: "201_add_contact__pular",
        7: "201_add_contact__susu",
        8: "202_search_contact__francais",
        9: "202_search_contact__maninka",
        10: "202_search_contact__pular",
        11: "202_search_contact__susu",
        12: "203_update_contact__francais",
        13: "203_update_contact__maninka",
        14: "203_update_contact__pular",
        15: "203_update_contact__susu",
        16: "204_delete_contact__francais",
        17: "204_delete_contact__maninka",
        18: "204_delete_contact__pular",
        19: "204_delete_contact__susu",
        20: "205_call_contact__francais",
        21: "205_call_contact__maninka",
        22: "205_call_contact__pular",
        23: "205_call_contact__susu",
        24: "206_yes__francais",
        25: "206_yes__maninka",
        26: "206_yes__pular",
        27: "206_yes__susu",
        28: "207_no__francais",
        29: "207_no__maninka",
        30: "207_no__pular",
        31: "207_no__susu",
        32: "301_zero__francais",
        33: "301_zero__maninka",
        34: "301_zero__pular",
        35: "301_zero__susu",
        36: "302_one__francais",
        37: "302_one__maninka",
        38: "302_one__pular",
        39: "302_one__susu",
        40: "303_two__francais",
        41: "303_two__maninka",
        42: "303_two__pular",
        43: "303_two__susu",
        44: "304_three__francais",
        45: "304_three__maninka",
        46: "304_three__pular",
        47: "304_three__susu",
        48: "305_four__francais",
        49: "305_four__maninka",
        50: "305_four__pular",
        51: "305_four__susu",
        52: "306_five__francais",
        53: "306_five__maninka",
        54: "306_five__pular",
        55: "306_five__susu",
        56: "307_six__francais",
        57: "307_six__maninka",
        58: "307_six__pular",
        59: "307_six__susu",
        60: "308_seven__francais",
        61: "308_seven__maninka",
        62: "308_seven__pular",
        63: "308_seven__susu",
        64: "309_eight__francais",
        65: "309_eight__maninka",
        66: "309_eight__pular",
        67: "309_eight__susu",
        68: "310_nine__francais",
        69: "310_nine__maninka",
        70: "310_nine__pular",
        71: "310_nine__susu",
        72: "401_mom__francais",
        73: "401_mom__maninka",
        74: "401_mom__pular",
        75: "401_mom__susu",
        76: "402_dad__francais",
        77: "402_dad__maninka",
        78: "402_dad__pular",
        79: "402_dad__susu",
        80: "501_fatoumata___language_independent",
        81: "502_mamadou___language_independent",
        82: "503_mariama___language_independent",
        83: "504_mohamed___language_independent",
        84: "505_kadiatou___language_independent",
        85: "506_ibrahima___language_independent",
        86: "507_aissatou___language_independent",
        87: "508_aminata___language_independent",
        88: "509_alpha___language_independent",
        89: "510_thierno___language_independent",
        90: "511_abdoulaye___language_independent",
        91: "512_aboubacar___language_independent",
        92: "513_amadou___language_independent",
        93: "514_fanta___language_independent",
        94: "515_mariame___language_independent",
        95: "516_oumou___language_independent",
        96: "517_ousmane___language_independent",
        97: "518_adama___language_independent",
        98: "519_marie___language_independent",
        99: "520_moussa___language_independent",
        100: "521_aissata___language_independent",
        101: "522_hawa___language_independent",
        102: "523_sekou___language_independent",
        103: "524_hadja___language_independent",
        104: "525_djenabou___language_independent",
    }