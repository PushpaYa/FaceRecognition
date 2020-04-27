#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:06:17 2019

@author: pushpa
"""
import cv2
import face_recognition
import glob
from os.path import basename
import os, sys
import numpy as np
import pickle
img_folder="/home/pushpa/train_image/"
Files = glob.glob(img_folder+'*.*')
img=[]
face_encoding=[]
known_face_encodings={}
known_face_names=[]
for file in Files:
    print("file",file)
    filename = os.path.splitext(basename(file))[0]
    FileExt = os.path.splitext(basename(file))[1]
    image = face_recognition.load_image_file(img_folder+filename+FileExt)
    known_face_encodings[filename] = face_recognition.face_encodings(image)
    if len(known_face_encodings[filename]) > 0:
        known_face_encodings[filename]=known_face_encodings[filename][0]
    else:
       print("No faces found in the image!")
           
    #known_face_encodings.append(encoding)
    #known_face_names.append(filename)
with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(known_face_encodings, f)
    