import os
import pydub
import uuid
from pathlib import Path
import logging
import math
import random

from argparse import ArgumentParser
from pydub.effects import normalize
import csv



class SamplingLogger:
    def __init__(self, file_path):
        self.log_file = open(file_path, 'w')
        self.csv_writer = csv.writer(self.log_file)
        
    def __enter__(self):
        self.csv_writer.writerow(['source_file_path', 'segment', 'start_time', 'duration'])
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.log_file.flush()
        self.log_file.close()

    def add_entry(self, source_file_path, segment, start_time, duration):
        self.csv_writer.writerow([source_file_path, segment, start_time, duration])

    



def sample_file(file_path, sample_logger, args):
    sound = pydub.AudioSegment.from_file(file_path)
    args.sampling_ratio
    args.max_sample_length_ms

    l = len(sound) / 1000 / 60
    sample_count = math.ceil(len(sound) * args.sampling_ratio / args.max_sample_length_ms)
    sample_count = max(1, sample_count)

    relative_source_path = Path(file_path).relative_to(Path(args.input_dir))

    for sample_index in range(sample_count):
        sample_id = str(uuid.uuid4())

        start_time = random.randint(0, len(sound) - args.max_sample_length_ms - 1)
        start_time = max(0, start_time)

        cropped_sound = sound[start_time: start_time + args.max_sample_length_ms]
        cropped_sound = normalize(cropped_sound)
        cropped_sound = cropped_sound.set_frame_rate(args.frame_rate)
        cropped_sound = cropped_sound.set_channels(args.channels)
        segment_filename = f"{sample_id}.wav"
        cropped_sound.export(Path(args.output_dir) / segment_filename, format="wav")

        duration = len(cropped_sound)
        sample_logger.add_entry(relative_source_path, segment_filename, start_time, duration)

    logging.debug(f"sampling {file_path} {l} minutes. {sample_count} samples")


def convert_file(input_path, output_path):
    try:
        print(f"converting {input_path} to {output_path}")    
        sound = pydub.AudioSegment.from_mp3(input_path)
        sound.export(output_path, format="wav")
    except:
        print("An error occured.")


def main(args):
    output_path = Path(args.output_dir)
    if not output_path.exists():
        output_path.mkdir(parents=True)

    with SamplingLogger(Path(args.output_dir) / "samples.csv") as sample_logger:
        for path, subdirs, files in os.walk(args.input_dir):
            for file_name in files:
                file_path = os.path.join(path, file_name)
                file_ext = file_path.split('.')[-1].lower()
                if file_ext in {'mp3', 'wav'}:
                    try:
                        sample_file(file_path, sample_logger, args)
                    except:
                        logging.error(f"An error occured while sampling {file_path}")


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--sampling-ratio", default=0.1)
    parser.add_argument("--max-sample-length-ms", default=30000)
    parser.add_argument("--frame-rate", default=16000)
    parser.add_argument("--channels", default=1)
    return parser.parse_args()


def configure_logging(args):
    logging.basicConfig(
        filename = Path(args.output_dir) / f"sampling.log",
        level = logging.DEBUG
        )


if __name__ == '__main__':
    args = parse_arguments()
    Path(args.output_dir).mkdir(exist_ok=True, parents=True)
    configure_logging(args)
    main(args)


# Keywords associated with mostly musical content: "MUSIQUE" "FOLKLORES" "RETRO" "PRETETE"
# cat /media/xtrem/data/tmp-waves/samples.csv |grep -v -e "MUSIQUE" -e "FOLKLORES" -e "RETRO" -e "PRETETE" | shuf | head | awk  '{FS=","; print $2}'
