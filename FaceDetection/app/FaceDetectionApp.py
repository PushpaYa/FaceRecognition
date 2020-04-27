#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri March 27 12:23:59 2020

@author: pushpa
"""
from flask import Flask, request, redirect, url_for, send_from_directory,send_file
from flask import Flask, request, jsonify,render_template
from flask_debug import Debug
from flask import Flask, request, jsonify,render_template
from flask_json import FlaskJSON, JsonError, json_response
import logging
import os
import glob
from os.path import basename
from flask import Response
import numpy as np
import pandas 
import pandas as pd
from os.path import basename
from numpy import nan
import re
import json
from werkzeug.utils import secure_filename
import cv2
import face_recognition
import glob
from os.path import basename
import os, sys
import numpy as np
from PIL import Image, ImageDraw
import os
import pickle

cwd = os.getcwd()
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
path =cwd+"/"+"upload_image"+"/"
print(path)
UPLOAD_FOLDER = path
Debug(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpeg','jpg','JPG','JPEG'])
img_folder=cwd+"/train_image/"
Files = glob.glob(img_folder+'*.*')
img=[]
face_encoding=[]
known_face_encodings=[]
known_face_names=[]

#Train model using train images
for file in Files:
    print("file",file)
    filename = os.path.splitext(basename(file))[0]
    FileExt = os.path.splitext(basename(file))[1]
    image = face_recognition.load_image_file(img_folder+filename+FileExt)
    encodings = face_recognition.face_encodings(image)
    if len(encodings) > 0:
        encoding=encodings[0]
        known_face_encodings.append(encoding)
        known_face_names.append(filename)
    else:
       print("No faces found in the image!")
           

#dump the trained encoding in pickle file   
with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(known_face_encodings, f)
    
    
    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS




@app.route('/', methods=['GET', 'POST'])
def upload_file_image():
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            logging.info('app.app_context')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            logging.info('app.app_context')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return "file uploaded successfully"
            return redirect(url_for('upload_file_image',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Please upload class picture</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
 
    
    
    
global frame

#take latest timestamp file from uploaded folder
def get_file_name():
    Files = glob.glob(path+'/*.*')
    if len(Files) > 0:
            latest_file_path = max(Files, key=os.path.getctime)
            filename = os.path.splitext(basename(latest_file_path))[0]     
            FileExt = os.path.splitext(basename(latest_file_path))[1]
            filename = path+filename+FileExt
    else:
        filename = ""
        

    return filename  

#reconige and tag faces ,return roll no ,name and tagged image
@app.route('/face_recognition_frames', methods=['GET', 'POST'])   
def face_recognition_frames():
    face_locations = []
    face_encodings = []
    face_names=[]
    students_records={}
    frame_number = 0
    # Load face encodings
    with open('dataset_faces.dat', 'rb') as f:
         known_face_encodings = pickle.load(f)
    
    frame = get_file_name()
    print(frame)
    name = "Could not find face check uploded image"
    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(frame)
    # Assume the whole image is the location of the face
    height, width, _ = unknown_image.shape
    
    
    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.4)
        name = "Unknown"
        rollno="Unknown"
        # See how far apart the test image is from the known faces
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        print("best_match_index",best_match_index)
        if matches[best_match_index]:
            name_rollno = known_face_names[best_match_index]
            name = name_rollno.split("_")[0]+" "+name_rollno.split("_")[1]
            rollno=name_rollno.split("_")[-2]

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        face_names.append(name)
        students_records[name]=rollno
    
        # Remove the drawing library from memory as per the Pillow docs
    del draw
    
        # Display the resulting image
        #pil_image.show()
    
        # You can also save a copy of the new image to disk if you want by uncommenting this line
    savepath="/home/pushpa/FaceDetection/app/data/"
    pil_image.save(os.path.join(savepath)+"image_with_boxes"+str(frame_number)+".jpeg")
    frame_number=frame_number+1
    if(len(face_names)==0):
        response = jsonify("No Face Found")
        response.headers['name'] = "No Face"
        response.headers['path'] = "No Image Saved"
    else:
        #image_file=os.path.join(path)+"image_with_boxes"+str(frame_number-1)+".jpeg"
        #response = app.make_response(image_file)
        response = send_file(os.path.join(savepath)+"image_with_boxes"+str(frame_number-1)+".jpeg")
        response.headers['name'] = students_records
        response.headers['path'] = os.path.join(savepath)+"image_with_boxes"+str(frame_number-1)+".jpeg"
    return response
    
if __name__ == "__main__":
    #app.run(debug=True)
	app.run(host = '0.0.0.0',port = 5011) 
    
    
    
