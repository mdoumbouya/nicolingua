from pathlib import Path

def get_results_file_path(trial_name, args):
    return Path(args.output_dir) / f"{trial_name}.csv"

def get_checkpoints_dir(trial_name, args):
    return Path(args.output_dir) / f"{trial_name}_checkpoints"

def results_exist(trial_name, args):
    return get_results_file_path(trial_name, args).is_file()
    

def save_results(trial_name, trial_results, args):
    feature_name = trial_results['feature_name']
    fold_index = trial_results['fold_index']
    
    Path(RESULTS_DIR).mkdir(exist_ok=True, parents=True)
    fname = f"{RESULTS_DIR}/{model_name}/{feature_name}_{fold_index}.csv"
    Path(fname).parent.mkdir(parents=True, exist_ok=True)
    with open(fname, 'w') as f:
        fieldnames = sorted(trial_results['epochs'][1].keys())
        
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='raise')
        
        writer.writeheader()
        
        for epoch in sorted(trial_results['epochs'].keys()):
            writer.writerow(trial_results['epochs'][epoch])