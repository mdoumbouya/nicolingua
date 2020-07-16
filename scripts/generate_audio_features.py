import torch
from fairseq.models.wav2vec import Wav2VecModel

cp = torch.load('models/wav2vec_large.pt')
model = Wav2VecModel.build_model(cp['args'], task=None)
model.load_state_dict(cp['model'])
model.eval()

wav_input_16khz = torch.randn(10,100000)
z = model.feature_extractor(wav_input_16khz)
print(z.shape)
c = model.feature_aggregator(z)
model.
print(c.shape)