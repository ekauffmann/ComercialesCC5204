import cv2
import sys
import os
import csv
import datetime
import numpy as np

# TO DO convertir blaTXT a npy y csv a numpytxt

freq = int(sys.argv[1])
zonas = (int(sys.argv[2]), int(sys.argv[3]))
bins = int(sys.argv[4])
dims = (720,400)
x= dims[0]/zonas[0]
y= dims[1]/zonas[1]

config= "freq%szone%s,%sbins%s" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

newpath = r"pruebas/"+config

if not os.path.exists(newpath):
    os.makedirs(newpath)
    os.makedirs(newpath+"/base")
    os.makedirs(newpath+"/comerciales")

def describeFolder(path, newPath):

    for file in os.listdir(path):
        video_capture = cv2.VideoCapture(path+"/"+file)
        video_desc = np.zeros(zonas[0]*zonas[1]*bins)
        print("describiendo " + file)
        frame_count = 0
        while (video_capture.isOpened()):
            ret, frame = video_capture.read()
            if frame is None:
                break
            if frame_count%freq==0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, dims)
                cv2.imshow('frame2', gray)
                frame_desc = []
                for i in xrange(zonas[0]):
                    for j in xrange(zonas[1]):
                        zona = gray[y*j:y*(j+1)-1, x*i:x*(i+1)-1]
                        hist = cv2.calcHist([zona],[0],None,[bins],[0,256])
                        hist_array = [item for sublist in hist for item in sublist]
                        frame_desc += hist_array
                video_desc= np.vstack((video_desc, np.array(frame_desc)))


            frame_count+=1
        np.save(newPath +"/"+path+"/"+file[:-4]+".npy", video_desc[1:])
        video_capture.release()

time_ini = datetime.datetime.now()
describeFolder("comerciales", newpath)
describeFolder("base", newpath)
time_end = datetime.datetime.now()

with open(newpath+"/metadata.csv", "wb") as csv_metadata:
    metadatawriter = csv.writer(csv_metadata, delimiter=',')
    metadatawriter.writerow(["freq","zonas","bins","dims", "time"])
    total_time = time_end - time_ini
    metadatawriter.writerow([freq,zonas,bins,dims,total_time])