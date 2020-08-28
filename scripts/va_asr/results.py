from pathlib import Path
import csv

def get_results_file_path(trial_name, args):
    return Path(args.output_dir) / f"{trial_name}.csv"

def get_checkpoints_dir(trial_name, args):
    return Path(args.output_dir) / f"{trial_name}_checkpoints"

def results_exist(trial_name, args):
    return get_results_file_path(trial_name, args).is_file()
    

def save_results(trial_name, trial_results, args):
    feature_name = trial_results['feature_name']
    fold_index = trial_results['fold_index']
    
    fname = get_results_file_path(trial_name, args)
    # Path(fname).parent.mkdir(parents=True, exist_ok=True)
    with open(fname, 'w') as f:
        fieldnames = sorted(trial_results['epochs'][1].keys())
        
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='raise')
        
        writer.writeheader()
        
        for epoch in sorted(trial_results['epochs'].keys()):
            writer.writerow(trial_results['epochs'][epoch])