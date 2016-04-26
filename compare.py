import os
import cv2
import numpy as np
import sys
import datetime



def compare(path):

    comerciales = []
    comercial_array = []

    comercial_id = 0

    for file in os.listdir("pruebas/"+path+"/comerciales"):
        frames = np.loadtxt("pruebas/"+path+"/comerciales/"+file)
        comercial = [[comercial_id, file, frames]]
        comerciales += comercial
        comercial_array += [[comercial_id, file, len(frames)]]
        comercial_id+=1


    np.save("pruebas/"+path+"/comercial_dict.npy", np.array(comercial_array), fmt="%s", delimiter="\t")

    time_ini = datetime.datetime.now()

    for file in os.listdir("pruebas/"+path+"/base"):
        matches = np.zeros(2)
        base_desc = np.load("pruebas/"+path+"/base/"+file)
        for base_frame in base_desc:
            min_dist = float("inf")
            best_com = ""
            best_frame = 0
            for com in comerciales:
                i = 0
                for frame in com[2]:
                    dist = cv2.norm(base_frame, frame, cv2.NORM_L1)
                    if(dist <= min_dist):
                        min_dist = dist
                        best_com = com[0]
                        best_frame = i
                    i+= 1

            matches = np.vstack((matches, [best_com, best_frame]))

    time_end = datetime.datetime.now()
    np.save("pruebas/"+path+"/matches.npy",matches[1:].astype(int))
    np.savetxt("pruebas/"+path+"/compare_time.txt", [str(time_end-time_ini)], fmt="%s")

if len(sys.argv) > 1:
    compare(sys.argv[1])
else:
    for file in os.listdir("pruebas"):
        compare(file)





