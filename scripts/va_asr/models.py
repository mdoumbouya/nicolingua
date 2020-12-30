import torch
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path

def mean_aggregation(x, dim):
    return torch.mean(x, dim)

def max_aggregation(x, dim):
    v, i = torch.max(x, dim)
    return v

class VAASRCNN(nn.Module):
    def __init__(self,
            input_channels,
            conv_channels,
            conv_pooling_type,
            conv_aggregate_type,
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
            ):

        super(VAASRCNN, self).__init__()


        self.input_channels = input_channels
        self.conv_dropout_p = conv_dropout_p
        self.fc_dropout_p = fc_dropout_p
        self.voice_cmd_neuron_count = voice_cmd_neuron_count
        self.voice_cmd_lng_neuron_count = voice_cmd_lng_neuron_count
        self.objective_type = objective_type
        
        if conv_pooling_type not in {"max", "avg"}:
            raise ValueError(f"Unknown Conv Pooling Type: {conv_pooling_type}")

        if conv_aggregate_type not in {"max", "mean"}:
            raise ValueError(f"Unknown Conv Aggregate Type: {conv_aggregate_type}")
        
            
        conv_pooling_class_by_type = {
            "max": nn.MaxPool1d,
            "avg": nn.AvgPool1d,
        }
        conv_pooling_class = conv_pooling_class_by_type[conv_pooling_type]

        if conv_aggregate_type == "max":
            self.conv_aggregate_fn = mean_aggregation
        else:
            self.conv_aggregate_fn = max_aggregation

        self.conv0 = nn.Conv1d(
            in_channels=input_channels, 
            out_channels=conv_channels[0], 
            kernel_size=1
            )
        
        self.conv1 = nn.Conv1d(
            in_channels=conv_channels[0], 
            out_channels=conv_channels[1], 
            kernel_size=3
            )
        self.drop1 = nn.Dropout(p=conv_dropout_p)
        self.pool1 = conv_pooling_class(kernel_size=2, stride=2)
        
        self.conv2 = nn.Conv1d(
            in_channels=conv_channels[1], 
            out_channels=conv_channels[2], 
            kernel_size=3
            )
        self.drop2 = nn.Dropout(p=conv_dropout_p)
        self.pool2 = conv_pooling_class(kernel_size=2, stride=2)
        
        self.conv3 = nn.Conv1d(
            in_channels=conv_channels[2], 
            out_channels=conv_channels[3], 
            kernel_size=3
            )
        self.drop3 = nn.Dropout(p=conv_dropout_p)
        self.pool3 = conv_pooling_class(kernel_size=2, stride=2)

        self.conv4 = nn.Conv1d(
            in_channels=conv_channels[3], 
            out_channels=conv_channels[4], 
            kernel_size=3
            )
        self.drop4 = nn.Dropout(p=conv_dropout_p)
        self.pool4 = conv_pooling_class(kernel_size=2, stride=2)
        
        self.drop5 = nn.Dropout(p=fc_dropout_p)
        
        self.lin61 = nn.Linear(in_features=sum(conv_channels[2:]), out_features=voice_cmd_neuron_count)
        
        # 'voice_cmd', 'voice_cmd__and__voice_cmd_lng'
        if self.objective_type == 'voice_cmd__and__voice_cmd_lng':
            self.lin62 = nn.Linear(in_features=sum(conv_channels[2:]), out_features=voice_cmd_lng_neuron_count)
                
    def forward(self, x):
        x = x.permute(0, 2, 1)
        
        x = self.conv0(x)
        
        x = self.conv1(x)
        x = F.elu(x)
        x = self.drop1(x)
        x = self.pool1(x)
        
        x = self.conv2(x)
        x = F.elu(x)
        x = self.drop2(x)
        x = self.pool2(x)
        
        v1 = self.conv_aggregate_fn(x, dim=2)
        
        x = self.conv3(x)
        x = F.elu(x)
        x = self.drop3(x)
        x = self.pool3(x)
        
        v2 = self.conv_aggregate_fn(x, dim=2)
        
        x = self.conv4(x)
        x = F.elu(x)
        x = self.drop4(x)
        x = self.pool4(x)
        
        v3 = self.conv_aggregate_fn(x, dim=2)
        
        v = torch.cat((v1, v2, v3), axis=1)
        v = self.drop5(v)
        
        if self.objective_type == 'voice_cmd':
            logits_voice_cmd = self.lin61(v)
            return logits_voice_cmd
        elif self.objective_type == 'voice_cmd__and__voice_cmd_lng':
            logits_voice_cmd = self.lin61(v)
            logits_voice_cmd_lng = self.lin62(v)
            return logits_voice_cmd, logits_voice_cmd_lng
        else:
            raise ValueError(f"Unknown objective type: {self.objective_type}")



class VAASRCNN1(VAASRCNN):
    def __init__(
            self,
            input_channels,
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
        ):

        super(VAASRCNN1, self).__init__(
            input_channels,
            [8, 8, 16, 32, 64],
            "avg", #conv_pooling_type,
            "mean", # conv_aggregate_type
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
        )


class VAASRCNN2(VAASRCNN):
    def __init__(
            self,
            input_channels,
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
        ):

        super(VAASRCNN2, self).__init__(
            input_channels,
            [8, 16, 32, 64, 128],
            "avg", #conv_pooling_type,
            "mean", # conv_aggregate_type
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
        )

class VAASRCNN3(VAASRCNN):
    def __init__(
            self,
            input_channels, 
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
        ):

        super(VAASRCNN3, self).__init__(
            input_channels,
            [16, 32, 64, 128, 256],
            "avg", #conv_pooling_type,
            "mean", # conv_aggregate_type
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
        )

class VAASRCNN3PoolAvgAggMax(VAASRCNN):
    def __init__(
            self,
            input_channels, 
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
        ):

        super(VAASRCNN3PoolAvgAggMax, self).__init__(
            input_channels,
            [16, 32, 64, 128, 256],
            "avg", #conv_pooling_type,
            "max", # conv_aggregate_type
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
        )


class VAASRCNN3PoolMaxAggMax(VAASRCNN):
    def __init__(
            self,
            input_channels, 
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
        ):

        super(VAASRCNN3PoolMaxAggMax, self).__init__(
            input_channels,
            [16, 32, 64, 128, 256],
            "max", #conv_pooling_type,
            "max", # conv_aggregate_type
            conv_dropout_p, 
            fc_dropout_p, 
            voice_cmd_neuron_count, 
            voice_cmd_lng_neuron_count,
            objective_type
        )


def save_model(model, optimizer, fold_id, feature_name, epoch, args):
    model_name =  model.__class__.__name__
    
    save_dir = Path(f"{args.output_dir}/checkpoints/{model_name}/{feature_name}_{fold_id}_checkpoints")
    save_path = save_dir / f"{epoch:04}.pt"
    
    save_dir.mkdir(parents=True, exist_ok=True)
    
    torch.save(
        {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'fold_id': fold_id,
            'feature_name': feature_name,
            'model_name':  model_name,
            'input_channels': model.input_channels, 
            'conv_dropout_p': model.conv_dropout_p, 
            'fc_dropout_p': model.fc_dropout_p, 
            'voice_cmd_neuron_count': model.voice_cmd_neuron_count, 
            'voice_cmd_lng_neuron_count': model.voice_cmd_lng_neuron_count,
            'objective_type': model.objective_type
        }, 
        save_path
    )


def load_model(checkpoint_path):
    state_dict = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    asrmodel = globals()[state_dict['model_name']](
        input_channels = state_dict['input_channels'], 
        conv_dropout_p = state_dict['conv_dropout_p'], 
        fc_dropout_p = state_dict['fc_dropout_p'], 
        voice_cmd_neuron_count = state_dict['voice_cmd_neuron_count'], 
        voice_cmd_lng_neuron_count = state_dict['voice_cmd_lng_neuron_count'], 
        objective_type = state_dict['objective_type'], 
    )

    asrmodel.load_state_dict(state_dict['model_state_dict'])

    #asrmodel = getattr(this, state_dict['model_name'])(
    #    input_channels = state_dict['input_channels'], 
    #    conv_dropout_p = state_dict['conv_dropout_p'], 
    #    fc_dropout_p = state_dict['fc_dropout_p'], 
    #    voice_cmd_neuron_count = state_dict['voice_cmd_neuron_count'], 
    #    voice_cmd_lng_neuron_count = state_dict['voice_cmd_lng_neuron_count'], 
    #    objective_type = state_dict['objective_type'], 
    #)
    return asrmodel