import cv2
import sys
from matplotlib import pyplot as plt

videoEntrada = "Tarea1-test1.mp4"
# videoSalida = sys.argv[2]

video_capture = cv2.VideoCapture(videoEntrada)

encoding = cv2.cv.CV_FOURCC(*'XVID')
fps = video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
width = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
height = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
count = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

ret, frame = video_capture.read()
i = 1

while ret:

    if (i % 10 == 0): print "%s%% frames procesados" % (int(i / frame_count * 100))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #TO DO: ESCALAR

    # grays=[gray[0:height/2,0:width/2],
    #        gray[height/2 + 1: height-1, width/2 + 1, width-1],
    #        gray[0:height/2+1, width/2 + 1, width-1 ],
    #        gray[height/2 + 1: height-1, 0:width/2]
    #        ]

    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    plt.plot(histr,color = "b")
    plt.xlim([0,256])
    plt.show()


video_capture.release()
