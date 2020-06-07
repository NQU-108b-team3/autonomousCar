import RPi.GPIO as gpio
import numpy as np
import time

def movDir(gpio, mP, dir):
    # forward, left, right, stop
    mv = ('0101', '0001', '0100', '0000')
    m = mv[dir]
    for i in range(4):
        if m[i] == '1':
            gpio.output(mP[i], gpio.HIGH)
        elif m[i] == '0':
            gpio.output(mP[i], gpio.LOW)

def right(gpio, mP):
    movDir(gpio, mP, 2)
    time.sleep(0.3)
    movDir(gpio, mP, 3)

def left(gpio, mP):
    movDir(gpio, mP, 1)
    time.sleep(0.3)
    movDir(gpio, mP, 3)

def forward(gpio, mP):
    movDir(gpio, mP, 0)
    time.sleep(0.11)
    movDir(gpio, mP, 0)
    time.sleep(0.01)
    movDir(gpio, mP, 3)

def changeP(mqttClient, gpio, currentP, dis, moveSet, mP):
    for i in range(dis * 5):
        forward(gpio, mP)
        
        if i % 5 == 0:
            currentP = (currentP[0] - moveSet[0], currentP[1] - moveSet[1])
            msg = str(currentP)
            mqttClient.publish("test/CurrP", msg)
    return currentP

def getDis(moveSet):
    dis = moveSet[0] if moveSet[0] != 0 else moveSet[1]
    dis *= -1 if dis < 0 else 1
    return dis

def getStep(moveSet):
    verti, hori = (moveSet[0], moveSet[1])
    if moveSet[0] != 0:
        verti = 1 if moveSet[0] > 0 else -1
    if moveSet[1] != 0:
        hori = 1 if moveSet[1] > 0 else -1
    return (verti, hori)

def mov(mqttClient, currentP, viaPath):
    mP = (11, 12, 13, 15)
    gpio.setmode(gpio.BOARD)
    gpio.setup(mP, gpio.OUT)

    previousP = currentP
    for i in range(len(viaPath)):
        nextP = viaPath[i]
        print("Previous position: ", previousP)
        print("Current position: ", currentP)
        print("Next position: ", nextP)

        vFrom = (previousP[0] - currentP[0], previousP[1] - currentP[1])
        vTo = (nextP[0] - currentP[0], nextP[1] - currentP[1])

        ans = np.cross(vTo, vFrom)
        if ans > 0:
            left(gpio, mP)
        elif ans < 0:
            right(gpio, mP)

        previousP = currentP

        moveSet = (currentP[0] - nextP[0], currentP[1] - nextP[1])
        dis = getDis(moveSet)
        moveSet = getStep(moveSet)
        currentP = changeP(mqttClient, gpio, currentP, dis, moveSet, mP)
    
    gpio.cleanup()

    return currentP
