# Using Radio Archives for Low-Resource Speech Recognition
## Towards an Intelligent Virtual Assistant for Illiterate Users


# Code
- [West African Virtual Assistant ASR](scripts/va_asr)
- [Virtual Assistant ASR Web Demo](scripts/webdemo)
- Reproducing Experimental Results
    - [E306: Speech Recognition Experiments](notebooks/E306)
    - [E209: Language Identification Experiments](notebooks/E209)
    - [Makefile](Makefile)



# Dataset: West African Radio Corpus
17,091 audio clips of length 30 seconds sampled from archives collected from 6 Guinean radio stations. The broadcasts consist of news and various radio shows in languages including French, Guerze, Koniaka, Kissi, Kono, Maninka, Mano, Pular, Susu, and Toma. Some radio shows include phone calls, background and foreground music, and various noise types. 


**Download from OpenSLR**

<a href="http://openslr.org/105/">http://openslr.org/105/</a>

**Download via https**
```
wget \
    https://nicolingua.s3.eu-west-2.amazonaws.com/nicolingua-0003-west-african-radio-corpus.tgz \
    nicolingua-0003-west-african-radio-corpus.tgz
```

**Download with aws-cli**
```
aws s3 cp \
    s3://nicolingua/nicolingua-0003-west-african-radio-corpus-openslr.tgz \
    nicolingua-0003-west-african-radio-corpus-openslr.tgz
```

# Dataset: West African Virtual Assistant Speech Recognition Corpus:
10,083 recorded utterances from 49 speakers (16 female and 33 male) ranging from 5 to 76 years old on a variety of devices.

**Download from OpenSLR**

<a href="http://openslr.org/106/">http://openslr.org/106/</a>

**Download via https**
```
wget \
    https://nicolingua.s3.eu-west-2.amazonaws.com/nicolingua-0004-west-african-va-asr-corpus.tgz \
    nicolingua-0004-west-african-va-asr-corpus.tgz
```

**Download with aws-cli**
```
aws s3 cp \
    s3://nicolingua/nicolingua-0004-west-african-va-asr-corpus.tgz \
    nicolingua-0004-west-african-va-asr-corpus.tgz
```

# Pre-Trained Model: West African Wav2vec

Compatible with the [baseline wav2vec large](https://github.com/pytorch/fairseq/tree/master/examples/wav2vec) model. Traned on the West African Radio Corpus.


**Download via https**
```
wget \
    https://nicolingua.s3.eu-west-2.amazonaws.com/nicolingua-0003-west-african-wav2vec.tgz \
    nicolingua-0003-west-african-wav2vec.tgz
```

**Download with aws-cli**
```
aws s3 cp \
    s3://nicolingua/nicolingua-0003-west-african-wav2vec.tgz \
    nicolingua-0003-west-african-wav2vec.tgz
```




# Licence


<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.



# How to cite our work
APA
```
Doumbouya, M., Einstein, L., Piech, C.. (2021). Using Radio Archives for Low-Resource Speech Recognition: Towards an Intelligent Virtual Assistant for Illiterate Users. In AAAI.
```

BibTex
```
 @inproceedings{doumbouya2021usingradio,
    title={Using Radio Archives for Low-Resource Speech Recognition: Towards an Intelligent Virtual Assistant for Illiterate Users},
    author={Doumbouya, Moussa and Einstein, Lisa and Piech, Chris},
    booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
    volume={35},
    year={2021}
  }
```

