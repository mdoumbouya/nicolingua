import sys
import logging
from argparse import ArgumentParser
from pathlib import Path
import re

import csv
import pydub
from pydub.effects import normalize


class AnnotationStats:
    def __init__(self):
        self._s_dict = {}

    def increment(self, lang_id, utt_id):
        s_key = f"{lang_id}_{utt_id}"
        s_lang_key = lang_id
        for k in [s_key, s_lang_key]:
            if k not in self._s_dict:
                self._s_dict[k] = 0

        self._s_dict[s_key] += 1
        self._s_dict[s_lang_key] += 1

    def log_stats(self):
        for k in sorted(list(self._s_dict.keys())):
            logging.info(f"Annotation Stats: {k}\t\t:{self._s_dict[k]}")



AUDACITY_ANNOTATION_FNAME_REGEX = re.compile("(?P<recording_session_id>r\d+)_(?P<speaker_id>s\d+)_(?P<device_id>d\d+)_(?P<language>\w+)__.*")
# KNOWN_LANGUAGES = {'maninka', 'susu', 'pular', 'francais', 'english', '_language_independent'}
KNOWN_LANGUAGES = {'maninka', 'susu', 'pular', 'francais', '_language_independent'} # there are a few clips in english to be removed.
KNOWN_GENDERS = {"M", "F"}
KNOWN_UTTERANCES = {
    "101_wake_word", 

    "201_add_contact", 
    "202_search_contact", 
    "203_update_contact", 
    "204_delete_contact", 
    "205_call_contact", 
    "206_yes", 
    "207_no", 

    "301_zero", 
    "302_one", 
    "303_two", 
    "304_three", 
    "305_four", 
    "306_five", 
    "307_six", 
    "308_seven", 
    "309_eight", 
    "310_nine",

    "401_mom",
    "402_dad",

    "501_fatoumata", 
    "502_mamadou", 
    "503_mariama", 
    "504_mohamed", 
    "505_kadiatou", 
    "506_ibrahima", 
    "507_aissatou", 
    "508_aminata", 
    "509_alpha", 
    "510_thierno", 
    "511_abdoulaye", 
    "512_aboubacar", 
    "513_amadou", 
    "514_fanta", 
    "515_mariame", 
    "516_oumou", 
    "517_ousmane", 
    "518_adama", 
    "519_marie", 
    "520_moussa", 
    "521_aissata", 
    "522_hawa", 
    "523_sekou", 
    "524_hadja", 
    "525_djenabou"
}


def process_audio_file(annotation_fname, audio_fname, metadata_dict_writer, speakers_dict, a_stats, args):
    logging.debug(f"processing {audio_fname}...")
    with open(annotation_fname) as f:
        audio_segment = pydub.AudioSegment.from_file(audio_fname)
        reader = csv.DictReader(f, fieldnames = ["start", "end", "marker"], delimiter="\t")
        for a in reader:
            marker_start_ms = float(a["start"]) * 1000
            marker_end_ms = float(a["end"]) * 1000

            if(marker_start_ms > len(audio_segment)):
                logging.error(f"Marker {a['marker']} starts after the end of audio segment in {annotation_fname.stem}")
                continue
            
            if(marker_end_ms > len(audio_segment)):
                logging.error(f"Marker {a['marker']} ends after the end of audio segment in {annotation_fname.stem}")
                continue

            start_ms = marker_start_ms - args.padding_ms
            end_ms = marker_end_ms + args.padding_ms
            segment = audio_segment[start_ms:end_ms]
            segment = normalize(segment)
            segment = segment.set_frame_rate(args.frame_rate)
            segment = segment.set_channels(args.channels)
            
            try:
                m_record = AUDACITY_ANNOTATION_FNAME_REGEX.match(annotation_fname.stem).groupdict()
            except:
                logging.error(f"Could not parse annotation file name: {annotation_fname.stem}")
                continue

            m_record["utterance_id"] = a['marker']
            segment_fname = Path(args.output_dir) / f"{m_record['recording_session_id']}_{m_record['speaker_id']}_{m_record['device_id']}_{m_record['language']}_{m_record['utterance_id']}.wav"
            
            if m_record['utterance_id'] not in KNOWN_UTTERANCES:
                logging.error(f"Unknown utterance {m_record['utterance_id']} in {annotation_fname}")
                continue
                
            if m_record['language'] not in KNOWN_LANGUAGES:
                logging.error(f"Unknown language {m_record['language']} in {annotation_fname}")
                continue

            if m_record['speaker_id'] not in speakers_dict:
                logging.error(f"Unknown speaker {m_record['speaker_id']} in {annotation_fname}")
                continue

            if speakers_dict[m_record['speaker_id']]['mothertongue'] not in KNOWN_LANGUAGES:
                logging.error(f"Unknown speaker motherthongue language {speakers_dict[m_record['speaker_id']]['mothertongue']} in {annotation_fname}")
                continue
            
            if speakers_dict[m_record['speaker_id']]['gender'] not in KNOWN_GENDERS:
                logging.error(f"Unknown speaker gender {speakers_dict[m_record['speaker_id']]['gender']} in {annotation_fname}")
                continue
            
            if m_record['utterance_id'][0] == '5':
                m_record['language'] = '_language_independent'
            
            m_record['label'] = f"{m_record['utterance_id']}__{m_record['language']}"

            m_record['speaker_mothertongue'] = speakers_dict[m_record['speaker_id']]['mothertongue']
            m_record['speaker_age'] = speakers_dict[m_record['speaker_id']]['age']
            m_record['speaker_gender'] = speakers_dict[m_record['speaker_id']]['gender']
            
            
            m_record["file"] = segment_fname.parts[-1]
            logging.debug(f"writing {segment_fname}...")
            segment.export(segment_fname, format="wav")

            metadata_dict_writer.writerow(m_record)

            a_stats.increment(m_record['language'], m_record['utterance_id'])


def load_speakers(args):
    speakers_fname = Path(args.input_dir) / 'meta' / 'speakers.csv'
    with open(speakers_fname) as f:
        reader = csv.DictReader(f)
        speakers = {r['sid']:r for r in reader}
    return speakers


def main(args):
    speakers_dict = load_speakers(args)

    a_stats = AnnotationStats()

    with open(Path(args.output_dir) / "metadata.csv", "w") as metadata_f:
        metadata_dict_writer = csv.DictWriter(metadata_f, fieldnames = ["file", "recording_session_id", "speaker_id", "device_id", "language", "utterance_id", "label", "speaker_age", "speaker_gender", "speaker_mothertongue"])
        metadata_dict_writer.writeheader()

        for annotation_fname in sorted(Path(args.input_dir).rglob("*.txt")):
            # filter out OSX "._" files!
            if annotation_fname.stem.startswith("._"):
                continue
            
            audio_fname = str(annotation_fname).replace(".txt", ".wav")
            if not Path(audio_fname).is_file():
                logging.warn(f"Skipping {annotation_fname}, for which no audio file could be found.")
                continue
            
            try:
                process_audio_file(annotation_fname, audio_fname, metadata_dict_writer, speakers_dict, a_stats, args)
            except:
                logging.exception(f"Unable to process {annotation_fname}")

    a_stats.log_stats()


def parse_arguments():
    parser = ArgumentParser(
        description="""Finds audacity label .txt files and matching .wav files."""
        """Creates an output audio segment file for each label for each annotated .wav file"""
    )
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--padding-ms", default=100, type=int, help="How many milliseconds to pad (before and after) the annotated segments")
    parser.add_argument("--frame-rate", default=16000)
    parser.add_argument("--channels", default=1)

    return parser.parse_args()


def configure_logging(args):
    module_name = Path(__file__).stem
    
    logging.basicConfig(
        filename = Path(args.output_dir) / f"{module_name}.log",
        level = logging.DEBUG
        )

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.ERROR)
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)


if __name__ == '__main__':
    args = parse_arguments()
    Path(args.output_dir).mkdir(exist_ok=True, parents=True)
    configure_logging(args)
    main(args)
