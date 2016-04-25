import cv2
import sys
import os
import csv
import datetime

#### TO DO
# agregar numero de frame a cada linea de los descriptores

freq = int(sys.argv[1])
zonas = (int(sys.argv[2]), int(sys.argv[3]))
bins = int(sys.argv[4])
dims = (720,400)
x= dims[0]/zonas[0]
y= dims[1]/zonas[1]

config= "f"+ sys.argv[1] +"z"+ sys.argv[2] +","+sys.argv[3]+"b"+sys.argv[4]
newpath = r"descriptores/"+config

if not os.path.exists(newpath):
    os.makedirs(newpath)
    os.makedirs(newpath+"/base")
    os.makedirs(newpath+"/comerciales")

time_ini = datetime.datetime.now()
for file in os.listdir("comerciales"):
    video_capture = cv2.VideoCapture("comerciales/"+file)

    with open(newpath+"/comerciales/"+file[:-4]+"_desc.csv", 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        print("describiendo " + file)

        i = 0

        while (video_capture.isOpened()):

            ret, frame = video_capture.read()
            if frame is None:
                break

            if i%freq==0:
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

                spamwriter.writerow(frame_desc)
            i+=1
        csvfile.close()

    video_capture.release()

for file in os.listdir("base"):
    video_capture = cv2.VideoCapture("base/"+file)

    with open(newpath+"/base/"+file+"_desc.csv", 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        print("describiendo " + file)

        i = 0

        while (video_capture.isOpened()):

            ret, frame = video_capture.read()
            if frame is None:
                break

            if i%freq==0:
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

                spamwriter.writerow(frame_desc)
            i+=1
        csvfile.close()

    video_capture.release()

time_end = datetime.datetime.now()

with open(newpath+"/metadata.csv", "wb") as csv_metadata:
    metadatawriter = csv.writer(csv_metadata, delimiter=',')
    metadatawriter.writerow(["freq","zonas","bins","dims", "time"])
    total_time = time_end - time_ini
    metadatawriter.writerow([freq,zonas,bins,dims,total_time])


