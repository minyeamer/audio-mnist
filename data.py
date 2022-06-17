import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import librosa
from sklearn.model_selection import train_test_split


def load_data(path='data/train', test_size=0.3):
    data = pd.read_csv(path+'.csv')
    data_wav = make_dataset(data, path)
    mfccs = preprocess_dataset(data_wav.data)
    if test_size > 0:
        return train_test_split(mfccs, data_wav.label, test_size=test_size)
    else:
        return (mfccs, np.array(data_wav.label)) if 'train' in path else mfccs


def make_dataset(df, path):
    dataset = []
    for file in tqdm(os.listdir(path),colour='green'):
        if 'wav' in file:
            abs_file_path = os.path.join(path,file)
            data, sr = librosa.load(abs_file_path, sr=16000)
            if 'train' in path:
                class_label = int(df[df.file_name == file].label)
                dataset.append([data,class_label])
            else:
                dataset.append([data, file])

    print('Dataset 생성 완료')
    columns = ['data','label'] if 'train' in path else ['data','file_name']
    return pd.DataFrame(dataset,columns=columns)


def preprocess_dataset(data):
    mfccs = []
    for i in data:
        extracted_features = librosa.feature.mfcc(y=i,
                                                sr=16000,
                                                n_mfcc=40)
        extracted_features = np.mean(extracted_features.T,axis=0)
        mfccs.append(extracted_features)

    return np.array(mfccs)
