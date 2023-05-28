import pandas as pd
import numpy as np
import cv2
import urllib.request
import matplotlib.pyplot as plt
import string
import random

from tensorflow import keras
from keras.models import Sequential,load_model
from keras.layers import Dense,Dropout,Flatten
from keras.layers import MaxPooling2D,Conv2D

from keras import layers as L
import numpy as np

import os  
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


model= load_model('braille_train.h5')


# import our OCR function
# from ocr_core import ocr_core

# define a folder to store and later serve the images
UPLOAD_FOLDER = 'static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check the file extension
def allowed_file(filename):  
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/home')
def home_page():  
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():  
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='📎 No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='📎 No file selected')

        if file and allowed_file(file.filename):
            # Save the file to the upload folder
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.root_path, 'static/uploads', filename)
            file.save(file_path)

            # Call the OCR function on the saved file
            extracted_text = ocr_core(file_path)

            # Extract the text and display it
            return render_template('upload.html',
                                msg='✅ Successfully processed',
                                extracted_text=extracted_text,
                                img_src=UPLOAD_FOLDER + filename)
        
    elif request.method == 'GET':
        return render_template('upload.html')


def ocr_core(img_path):
    print("Image Path:", img_path)
    img = cv2.imread(img_path)
    h,w,c = img.shape
    print("height: ",h , " width : ", w) # h,w
    img_no=cv2.resize(img,(w,116))
    h1,w1,c1=img_no.shape

    sentence=""
    alphabet = list(string.ascii_lowercase)
    cur_pos = 0
    target = {}
    for letter in alphabet:
        target[letter] = [0] * 27
        target[letter][cur_pos] = 1
        cur_pos += 1
    target[' '] = [0] * 27
    target[' '][26] = 1


    for wid in range (0,w1,72):
        img_crop=img_no[:, 0+wid:72+wid]
        # cv2.imshow("zz",img_crop)
        pred_img = cv2.resize(img_crop, (28,28),interpolation=cv2.INTER_CUBIC)   
        # cv2.imshow("zz",pred_img)
        pred_img = pred_img.astype(np.float32)/255.0
        pred_img = np.expand_dims(pred_img,axis=0)
        pred_lb = model.predict(pred_img)
        for j in range(len(pred_lb[0])):
                if pred_lb[0][j] > 0.6:
                    pred_lb[0][j] = 1.0
                else:
                    pred_lb[0][j] = 0.0

        for key,value in target.items():
            if np.array_equal(np.asarray(pred_lb[0]),np.asarray(value)):
                print(key)
                sentence=sentence+key
    
    print(sentence)
    return sentence


if __name__ == '__main__':  
    app.run()

