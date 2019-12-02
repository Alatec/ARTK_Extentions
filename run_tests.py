import serial
import numpy as np
import pandas as pd
import time
import re
arduino = serial.Serial('COM6',
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

with arduino:
    for i in range(len(vals1)):
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
                arduino.write("{}\r\n".format(int(vals1[i])).encode())
                arduino.write("{}\r\n".format(int(vals2[i])).encode())
                
            elif "T1" in text:
                results = text.split(" ")
                if len(results) == 2:
                    tot = abs(time.time() - start)
                    point[0] = int(results[1])
                    point[1] = tot
            elif "T2" in text:
                results = text.split(" ")
                if len(results) == 2:
                    tot = abs(time.time() - start)
                    point[2] = int(results[1])
                    point[3] = tot
                    
            if 0 not in point: 
                running = False
                output.append(point)
                print(i,point)
        reset()
            # print(arduino.readline().decode())
            # reset()
# np.savetxt("FIFO_10percent.csv", output, '%.1e', delimiter=',')
cols = ["T1_CPU","T1_Time","T2_CPU","T2_Time"]
df = pd.DataFrame.from_records(output,columns=cols)
df.to_csv("SRF_{}percent.csv".format(sigma))