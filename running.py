from keras.models import load_model
import numpy as np
import keras
from tensorflow.keras.utils import img_to_array
import os
import pyrebase
import time



hasil_trigger_values = 'null'
model = load_model('trained_model.h5')
try :
    config = {
                "apiKey": "AIzaSyB71SiXS7FtCihNwgUxzJHY315FjD3HMhM",
                "authDomain": "pkm-telemedical-covid19.firebaseapp.com",
                "databaseURL": "https://pkm-telemedical-covid19-default-rtdb.asia-southeast1.firebasedatabase.app",
                "storageBucket": "pkm-telemedical-covid19.appspot.com",
            }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    db = firebase.database()

    print('firebase connected')
except OSError as e: print(e)

while True:
    try:
        user_db = db.child("users").get()
        user_parent = user_db.key()
        filename_db = {}
        for i in user_db.each():
            filename_db = list(user_db.val().values())
        #=============================================================
        filename = filename_db[0]
        trigger = filename_db[2]

        path_cloud = f"files/{filename}"
        if trigger is True and filename != hasil_trigger_values:
                time.sleep(1)
                storage.child(path_cloud).download(filename)
                if os.path.exists(filename) :

                            img = keras.utils.load_img(filename, target_size=(500, 500))

                            x = img_to_array(img)
                            x /= 255
                            img_test = np.expand_dims(x, axis=0)

                            classes = model.predict(img_test, batch_size=50)
                            print(classes[0])

                            if classes[0] < 0.5:
                                data = {"filename": 'null', "hasil": "Normal", "trigger": False}
                                db.child(user_parent).update(data)
                                os.remove(filename)
                            else:
                                data = {"filename": 'null', "hasil": "Positif Covid-19", "trigger": False}
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