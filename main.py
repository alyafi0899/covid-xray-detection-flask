from keras.models import load_model
import numpy as np
import keras
from tensorflow.keras.utils import img_to_array
import json
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import pyrebase


from waitress import serve



app = Flask(__name__)
#
CORS(app)
# creating an API object
api = Api(app)


class prediction(Resource):
    def get(self, files):
        config = {
            "apiKey": "AIzaSyB71SiXS7FtCihNwgUxzJHY315FjD3HMhM",
            "authDomain": "pkm-telemedical-covid19.firebaseapp.com",
            "databaseURL": "https://pkm-telemedical-covid19-default-rtdb.asia-southeast1.firebasedatabase.app",
            "projectId": "pkm-telemedical-covid19",
            "storageBucket": "pkm-telemedical-covid19.appspot.com",
            "messagingSenderId": "961868874019",
            "appId": "1:961868874019:web:16bfe31ea165baf93a0c96",
            "measurementId": "G-24HVPLE5B6"
        }

        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        db = firebase.database()
#=============================================================

        filename = files
        path_cloud = f"files/{filename}"
        storage.child(path_cloud).download(filename)

        if os.path.exists(filename):
            model = load_model('trained_model.h5')
            img = keras.utils.load_img(filename, target_size=(500, 500))

            x = img_to_array(img)
            x /= 255
            img_test = np.expand_dims(x, axis=0)

            classes = model.predict(img_test, batch_size=50)
            print(classes[0])

            if classes[0] < 0.5:
                hasil = '{"hasil":"Normal"}'
                hasil_json = json.loads(hasil)
                os.remove(filename)
                return hasil_json

            else:
                hasil = '{"hasil":"positif covid"}'
                hasil_json = json.loads(hasil)
                os.remove(filename)
                return hasil_json
        else:
            hasil = '{"hasil":"File Tidak ada"}'
            hasil_json = json.loads(hasil)
            return hasil_json

api.add_resource(prediction, '/prediction/<string:files>')

if __name__ == '__main__':
      app.run(host="0.0.0.0", port=3000, debug=True)
# serve(app, host='0.0.0.0', port=8080, threads=1)