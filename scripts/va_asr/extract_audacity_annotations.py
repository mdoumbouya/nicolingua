import sys
import logging
from argparse import ArgumentParser
from pathlib import Path
import re

import csv
import pydub
from pydub.effects import normalize


SEGMENT_FNAME_REGEX = re.compile("(?P<recording_session_id>r\d+)_(?P<speaker_id>s\d+)_(?P<device_id>d\d+)_(?P<language>\w+)__.*__(?P<label_id>\d+_.*)")
KNOWN_LANGUAGES = {'maninka', 'susu', 'pular', 'francais', 'english'}
KNOWN_LABELS = {
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



def process_audio_file(annotation_fname, audio_fname, metadata_dict_writer, args):
    logging.debug(f"processing {audio_fname}...")
    with open(annotation_fname) as f:
        audio_segment = pydub.AudioSegment.from_file(audio_fname)
        reader = csv.DictReader(f, fieldnames = ["start", "end", "label"], delimiter="\t")
        for a in reader:
            marker_start_ms = float(a["start"]) * 1000
            marker_end_ms = float(a["end"]) * 1000

            if(marker_start_ms > len(audio_segment)):
                logging.error(f"Marker {a['label']} starts after the end of audio segment in {segment_fname.stem}")
                continue
            
            if(marker_end_ms > len(audio_segment)):
                logging.error(f"Marker {a['label']} ends after the end of audio segment in {segment_fname.stem}")
                continue

            start_ms = marker_start_ms - args.padding_ms
            end_ms = marker_end_ms + args.padding_ms
            segment = audio_segment[start_ms:end_ms]
            segment = normalize(segment)
            segment = segment.set_frame_rate(args.frame_rate)
            segment = segment.set_channels(args.channels)
            
            segment_fname = Path(args.output_dir) / f"{annotation_fname.stem}__{a['label']}.wav" 

            try:
                m_record = SEGMENT_FNAME_REGEX.match(segment_fname.stem).groupdict()
            except:
                logging.error(f"Could not parse annotated segment name: {segment_fname.stem}")
                continue
            
            if m_record['label_id'] not in KNOWN_LABELS:
                logging.error(f"Unknown label {m_record['label_id']} in {annotation_fname} ")
                continue
                
            if m_record['language'] not in KNOWN_LANGUAGES:
                logging.error(f"Unknown language {m_record['language']} in {annotation_fname} ")
                continue

            m_record["file"] = segment_fname.parts[-1]
            logging.debug(f"writing {segment_fname}...")
            segment.export(segment_fname, format="wav")

            metadata_dict_writer.writerow(m_record)



def main(args):
    with open(Path(args.output_dir) / "metadata.csv", "w") as metadata_f:
        metadata_dict_writer = csv.DictWriter(metadata_f, fieldnames = ["file", "recording_session_id", "speaker_id", "device_id", "language", "label_id"])
        metadata_dict_writer.writeheader()

        for annotation_fname in Path(args.input_dir).rglob("*.txt"):
            # filter out OSX "._" files!
            if annotation_fname.stem.startswith("._"):
                continue
            
            audio_fname = str(annotation_fname).replace(".txt", ".wav")
            if not Path(audio_fname).is_file():
                logging.warn(f"Skipping {annotation_fname}, for which no audio file could be found.")
                continue
            
            try:
                process_audio_file(annotation_fname, audio_fname, metadata_dict_writer, args)
            except:
                logging.exception(f"Unable to process {annotation_fname}")

            


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
    # module_name = sys.modules[__name__].__file__.stem
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
