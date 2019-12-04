import serial
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import re
arduino = serial.Serial('COM14',
                     baudrate=9600,
                     bytesize=serial.EIGHTBITS,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     timeout=1,
                     xonxoff=0,
                     rtscts=0
                     )
# Toggle DTR to reset Arduino
sigma = 50
np.random.seed(57)
vals1 = np.random.normal(100,100+sigma,250)
vals1 = np.abs(vals1)
vals2 = np.random.normal(100,100+sigma,250)
vals2 = np.abs(vals2)
output = []
print(vals1.shape)
# exit()

def reset():
    arduino.setDTR(False)
    time.sleep(1)
    # toss any data already received, see
    # http://pyserial.sourceforge.net/pyserial_api.html#serial.Serial.flushInput
    arduino.flushInput()
    arduino.setDTR(True)

prime = 3
pi_approx = 3

primes = []
pis = []

dat=[0,1]
fig = plt.figure()
ax = fig.add_subplot(111)
# Ln, = ax.plot(dat)
# ax.set_xlim([0,20])
# plt.ion()
# plt.show()   

def animate(i):
        global prime
        global pi_approx
        global pis
        global primes
        running = True
        point = [0,0,0,0]
        start = time.time()
        while running:
            text = arduino.readline().decode()
            # if(len(text) > 0): print(text.strip())
            if abs(time.time() - start) > 10:
                running = False
                print("Failed")
            if "Init" in text:
                # print(i)
                arduino.write("{}\r\n".format(prime).encode())
                time.sleep(0.5)
                print("Testing {}\r\n".format(round(1/(pi_approx/2),9)).encode())
                arduino.write("{}\r\n".format(round(1/(pi_approx/2),9)).encode())
                time.sleep(0.5)
                
            elif "prime" in text:
                results = text.split(" ")
                if len(results) == 2:
                    tot = abs(time.time() - start)
                    point[0] = int(results[1])
                    prime = point[0]
                    point[1] = tot
            elif "PI" in text:
                text2 = arduino.readline().decode()
                # results = text.split(" ")
                pi_approx = float(text2)
                if len(results) == 2:
                    tot = abs(time.time() - start)
                    point[2] = pi_approx
                    point[3] = tot
            else:
                print(text)
            if 0 not in point: 
                running = False
                output.append(point)
                primes.append(prime)
                pis.append(pi_approx)
                ax.clear()
                ax.plot(pis)
                ax.plot([0,len(pis)],[3.141592654,3.141592654],'r-', ls='--')
                # ax.annotate("Latest Prime: {}".format(prime), (len(pis)-1,pi_approx))
                plt.title("Approximating Pi")
                plt.xlabel("Latest Prime: {}".format(prime))
                plt.ylim([2.5,3.5])
                # print(i,point)
        reset()
            # print(arduino.readline().decode())
            # reset()
# np.savetxt("FIFO_10percent.csv", output, '%.1e', delimiter=',')
# cols = ["T1_CPU","T1_Time","T2_CPU","T2_Time"]
# df = pd.DataFrame.from_records(output,columns=cols)
# df.to_csv("SRF_{}percent.csv".format(sigma))

ani = animation.FuncAnimation(fig,animate,interval=1000)
plt.show()