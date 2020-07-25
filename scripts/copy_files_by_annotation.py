import os
from pathlib import Path
import mutagen
import csv
from argparse import ArgumentParser
import shutil



def main(args):
    for root, dirs, files in os.walk(args.input_dir):
        for f in files:
            file_path = Path(root) / Path(f)
            metadata = mutagen.File(file_path)
            
            if metadata:
                try:
                    #print(file_path)
                    tags = str(metadata['COMM::eng'])
                    tags = [t.strip() for t in tags.split(";")]
                    if args.tag in tags:
                        shutil.copy2(file_path, args.output_dir)
                    
                except KeyError:
                    print("Problematic metadata record. \n\tfile: {}\n\tmetadata: {}".format(file_path, metadata))


def parse_command_line_args():
    parser = ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--tag", required=True)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_command_line_args()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    main(args)

