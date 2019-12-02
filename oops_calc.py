import numpy as np
import matplotlib.pyplot as plt
sigma = 25
np.random.seed(57)
vals1 = np.random.normal(100,100+sigma,250)
# vals1 = np.abs(vals1)
vals2 = np.random.normal(100,100+sigma,250)
# vals2 = np.abs(vals2)

print(vals1.mean(), vals1.std(), vals1.astype(int).mean(), vals1.astype(int).std())
print(vals2.mean(), vals2.std(), vals2.astype(int).mean(), vals2.astype(int).std())

fig, ax = plt.subplots(2,2,sharex=True,sharey=True)

ax[0][0].boxplot(vals1.astype(int))
ax[0][1].boxplot(np.abs(vals1.astype(int)))
ax[1][0].boxplot(vals2.astype(int))
ax[1][1].boxplot(np.abs(vals2.astype(int)))
plt.show()