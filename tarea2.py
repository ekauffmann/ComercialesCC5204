import cv2
import sys
from matplotlib import pyplot as plt

videoEntrada = "comerciales/donnasept.mp4"
# videoSalida = sys.argv[2]

video_capture = cv2.VideoCapture(videoEntrada)

encoding = cv2.cv.CV_FOURCC(*'XVID')
fps = video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
print fps