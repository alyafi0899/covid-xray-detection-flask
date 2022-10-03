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
from PIL import Image as im
from keras.utils import img_to_array


def signal_to_image(filename):
    with b2k.BCI2kReader(filename) as test:
        my_signals, stateslice = test[100:5000]
        my_signals = my_signals.astype(np.uint8)
        data = im.fromarray(my_signals)
        data.save(f'./{filename}.png')
        print(1);


try:
    model = load_model('./trained_model_image_dataset.h5')
    config = {
        "apiKey": "AIzaSyAwYFtxgOHCSfvm0JisBQNdXger82N7OeA",
        "authDomain": "asd-telemedical.firebaseapp.com",
        "databaseURL": "https://asd-telemedical-default-rtdb.asia-southeast1.firebasedatabase.app/",
        "storageBucket": "asd-telemedical.appspot.com",
    }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    db = firebase.database()

    print('firebase connected')
except OSError as e:
    print(e)

while True:
    try:
        user_db = db.child("eeg_function").get()
        user_parent = user_db.key()
        filename_db = {}
        for i in user_db.each():
            filename_db = list(user_db.val().values())
        # =============================================================
        filename = filename_db[0]
        trigger = filename_db[2]
        path_cloud = f"files/{filename}"

        if trigger is True:
            storage.child(path_cloud).download(filename)
            signal_to_image(filename)
            if os.path.exists(f'{filename}.png'):

                img = tf.keras.utils.load_img(f'{filename}.png', target_size=(64, 300))

                x = img_to_array(img)
                x /= 255



                img_test = np.expand_dims(x, axis=0)

                classes = model.predict(img_test, batch_size=50)

                if classes[0] < 0.5:
                    data = {"filename": "null", "hasil": "Autism", "trigger": False}
                    db.child(user_parent).update(data)
                    os.remove(filename)
                    os.remove(f'{filename}.png')
                else:
                    data = {"filename": "null", "hasil": "Normal", "trigger": False}
                    db.child(user_parent).update(data)
                    os.remove(filename)
                    os.remove(f'{filename}.png')

            else:
                data = {"filename": filename, "hasil": "File Tidak ada", "trigger": False}
                db.child(user_parent).update(data)
                os.remove(filename)
                os.remove(f'{filename}.png')
                pass
        else:
            pass
    except OSError as e:
        print(e)
