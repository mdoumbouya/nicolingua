import sys
import glob
from argparse import ArgumentParser
from pathlib import Path
import logging
import csv
import hashlib


def transform(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def main(args):
    with open(args.input_file) as f:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(sys.stdout, fieldnames = reader.fieldnames)
        writer.writeheader()
        for r in reader:
            r[args.column_name] = transform(r[args.column_name])
            writer.writerow(r)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--column-name", required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
