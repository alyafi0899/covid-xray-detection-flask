from keras.models import load_model
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from BCI2kReader import BCI2kReader as b2k
import pandas as pd
import glob
import os
import json
import pyrebase

def data_extraction_pred(raw):
    combine_dataframe = []
    for i in range(16):
        mean = raw.values[i].mean()  # mean setiap channel (channel = index array)
        combine_dataframe.append(float(mean))

        std = raw.values[i].std()
        combine_dataframe.append(float(std))

        snr = signaltonoise(raw.values[i])
        combine_dataframe.append(float(snr))

        min_iqr, max_iqr = quantilee(raw.values[i])
        combine_dataframe.append(float(min_iqr))
        combine_dataframe.append(float(max_iqr))

    # final_dataframe = pd.DataFrame(combine_dataframe, index = ['FP1_mean', 'FP1_std', 'FP1_snr', 'F3_mean', 'F3_std', 'F3_snr', 'F7_mean', 'F7_std', 'F7_snr', 'T3_mean', 'T3_std', 'T3_snr','T5_mean', 'T5_std', 'T5_snr','O1_mean', 'O1_std', 'O1_snr','C4_mean', 'C4_std', 'C4_snr','FP2_mean', 'FP2_std', 'FP2_snr','Fz_mean', 'Fz_std', 'Fz_snr','F4_mean', 'F4_std', 'F4_snr','F8_mean', 'F8_std', 'F8_snr','C3_mean', 'C3_std', 'C3_snr','Cz_mean', 'Cz_std', 'Cz_snr','Pz_mean', 'Pz_std', 'Pz_snr','Oz_mean', 'Oz_std', 'Oz_snr','O2_mean', 'O2_std', 'O2_snr'])
    final_dataframe = pd.DataFrame(combine_dataframe)
    final_dataframe = pd.DataFrame.transpose(final_dataframe)
    final_dataframe.reset_index()
    return final_dataframe


def quantilee(a):
    Q1 = np.quantile(a, .25)
    Q3 = np.quantile(a, .75)
    IQR = Q3 - Q1
    min_IQR = Q1 - 1.5 * IQR
    max_IQR = Q3 + 1.5 * IQR
    return min_IQR, max_IQR


def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)


while True:
    try:
        config = {
            "apiKey": "AIzaSyAwYFtxgOHCSfvm0JisBQNdXger82N7OeA",
            "authDomain": "asd-telemedical.firebaseapp.com",
            "databaseURL": "https://asd-telemedical-default-rtdb.asia-southeast1.firebasedatabase.app",
            "projectId": "asd-telemedical",
            "storageBucket": "asd-telemedical.appspot.com",
            "messagingSenderId": "132973919920",
            "appId": "1:132973919920:web:684c5d32695cb386d70575",
            "measurementId": "G-7KLT4RBEPE"
        }
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        db = firebase.database()
        user_db = db.child("eeg_function").get()
        user_parent = user_db.key()
        filename_db = {}
        for i in user_db.each():
            filename_db = list(user_db.val().values())
        #=============================================================
        filename = filename_db[0]
        trigger = filename_db[2]
        path_cloud = f"files/{filename}"
        storage.child(path_cloud).download(filename)

        if trigger is True:
                storage.child(path_cloud).download(filename)
                if os.path.exists(filename):
                    filename3 = filename
                    with b2k.BCI2kReader(filename3) as test3:
                        my_states = test3.read(-1)
                        my_signals3, stateslice3 = test3[100:500]

                    plot_autism_eeg = pd.DataFrame(my_signals3)
                    plot_autism_eeg = pd.DataFrame.transpose(plot_autism_eeg)

                    model = load_model('./trained_model_saved_model_improved.h5')
                    classes = model.predict(data_extraction_pred(plot_autism_eeg), batch_size=500)
                    # classes = [2]
                    # print(classes[0])
                    if classes[0] > 0.99932:
                        data = {"filename": filename, "hasil": "autism", "trigger": False}
                        db.child(user_parent).update(data)
                        os.remove(filename)
                    else:
                        data = {"filename": filename, "hasil": "normal", "trigger": False}
                        db.child(user_parent).update(data)
                        os.remove(filename)

                else:
                    data = {"filename": filename, "hasil": "File Tidak ada", "trigger": False}
                    db.child(user_parent).update(data)
                    os.remove(filename)
                    pass
        else:
            pass
    except OSError as e: print(e)