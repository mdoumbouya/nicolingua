import os
import datetime
import glob
from argparse import ArgumentParser
from pathlib import Path
import logging
import csv
import itertools

import numpy as np
import sklearn
import sklearn.metrics

import torch
import torch.nn as nn
import torch.optim as optim
from pytorch_model_summary import summary

import models
from results import results_exist, save_results
from data import get_loaders_for_fold
from utils import get_torch_device, get_predictions_for_logits






def main(args):
    run_trials(args)
    




def run_trials(args):
    trial_params = generate_trial_params(args)
    
    for p in trial_params:
        trial_name = f"{args.model_name}__" + "__".join([f"{k}_{p[k]}" for k in sorted(p.keys())])
        logging.info(f"running trial: {trial_name}")
        
        if results_exist(trial_name, args):
            logging.info(f"skipping {trial_name}")
            continue
        
        model_class = getattr(models, args.model_name)
        model = model_class(
            conv_pooling_type = 'avg', 
            conv_dropout_p = p['c_dropout_p'],
            fc_dropout_p = p['f_dropout_p'],
            voice_cmd_neuron_count = 105, 
            voice_cmd_lng_neuron_count = 5,
            objective_type = p['obj']
        ).to(get_torch_device(args))

        epochs_results = train_on_fold(
            model, 
            fold_id = p['fold_id'], 
            feature_name = p['feature'], 
            objective_type = p['obj'], 
            batch_size = args.batch_size, 
            epochs = args.epochs
        )

        # results for only one fold
        trial_results = {
            'fold_index': p['fold_id'],
            'feature_name': p['feature'],
            'epochs': epochs_results
        }
        
        
        save_results(trial_name, trial_results, args)
        # write_epoch_test_logits(model_name, all_folds_results)

        del model


def generate_trial_params(args):
    trial_params = [
        {
            "fold_id": t[0],
            "c_dropout_p": t[1],
            "f_dropout_p": t[2],
            "feature": t[3],
            "obj": t[4],
        }
        for t in itertools.product(
            range(args.fold_count),
            args.conv_dropout_probabilities,
            args.fc_dropout_probabilities,
            args.feature_names, 
            args.objective_types
        )
    ]

    logging.info("Generated trials: ")
    _ = [logging.info(p) for p in trial_params]

    return trial_params



def train(model, optimizer, criterion, objective_type, train_loader):
    model.train()
    device=get_torch_device(args)
    train_loss = 0

    for batch_idx, (x, y_voice_cmd, y_voice_cmd_lng) in enumerate(train_loader):
        x = x.to(device)
        y_voice_cmd = y_voice_cmd.to(device)
        y_voice_cmd_lng = y_voice_cmd_lng.to(device)

        optimizer.zero_grad()
        outputs = model(x)

        if objective_type == 'voice_cmd':
            logits_voice_cmd = outputs
            loss = criterion(logits_voice_cmd, y_voice_cmd)
        elif objective_type == 'voice_cmd__and__voice_cmd_lng':
            logits_voice_cmd, logits_voice_cmd_lng = outputs    
            loss = (criterion(logits_voice_cmd, y_voice_cmd) + criterion(logits_voice_cmd_lng, y_voice_cmd_lng)) / 2
            
        else:
            raise ValueError(f"Unknown objective type: {objective_type}")

        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        

def test(model, criterion, objective_type, loader, bias_category_labels):
    device = get_torch_device(args)

    model.eval()
    accumulated_loss = 0

    pred_classes = []
    true_classes = []

    pred_classes_lng = []
    true_classes_lng = []

    for batch_idx, (x, y_voice_cmd, y_voice_cmd_lng) in enumerate(loader):
        x = x.to(device)
        y_voice_cmd = y_voice_cmd.to(device)
        y_voice_cmd_lng = y_voice_cmd_lng.to(device)

        outputs = model(x)

        if objective_type == 'voice_cmd':
            logits_voice_cmd = outputs

            pred_classes.extend(
                get_predictions_for_logits(logits_voice_cmd).cpu().numpy()
            )
            true_classes.extend(y_voice_cmd.cpu().numpy())

            loss = criterion(logits_voice_cmd, y_voice_cmd)
        elif objective_type == 'voice_cmd__and__voice_cmd_lng':
            logits_voice_cmd, logits_voice_cmd_lng = outputs
            pred_classes.extend(
                get_predictions_for_logits(logits_voice_cmd).cpu().numpy()
            )
            true_classes.extend(y_voice_cmd.cpu().numpy())

            pred_classes_lng.extend(
                get_predictions_for_logits(logits_voice_cmd_lng).cpu().numpy()
            )
            true_classes_lng.extend(y_voice_cmd_lng.cpu().numpy())

            loss = (criterion(logits_voice_cmd, y_voice_cmd) + criterion(logits_voice_cmd_lng, y_voice_cmd_lng)) /2
        else:
            raise ValueError(f"Unknown objective type: {objective_type}")

        accumulated_loss += loss.item()

    n = len(true_classes)

    average_loss = accumulated_loss/n
    
    acc = sklearn.metrics.accuracy_score(true_classes, pred_classes)
    acc_by_bais_category = {
        category: sklearn.metrics.accuracy_score(true_classes, pred_classes, sample_weight=sw)
        for category, sw in bias_category_labels.items()
    }
    
    
    if objective_type == 'voice_cmd__and__voice_cmd_lng':
        acc_lng = sklearn.metrics.accuracy_score(true_classes_lng, pred_classes_lng)
        acc_by_bais_category_lng = {
            category: sklearn.metrics.accuracy_score(true_classes_lng, pred_classes_lng, sample_weight=sw)
            for category, sw in bias_category_labels.items()
        }
    else:
        acc_lng = -1
        acc_by_bais_category_lng = {
            category: -1
            for category, sw in bias_category_labels.items()
        }
        
    return n, average_loss, acc, acc_by_bais_category, acc_lng, acc_by_bais_category_lng
      
        
def train_on_fold(model, fold_id, feature_name, objective_type, batch_size, epochs):
    torch.manual_seed(0)
    device = get_torch_device(args)
    results = {}
    
    train_loader, test_loader, train_bias_category_labels, test_bias_category_labels = get_loaders_for_fold(fold_id, feature_name, batch_size, args)

    logging.info("Model Summary :\n" + summary(model, torch.zeros((10, args.max_sequence_length, 512)).to(device), show_input=False))
    logging.info(f"train_n: {len(train_loader.dataset)}")
    logging.info(f"test_n: {len(test_loader.dataset)}")

    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)
    criterion = nn.CrossEntropyLoss(reduction='sum')

    for epoch in range(1, epochs+1):
        
        # train on training set
        train(model, optimizer, criterion, objective_type, train_loader)
        
        # test on training set
        train_n, train_average_loss, train_acc, train_acc_by_bais_category, train_acc_lng, train_acc_by_bais_category_lng = \
            test(model, criterion, objective_type, train_loader, train_bias_category_labels)
        
        # test on test set
        test_n, test_average_loss, test_acc, test_acc_by_bais_category, test_acc_lng, test_acc_by_bais_category_lng = \
            test(model, criterion, objective_type, test_loader, test_bias_category_labels)
        

        if epoch%10==0:
            logging.info(f"Epoch: {epoch}. Train Loss: {train_average_loss:0.4}. Test Loss: {test_average_loss:0.4}. Train Acc: {train_acc:0.4}. Test Acc:{test_acc:0.4}")
        else:
            logging.debug(f"Epoch: {epoch}. Train Loss: {train_average_loss:0.4}. Test Loss: {test_average_loss:0.4}. Train Acc: {train_acc:0.4}. Test Acc:{test_acc:0.4}")
        
         
        results[epoch] = {
            'epoch': epoch,
            
            'train_n': train_n,
            'train_loss': train_average_loss,
            'train_acc': train_acc,
            'train_acc_lng': train_acc_lng,
            
            'test_n': test_n,
            'test_loss': test_average_loss,
            'test_acc': test_acc,
            'test_acc_lng': test_acc_lng
        }
        
        for c in train_acc_by_bais_category:
            results[epoch][f"train_acc_{c}"] = train_acc_by_bais_category[c]
            results[epoch][f"train_n_{c}"] = int(np.sum(train_bias_category_labels[c]))
            
        for c in train_acc_by_bais_category_lng:
            results[epoch][f"train_acc_lng_{c}"] = train_acc_by_bais_category_lng[c]
            
            
        for c in test_acc_by_bais_category:
            results[epoch][f"test_acc_{c}"] = test_acc_by_bais_category[c]
            results[epoch][f"test_n_{c}"] = int(np.sum(test_bias_category_labels[c]))

        for c in test_acc_by_bais_category_lng:
            results[epoch][f"test_acc_lng_{c}"] = test_acc_by_bais_category_lng[c]
            

    return results



def parse_arguments():
    # Define default parameter values
    DEFAULT_FEATURE_NAMES = [
        "wav2vec_features-c", 
        "wav2vec_features-z", 
        "retrained-wav2vec_features-c", 
        "retrained-wav2vec_features-z"
    ]
    DEFAULT_OBJECTIVE_TYPES = ['voice_cmd', 'voice_cmd__and__voice_cmd_lng']
    DEFAULT_CONV_DROPOUT_PROBABILITIES = [0.2]
    DEFAULT_FC_DROPOUT_PROBABILITIES = [0.2]
    DEFAULT_SELECTED_LANGUAGES = {'_language_independent', 'francais', 'maninka', 'pular', 'susu'}

    # Configure parser
    parser = ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-name", required=True, choices=["VAASRCNN1", "VAASRCNN2"])
    parser.add_argument("--gpu-id", type=int, default=-1)
    parser.add_argument("--fold-count", type=int, default=10)
    parser.add_argument("--feature-names", default=DEFAULT_FEATURE_NAMES)
    parser.add_argument("--objective-types", default=DEFAULT_OBJECTIVE_TYPES)
    parser.add_argument("--conv-dropout-probabilities", type=float, nargs="*", default=DEFAULT_CONV_DROPOUT_PROBABILITIES)
    parser.add_argument("--fc-dropout-probabilities", type=float, nargs="*", default=DEFAULT_FC_DROPOUT_PROBABILITIES)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--train-percent", type=float, default=0.7)
    parser.add_argument("--epochs", type=int, default=1000)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--max-sequence-length", type=int, default=200)
    parser.add_argument("--selected-languages", default=DEFAULT_SELECTED_LANGUAGES)

    # Parse and return args
    return parser.parse_args()


def configure_logging(args):
    module_name = Path(__file__).stem

    pid = os.getpid()
    start_time= datetime.datetime.now().isoformat()

    logging.basicConfig(
        filename = Path(args.output_dir) / f"{module_name}_{start_time}_pid_{pid}.log",
        level = logging.DEBUG,
        format="%(asctime)s:%(levelno)s:%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z"
        )


if __name__ == '__main__':
    args = parse_arguments()
    Path(args.output_dir).mkdir(exist_ok=True, parents=True)
    configure_logging(args)
    main(args)
