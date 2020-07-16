import pydub
from pprint import PrettyPrinter
pprint = PrettyPrinter().pprint
import soundfile as sf
import audio_metadata

file_path = "/media/xtrem/data/experiments/nicolingua-0001-language-id/audio_samples/00034b34-b671-4e38-bc7a-6d6b0acdbda5.wav"
file_path = "/media/xtrem/data/experiments/nicolingua-0001-language-id/audio_samples/0006fefa-feba-45df-ad2e-f5369ed2da7c.wav"


#pprint(pydub.utils.mediainfo(file_path))

#data, samplerate = sf.read(file_path)

#pprint(sf.info(file_path))

tags = audio_metadata.load(file_path)['tags']['comment'][0]['text']
print(tags)

