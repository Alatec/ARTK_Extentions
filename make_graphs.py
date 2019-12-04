import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sjf10 = pd.read_csv("SJF_10percent.csv", index_col=0)
sjf25 = pd.read_csv("SJF_25percent.csv", index_col=0)
sjf50 = pd.read_csv("SJF_50percent.csv", index_col=0)

srf10 = pd.read_csv("SRF_10percent.csv", index_col=0)
srf25 = pd.read_csv("SRF_25percent.csv", index_col=0)
srf50 = pd.read_csv("SRF_50percent.csv", index_col=0)

fifo10 = pd.read_csv("FIFO_10percent.csv", index_col=0)
fifo25 = pd.read_csv("FIFO_25percent.csv", index_col=0)
fifo50 = pd.read_csv("FIFO_50percent.csv", index_col=0)

switch10 = pd.read_csv("SWITCH_10percent.csv", index_col=0)
switch25 = pd.read_csv("SWITCH_25percent.csv", index_col=0)
switch50 = pd.read_csv("SWITCH_50percent.csv", index_col=0)

fig, ax = plt.subplots(4,1,sharex=True,sharey=True)

bin_num=10

ax[0].hist(sjf50[["T2_Time","T1_Time"]].max(axis=1), bins=bin_num, normed=True)
ax[1].hist(srf50[["T2_Time","T1_Time"]].max(axis=1), bins=bin_num, normed=True)
ax[2].hist(fifo50[["T2_Time","T1_Time"]].max(axis=1), bins=bin_num, normed=True)
ax[3].hist(switch50[["T2_Time","T1_Time"]].max(axis=1), bins=bin_num,normed=True)

ax[0].set_title("SJF")
ax[1].set_title("SRF")
ax[2].set_title("FIFO")
ax[3].set_title("SWITCH")

plt.show()

