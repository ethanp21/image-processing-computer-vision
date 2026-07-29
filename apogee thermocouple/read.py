import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import time

time1 = []
time10 = []
time2 = []
time20 = []
time3 = []
time30 = []

apogee = []

T1oC_grass = []
T2oC_grass = []
T3oC_grass = []
T4oC_grass = []
T5oC_grass = []
T6oC_grass = []
T7oC_grass = []

T1oC_asphalt = []
T2oC_asphalt = []
T3oC_asphalt = []
T4oC_asphalt = []
T5oC_asphalt = []
T6oC_asphalt = []
T7oC_asphalt = []


with open('2rit.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        time1.append(row[0])
        T1oC_grass.append(row[1])
        T2oC_grass.append(row[2])
        T3oC_grass.append(row[3])
        T4oC_grass.append(row[4])
        T5oC_grass.append(row[5])
        T6oC_grass.append(row[6])
        T7oC_grass.append(row[7])


with open('4rit.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        time2.append(row[0])
        T1oC_asphalt.append(row[1])
        T2oC_asphalt.append(row[2])
        T3oC_asphalt.append(row[3])
        T4oC_asphalt.append(row[4])
        T5oC_asphalt.append(row[5])
        T6oC_asphalt.append(row[6])
        T7oC_asphalt.append(row[7])

with open('2021_07_30_turfdrone.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        time3.append(row[0])
        apogee.append(row[1])

plt.figure()
plt.plot(time1, T1oC_grass, label = "Grass 1")
plt.plot(time1, T2oC_grass, label = "Grass 2") 
plt.plot(time1, T3oC_grass, label = "Grass 3") 
plt.plot(time1, T4oC_grass, label = "Grass 4") 
plt.plot(time1, T5oC_grass, label = "Grass 5") 
plt.plot(time1, T6oC_grass, label = "Grass 6") 
plt.plot(time1, T7oC_grass, label = "Grass 7")  
plt.plot(time2, T1oC_asphalt, label = "Asphalt 1")
plt.plot(time2, T2oC_asphalt, label = "Asphalt 2") 
plt.plot(time2, T3oC_asphalt, label = "Asphalt 3") 
plt.plot(time2, T4oC_asphalt, label = "Asphalt 4") 
plt.plot(time2, T5oC_asphalt, label = "Asphalt 5") 
plt.plot(time2, T6oC_asphalt, label = "Asphalt 6") 
plt.plot(time2, T7oC_asphalt, label = "Asphalt 7")
plt.plot(time3, apogee, label = "apogee")
plt.xlabel("I am x")
plt.ylabel("I am y")
ax = plt.gca()
ax.set_xticks(ax.get_xticks()[::20])
plt.xticks(rotation=90)
plt.title("With Labels")
plt.legend()
plt.tight_layout()
plt.show()

