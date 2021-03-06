import numpy as np
import sys

freq = int(sys.argv[1])
zonas = (int(sys.argv[2]), int(sys.argv[3]))
bins = int(sys.argv[4])
dims = (720,400)
fps = 29.97002997

config= "freq%szone%s,%sbins%s" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

tolerance = float(sys.argv[5])/100

def myHamming(a1, a2):
    dist = 0
    for index in range(len(a1)):
        if a1[index][0] != a2[index][0] or a1[index][1] != a2[index][1]:
            dist+=1
    return dist

def prettyTime(s):
    mins, secs = divmod(s, 60)
    hours, mins = divmod(mins, 60)
    return "%d:%02d:%02d" % (hours, mins, secs)

dict = np.loadtxt("pruebas/" + config + "/comercial_dict.txt",
                  dtype={'names': ['id', 'name', 'frame_count'],
                         'formats': ['i', 'S32', 'i']}, delimiter="\t")

masks = []
times = []
count= np.zeros(len(dict))

for com in dict:
    a = [com[0]]*com[2]
    b = range(0, com[2])
    masks += [np.transpose(np.array([a,b]))]
    times += [[]]


matches = np.load("pruebas/" + config + "/matches.npy")

i = 0
with open("pruebas/"+config+"/playlist.m3u", 'w') as pls:

    while i < len(matches):

        com_id = matches[i][0]
        best_frame = matches[i][1]
        if (i + dict[com_id]['frame_count'] >= len(matches)) or best_frame > i:
            i+=1
            continue
        mask = masks[com_id]
        window = matches[i-best_frame:i-best_frame+dict[com_id]['frame_count']]
        dist = myHamming(mask,window)
        com_fc = dict[com_id]['frame_count']
        if(dist <= com_fc*tolerance):
            count[com_id]+=1
            times[com_id]+= [i-best_frame]
            #print "%s %s %s %d %d" % (prettyTime(i*30/29.97), dict[com_id]['name'], str(matches[i]), dist, com_fc)
            print str((i-best_frame)*freq/fps) + " "+ str((i-best_frame+com_fc)*freq/fps) + " " + dict[com_id]['name']
            pls.write("#EXTVLCOPT:start-time=%d\n" % ((i-best_frame)*freq/fps))
            pls.write("#EXTVLCOPT:stop-time=%d\n" % ((i-best_frame+com_fc-1)*freq/fps))
            pls.write("../../base/mega-2014_04_25T22_00_07.mp4\n")
            i = i-best_frame+com_fc

        i+=1

with open("pruebas/"+config+"/ocurrencias"+str(tolerance)+".txt", 'w') as oc:
    oc.write(str(np.sum(count).astype(int)) + " ocurrencias"+"\n")
    for i in range(len(dict)):
        oc.write("%s %d" % (dict[i]['name'], count[i])+"\n")
        for j in times[i]:
            oc.write("\t" + str(j*freq/fps) + "\t-> " + str(prettyTime(j*freq/fps))+"\n")