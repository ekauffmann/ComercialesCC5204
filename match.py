import os
import cv2
import numpy as np
import math
tolerance = 0.8

def myHamming(a1, a2):
    dist = 0
    for index in range(len(a1)):
        if a1[index][0] != a2[index][0] or a1[index][1] != a2[index][1]:
            dist+=1
    return dist

def prettyTime(s):
    secs = s
    hours = int(secs/3600)
    secs -= hours*3600
    mins = int(secs/60)
    secs -= mins*60
    return str(hours)+":"+str(mins)+":"+str(secs)

dict = np.loadtxt("pruebas/f30z2,2b32/comercial_dict.txt",
                  dtype={'names': ['id', 'name', 'frame_count'],
                         'formats': ['i', 'S32', 'i']}, delimiter="\t")

masks = []
for com in dict:
    a = [com[0]]*com[2]
    b = range(0, com[2])
    asd = np.transpose(np.array([a,b]))
    masks += [np.transpose(np.array([a,b]))]

matches = np.load("pruebas/f30z2,2b32/matches.npy")

i = 0
while i < len(matches):
    com_id = matches[i][0]
    best_frame = matches[i][1]
    if (i + dict[com_id]['frame_count'] >= len(matches)) or best_frame > i:
        i+=1
        continue
    mask = masks[com_id]
    window = matches[i-best_frame:i-best_frame+dict[com_id]['frame_count']]
    dist = myHamming(mask,window)
    if(dist <= dict[com_id]['frame_count']*tolerance):
        print prettyTime(i*30/29.97)+" "+dict[com_id]['name'] +" " +str(matches[i]) + str(dist) + " "+str(dict[com_id]['frame_count'])
        i = i-best_frame+dict[com_id]['frame_count']
    i+=1
