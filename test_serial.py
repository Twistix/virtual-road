import serial
import time

com = "COM5" #input("Quel COM ?\n")
ser = serial.Serial(com, timeout=0.1)       # ouverture du port serie

for _ in range(200):
    if ser.inWaiting()>0 :
        print(ser.readline())
    print('lol')
    time.sleep(0.05)
