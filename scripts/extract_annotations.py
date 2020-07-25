import os
from pathlib import Path
import mutagen
import csv
from argparse import ArgumentParser



def main(args):
    with open(args.output_file, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["file", "tags"])
        for root, dirs, files in os.walk(args.input_dir):
            counter = 0
            for f in files:
                file_path = Path(root) / Path(f)
                metadata = mutagen.File(file_path)
                
                if metadata:
                    try:
                        #print(file_path)
                        tags = metadata['COMM::eng']
                        counter+=1
                        fn = os.path.basename(file_path)
                        csv_writer.writerow([fn, tags])
                    except KeyError:
                        print("Problematic metadata record. \n\tfile: {}\n\tmetadata: {}".format(file_path, metadata))
            print(counter)


def parse_command_line_args():
    parser = ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_file")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_command_line_args()
    main(args)

