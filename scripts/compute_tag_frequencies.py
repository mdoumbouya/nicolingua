import os
from pathlib import Path
import mutagen
import csv
from argparse import ArgumentParser
import shutil
import itertools


def main(args):
    tag_set_list = load_tag_set_list(args)
    all_tags = set()
    all_tags = all_tags.union(*tag_set_list)

    with open(args.output_file, "w") as f:
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
                    print("Problematic metadata record. \n\tfile: {}\n\tmetadata: {}".format(file_path, metadata))
    return tag_set_list


def parse_command_line_args():
    parser = ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_file")
    parser.add_argument("--required-tag", default="ct-speech")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_command_line_args()
    main(args)

