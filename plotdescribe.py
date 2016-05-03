import cv2
import sys
import os
import csv
import datetime
import time
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o



def barplot(ax, dpoints, label, max_y, primero=False):
    '''
    Create a barchart for data across different categories with
    multiple conditions for each category.

    @param ax: The plotting axes from matplotlib.
    @param dpoints: The data set as an (n, 3) numpy array
    '''

    # Aggregate the conditions and the categories according to their
    # mean values
    conditions = [(c, np.mean(dpoints[dpoints[:, 0] == c][:, 2].astype(float)))
                  for c in np.unique(dpoints[:, 0])]
    categories = [(c, np.mean(dpoints[dpoints[:, 1] == c][:, 2].astype(float)))
                  for c in np.unique(dpoints[:, 1])]

    # sort the conditions, categories and data so that the bars in
    # the plot will be ordered by category and condition
    conditions = [c[0] for c in sorted(conditions, key=o.itemgetter(1))]
    categories = [c[0] for c in sorted(categories, key=o.itemgetter(1))]

    dpoints = np.array(sorted(dpoints, key=lambda x: categories.index(x[1])))

    # the space between each set of bars
    space = 0.3
    n = len(conditions)
    width = (1 - space) / (len(conditions))

    # Create a set of bars at each position
    for i, cond in enumerate(conditions):
        indeces = range(1, len(categories) + 1)
        vals = dpoints[dpoints[:, 0] == cond][:, 2].astype(np.float)
        pos = [j - (1 - space) / 2. + i * width for j in indeces]
        ax.bar(pos, vals, width=width, label=cond,
               color=cm.Accent(float(i) / n))

    # Set the x-axis tick labels to be equal to the categories
    ax.set_xticks(indeces)
    ax.set_xticklabels(categories)
    plt.setp(plt.xticks()[1], rotation=90)

    # Add the axis labels
    if primero: ax.set_ylabel("Tiempo[m]")
    ax.set_xlabel("Zonas")
    ax.set_title(label)

    # Add a legend
    if primero:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], loc='upper left', title="Bins")

    ax.set_ylim([0, max_y])
    ax.grid(True)


data = np.zeros(4)
max_minutos = 0

for file in os.listdir("pruebas"):
    with open("pruebas/" + file + "/metadata.csv", "rb") as csv_metadata:
        metadatareader = csv.reader(csv_metadata, delimiter=",")
        (next(metadatareader))
        line = (next(metadatareader))
        [fps, z, bins, _, tiempo] = line
        z = z.strip("()").split(",")
        tiempo = time.strptime(tiempo.split('.')[0], '%H:%M:%S')
        minutos = datetime.timedelta(minutes=tiempo.tm_min, seconds=tiempo.tm_sec).total_seconds() / 60
        if minutos > max_minutos: max_minutos = minutos
        data = np.vstack((data, np.array([fps, bins, str(z[0]) + "x" + str(z[1]), minutos])))

data = data[1:]

freqs = np.unique(data[:, 0])

fig = plt.figure()

for i, f in enumerate(freqs):
    subdata = data[data[:, 0] == f][:, 1:]
    print f
    print subdata

    barplot(fig.add_subplot(1, len(freqs), len(freqs) - i), subdata, "1 descriptor cada " + str(f) + " frames",
            max_minutos+5 , i == len(freqs) - 1)
plt.show()
