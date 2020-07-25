import os, sys
from pathlib import Path
import mutagen
import csv
from argparse import ArgumentParser
import shutil
import itertools
import logging



def main_specific_tags(args):
    tag_set_list = load_tag_set_list(args)
    tag_set = set(args.tags)
    count = len([ts for ts in tag_set_list if tag_set.issubset(ts)])
    print(f"{tag_set} {count}")


def main_all_tags(args):
    tag_set_list = load_tag_set_list(args)
    all_tags = set()
    all_tags = all_tags.union(*tag_set_list)

    if args.output_file:
        f = open(args.output_file, "w")
    else:
        f = sys.stdout

    writer = csv.writer(f)

    writer.writerow(['cardinality', 'subset', 'count'])

    for subset_cardinality in range(1, 6):
        subset_counts = []
        for tag_subset in itertools.combinations(all_tags, subset_cardinality):
            count = compute_subset_frequency(tag_set_list, set(tag_subset))
            
            subset_counts.append({
                "subset": tag_subset,
                "cardinality": subset_cardinality,
                "count": count
            })

        subset_counts = [e for e in subset_counts if e['count']>0]
        subset_counts = sorted(subset_counts, key=lambda e: e['count'], reverse=True)

        for e in subset_counts:
            writer.writerow([
                e['cardinality'],
                ", ".join(sorted(e['subset'])),
                e['count']
            ])

    if args.output_file:
        f.close()

def compute_subset_frequency(tag_set_list, tag_subset):
    count = 0
    for tag_set in tag_set_list:
        if tag_subset.issubset(tag_set):
            count += 1
    return count

def load_tag_set_list(args):
    tag_set_list = []
    for root, dirs, files in os.walk(args.input_dir):
        for f in files:
            file_path = Path(root) / Path(f)
            metadata = mutagen.File(file_path)
            
            if metadata:
                try:
                    #print(file_path)
                    tags = str(metadata['COMM::eng'])
                    tag_set = set([t.strip() for t in tags.split(";")])
                    tag_set_list.append(tag_set)
                    
                except KeyError:
                    logging.warn(
                        "Problematic metadata record. \n\tfile: {}\n\tmetadata: {}".format(file_path, metadata)
                    )
    return tag_set_list


def parse_command_line_args():
    parser = ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("--output-file", required=False)
    parser.add_argument("--tags", nargs="+")

    return parser.parse_args()


def configure_logging(args):
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


if __name__ == "__main__":
    args = parse_command_line_args()
    configure_logging(args)
    if args.tags:
        main_specific_tags(args)
    else:
        main_all_tags(args)

