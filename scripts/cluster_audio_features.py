import glob
from argparse import ArgumentParser
from pathlib import Path
import logging
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import h5py
import shutil


def pool_feature_last_seq(raw_features):
    return raw_features[-1]

def load_features(args):
    id_list = []
    features_list = []

    logging.debug("Loading features")
    for path in glob.glob(str(Path(args.features_input_dir) / "*.h5context")):
        with h5py.File(path, 'r') as f:
            features_shape = f['info'][1:].astype(int)
            features = np.array(f['features'][:]).reshape(features_shape)
            features = pool_feature_last_seq(features)

            id_list.append(Path(path).stem)
            features_list.append(features)

            if len(features_list) % 1000 == 0:
                logging.debug("Loaded {} features".format(len(features_list)))
                # break # temporary

    logging.debug("Loaded {} features".format(len(features_list)))
    return id_list, np.array(features_list)


def perform_clustering(features, args):

    kmeans = KMeans(
        n_clusters = args.cluster_count, 
        random_state=args.random_seed
        )

    kmeans = kmeans.fit(features)
    return kmeans.labels_


def generate_output(ids, labels, args):
    assert(len(ids) == len(labels))
    for i in range(len(ids)):
        sample_path = Path(args.samples_input_dir) / f"{ids[i]}.wav" 
        sample_output_dir = Path(args.output_dir) / str(labels[i])
        sample_output_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sample_path, sample_output_dir)
        

def output_t_sne_projection(features, labels, args):
    projection = TSNE(n_components=2).fit_transform(features)
    plt.scatter(projection[:,0], projection[:,1], c=labels, cmap="tab20b")
    fig_filepath = Path(args.output_dir) / "t_sne.png"
    plt.savefig(fig_filepath)


def main(args):
    ids, features = load_features(args)
    
    labels = perform_clustering(features, args)
    output_t_sne_projection(features, labels, args)
    generate_output(ids, labels, args)

    print(len(ids))
    print(features.shape)
    print(len(labels))

    
            


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("samples_input_dir")
    parser.add_argument("features_input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--cluster-count", default=10, type=int)
    parser.add_argument("--random_seed", default=42)

    return parser.parse_args()


def configure_logging(args):
    logging.basicConfig(
        filename = Path(args.output_dir) / f"clustering.log",
        level = logging.DEBUG
        )


if __name__ == '__main__':
    args = parse_arguments()
    Path(args.output_dir).mkdir(exist_ok=True, parents=True)
    configure_logging(args)
    main(args)
