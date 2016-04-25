import os
import csv
import cv2
import numpy as np

comerciales = []
for file in os.listdir("descriptores/f30z2,2b32/comerciales"):
    with open("descriptores/f30z2,2b32/comerciales/"+file, "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        frames = [map(float,item) for item in reader]
        comercial = [[file, frames]]
        comerciales += comercial
        csvfile.close()

for file in os.listdir("descriptores/f30z2,2b32/base"):
    with open("descriptores/f30z2,2b32/matches.csv", "wb") as matches:
        writer = csv.writer(matches, delimiter= ",")
        with open("descriptores/f30z2,2b32/base/"+file, "rb") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            count = 0
            for line in reader:
                if count%500==0: print count
                base_frame = [float(item) for item in line]
                min_dist = float("inf")
                best_com = ""
                best_frame = 0
                for com in comerciales:
                    i = 0
                    for frame in com[1]:
                        dist = cv2.norm(np.array(base_frame), np.array(frame), cv2.NORM_L1)
                        if(dist < min_dist):
                            min_dist = dist
                            best_com = com[0]
                            best_frame = i
                        i+= 1

                writer.writerow([count]+[best_com]+[best_frame])
                count+=1

            csvfile.close()
        matches.close()



