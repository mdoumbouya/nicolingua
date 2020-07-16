import os
import pydub
import uuid
from pathlib import Path
import logging
import math
import random
from multiprocessing import Pool
import functools
from functools import partial

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


def sample_file(file_path, args):
    try:
        sound = pydub.AudioSegment.from_file(file_path)
        args.sampling_ratio
        args.max_sample_length_ms

        l = len(sound) / 1000 / 60
        sample_count = math.ceil(len(sound) * args.sampling_ratio / args.max_sample_length_ms)
        sample_count = max(1, sample_count)

        relative_source_path = Path(file_path).relative_to(Path(args.input_dir))

        sampling_report = []

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

            sampling_report.append({
                "source": relative_source_path,
                "segment": segment_filename,
                "start_time": start_time,
                "duration": duration
            })

        logging.debug(f"sampled {file_path} {l} minutes. {sample_count} samples")

        return sampling_report
    except:
        logging.error(f"An error occured while sampling {file_path}")
        return []


def main(args):
    output_path = Path(args.output_dir)
    if not output_path.exists():
        output_path.mkdir(parents=True)

    # collect input files to sample
    input_files = []
    for path, subdirs, files in os.walk(args.input_dir):
        for file_name in files:
            file_path = os.path.join(path, file_name)
            file_ext = file_path.split('.')[-1].lower()
            if file_ext in {'mp3', 'wav'}:
                input_files.append(file_path)

    # use multiprocessing to sample the files in parallel 
    with SamplingLogger(Path(args.output_dir) / "samples.csv") as sample_logger:
        with Pool(args.worker_count) as p:
            threaded_routine = functools.partial(sample_file, args=args)
            sampling_reports = p.map(threaded_routine, input_files)

            # write sampling reports
            for report in sampling_reports:
                for segment in report:
                    sample_logger.add_entry(
                        segment["source"], 
                        segment["segment"], 
                        segment["start_time"], 
                        segment["duration"]
                    )


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--sampling-ratio", default=0.1)
    parser.add_argument("--max-sample-length-ms", default=30000)
    parser.add_argument("--frame-rate", default=16000)
    parser.add_argument("--channels", default=1)
    parser.add_argument("--worker-count", default=16, type=int)
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
