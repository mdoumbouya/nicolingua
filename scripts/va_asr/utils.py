import torch
import torch.nn.functional as F

def get_torch_device(args):
    if args.gpu_id>0:
        device = torch.device(f"cuda:{GPU_ID}")
    else:
        device = torch.device(f"cpu")
    return device

def get_predictions_for_logits(logits):
    probs = F.softmax(logits, dim=1)
    return torch.argmax(probs, dim=1)