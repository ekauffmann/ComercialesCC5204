import cv2
import sys
from matplotlib import pyplot as plt

videoEntrada = "Tarea1-test1.mp4"
# videoSalida = sys.argv[2]

video_capture = cv2.VideoCapture(videoEntrada)

encoding = cv2.cv.CV_FOURCC(*'XVID')
fps = video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
width = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
print width
height = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
print height
count = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

i = 0
    #TO DO: ESCALAR
    # grays=[gray[0:height/2,0:width/2],
    #        gray[height/2 + 1: height-1, width/2 + 1, width-1],
    #        gray[0:height/2+1, width/2 + 1, width-1 ],
    #        gray[height/2 + 1: height-1, 0:width/2]
    #        ]
while (video_capture.isOpened()):

    ret, frame = video_capture.read()
    if frame is None:
        break
    i+=1
    if i%30==0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        hist = cv2.calcHist([gray],[0],None,[64],[0,256])

        print hist
        plt.plot(hist,color = "b")
        plt.xlim([0,64])
        plt.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video_capture.release()