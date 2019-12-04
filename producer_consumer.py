import numpy as np
import matplotlib.pyplot as plt

def next_prime(curr):
    next = 0
    curr += 1
    while next == 0:
        for i in range(2,curr):
            if curr % i == 0:
                break
            elif i == curr-1:
                next = curr
                break
        curr += 1
    return next


def next_val(num):
    vals = np.zeros(num, dtype=np.int)
    recips = np.zeros_like(vals, dtype=np.float)

    for i, val in enumerate(vals):
        if i == 0:
            vals[i] = 3
        else:
            vals[i] = next_prime(vals[i-1])

        if vals[i] % 4 == 3:
            recips[i] = -1*float(vals[i])
        else:
            recips[i] = float(vals[i])


    recips = 1. + 1/recips

    return (1/np.prod(recips))*2

a = []
for i in range(1,10):
    a.append(next_val(i))

plt.plot(a)
plt.show()

print(next_val(1000))