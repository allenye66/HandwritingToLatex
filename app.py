from flask import Flask, request, render_template

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.image as mpimg
import pandas as pd
import os
from keras.models import load_model
from base64 import b64decode
from PIL import Image



app = Flask(__name__)
temp_img_path = "/home/anant/Downloads/Latex Converter/image.png"
temp_img_path_2 = "/home/anant/Downloads/Latex Converter/image2.png"
model_path = '/home/anant/Downloads/Latex Converter/model.h5'

temp = tf.Session()
keras.backend.set_session(temp)
model = load_model(model_path)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods = ['POST'])
def process():
	uri = stringNormalize(request.get_data().decode("utf-8"))
	print(uri)
	num_arr = uriToImage(uri)
	print("Image recieved")
	img_arr = normalize(parse(num_arr))
	print("Image array Recieved: ", len(img_arr))
	char_arr = []
	print("Predicting")
	for i in img_arr:
		temp = predict(model, i)
		char_arr.append(temp)
	print(char_arr)

def stringNormalize(uri):
    uri = uri.replace("%21", "!")
    uri =uri.replace("%23", "#")
    uri =uri.replace("%24", "$")
    uri =uri.replace("%25", "%")
    uri =uri.replace("%26", "&")
    uri =uri.replace("%27", "'")
    uri =uri.replace("%26", "&")
    uri =uri.replace("%28", "(")
    uri =uri.replace("%29", ")")
    uri =uri.replace("%2A", "*")
    uri =uri.replace("%2B", "+")
    uri =uri.replace("%2C", ",")
    uri =uri.replace("%2F", "/")
    uri =uri.replace("%3A", ":")
    uri =uri.replace("%3B", ";")
    uri =uri.replace("%3D", "=")
    uri =uri.replace("%3F", "?")
    uri =uri.replace("%40", "@")
    uri =uri.replace("%5B", "[")
    uri =uri.replace("%3B", "]")
    return uri

def uriToImage(uri):
	header, encoded = uri.split(",", 1)
	data = b64decode(encoded)
	with open(temp_img_path, "wb") as f:
		f.write(data)
	img = mpimg.imread(temp_img_path)
	shape = img.shape
	for i in range(shape[0]):
		for j in range(shape[1]):
			if(img[i][j][3] == 0):
				img[i][i][0] = 255
				img[i][i][1] = 255
				img[i][i][2] = 255
				img[i][j][3] = 255
	return img

def split_horizontal(array):
    arr = []
    arrhorizontal = []

    for i in range(array.shape[0]):
        tempSet= set()
        for j in range(array.shape[1]):

            temp = 0
            for k in range(3):
                #if(imarray[i][j][k] != 255):
                #    print(imarray[i][j][k], "tuple: " , (i,j,k))
                temp = temp + array[i][j][k]

            tempSet.add(temp)
       # print(tempSet, " len: ", len(tempSet))

        #CHANGE BACK TO 1 FOR MICHAEL
        if len(tempSet) > 2:
            arr.append("no")
        else:
            arr.append("yes")
            
    fool = arr[0]
    barr = []
    barrhorizontal = []
    for i in range(len(arr)):
        if (arr[i] is not fool):
            barr.append(i)
            fool = arr[i]
    return barr

def parse(imarray):
	arr = []
	for i in range(imarray.shape[1]):
	    tempSet= set()
	    for j in range(imarray.shape[0]):

	        temp = 0
	        for k in range(3):
	            #if(imarray[i][j][k] != 255):
	            #    print(imarray[i][j][k], "tuple: " , (i,j,k))
	            temp = temp + imarray[j][i][k]
	            
	        tempSet.add(temp)
	   # print(tempSet, " len: ", len(tempSet))
	    
	    #CHANGE BACK TO 1 FOR MICHAEL
	    if len(tempSet) > 2:
	        arr.append("no")
	    else:
	        arr.append("yes")
	fool = arr[0]
	barr = []
	for i in range(len(arr)):
	    if (arr[i] is not fool):
	        barr.append(i)
	        fool = arr[i]
	bar = []
	for i in range(len(barr)-1):
	    bar.append((barr[i] + barr[i+1])//2)
	bar.insert(0, 0)
	bar.append(imarray.shape[1]-1)
	arrayColNum = []
	for i in range(len(bar)):
	    if i % 2 == 0:
	        arrayColNum.append(bar[i])

	arrayOfImgs = []

	arrs = np.split(imarray, [int(i) for i in arrayColNum], axis = 1)[1:]

	for i in arrs:
	    print(i.shape)
	    arr_temp= split_horizontal(i)
	    int1, int2 = (0,0)
	    if(len(arr_temp) == 0):
	        int1 = 0
	        int2 = i.shape[0] - 1
	    elif(len(arr_temp) == 1):
	        int1 = arr_temp[0]
	        int2 = i.shape[0] - 1
	    else:
	        int1 = arr_temp[0]
	        int2 = arr_temp[-1]
	    
	    print(int1, int2)
	    arrayOfImgs.append(np.split(i, [int1, int2], axis = 0)[1])
	print(arrayOfImgs)
	return arrayOfImgs

def normalize(arr):
	new = []
	temporary = np.zeros((128,128,3))
	for i in arr:
		i = i.astype(np.uint8)
		mpimg.imsave(temp_img_path_2, i)
		img = np.asarray(Image.open(temp_img_path_2).resize((128,128)))
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):
				temporary[i][j] = [img[i][j][0], img[i][j][1], img[i][j][2]]
		new.append(temporary)
	return new



def predict(model, picture):
	
	with temp.as_default():
		with temp.graph.as_default():
			pred = model.predict(np.asarray([picture])).tolist()[0]
			return pred.index(max(pred))


if __name__ == '__main__':
    app.run(debug = True)