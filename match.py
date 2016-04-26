import numpy as np
tolerance = 0.8

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
count= np.zeros(len(dict))

while i < len(matches):

    com_id = matches[i][0]
    best_frame = matches[i][1]
    if (i + dict[com_id]['frame_count'] >= len(matches)) or best_frame > i:
        i+=1
        continue
    mask = masks[com_id]
    window = matches[i-best_frame:i-best_frame+dict[com_id]['frame_count']]
    dist = myHamming(mask,window)
    thisCom_framecount = dict[com_id]['frame_count']
    if(dist <= thisCom_framecount*tolerance):
        count[com_id]+=1
        print "%s %s %s %d %d" % (prettyTime(i*30/29.97), dict[com_id]['name'], str(matches[i]), dist, thisCom_framecount)
        i = i-best_frame+thisCom_framecount
    i+=1

for i in range(len(dict)):
    print "%s %d" % (dict[i]['name'], count[i])

print np.sum(count).astype(int)
