import os
from pathlib import Path
import mutagen
import csv
from argparse import ArgumentParser
import shutil
import logging


def main(args):
    output_metadata_file_path = Path(args.output_dir) / "metadata.csv"
    if args.output_audio_files:
        output_audio_dir = Path(args.output_dir) / "audio_samples"
        output_audio_dir.mkdir(parents=True, exist_ok=True)
    

    with open(output_metadata_file_path, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["file", "tags"])
        for root, dirs, files in os.walk(args.input_dir):
            counter = 0
            for f in files:
                audio_file_path = Path(root) / Path(f)
                metadata = mutagen.File(audio_file_path)
                
                if metadata:
                    try:
                        tags = metadata['COMM::eng']
                        counter+=1
                        fn = os.path.basename(audio_file_path)
                        csv_writer.writerow([fn, tags])

                        if args.output_audio_files:
                            shutil.copy(audio_file_path, output_audio_dir)

                    except KeyError:
                        logging.exception("Problematic metadata record. \n\tfile: {}\n\tmetadata: {}".format(audio_file_path, metadata))

            logging.info(f"Processed {counter} annotated audio clips")



def configure_logging(args):
    module_name = Path(__file__).stem
        
    logging.basicConfig(
        filename = Path(args.output_dir) / f"{module_name}.log",
        level = logging.DEBUG
        )


def parse_command_line_args():
    parser = ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--output-audio-files", default=False, action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command_line_args()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    configure_logging(args)
    logging.info(f"Command line arguments: {args}")
    main(args)