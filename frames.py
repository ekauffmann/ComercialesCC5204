import cv2
import os

import csv
array=[
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12]]

with open('eggs.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|')
    spamwriter.writerow(array)
    spamwriter.writerow(array)
    spamwriter.writerow(array)

with open('eggs.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
       #print ', '.join(row)
        print row[0][0]

#
# zonas=(2,4)
# dims=(720,400)
#
# x= dims[0]/zonas[0]
# y= dims[1]/zonas[1]
# for file in os.listdir("base"):
#     video_capture = cv2.VideoCapture("base/"+file)
#     count = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
#     print("" + file + ": " + str(count) + "frame count")
#     video_capture.release()
#
#
# # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# # gray = cv2.resize(gray, dims)
# # cv2.imshow('frame2', gray)
# # cv2.waitKey(0)
# #
# # for i in xrange(zonas[0]):
# #     for j in xrange(zonas[1]):
# #         zona = gray[y*j:y*(j+1)-1, x*i:x*(i+1)-1]
# #         cv2.imshow('frame', zona)
# #         cv2.waitKey(0)
# # cv2.destroyAllWindows()