from microbit import *
import machine
import time
import radio
import MaqueenPlus as mqpbot
import Direction

radio.config(channel=7, group=0, queue=1)
radio.on()

mqp = mqpbot.MaqueenPlus()

Drivingmode = 1
Linemode = 2
ProgramMode = 3
mode = 1
numCommands = 0
obj_avoidance = 'on'

def Driving(radiodata):
    display.show('D')
    firstLetter = radiodata[0]
    if firstLetter == 'L':
        if radiodata == 'Left':
            Direction.D_Left()
    if firstLetter == 'F':
        if radiodata == 'Forward':
            Direction.D_Forward()
        elif radiodata == 'Forward_R':
            Direction.D_ForwardR()
        elif radiodata == 'Forward_L':
            Direction.D_ForwardL()
    if firstLetter == 'B':
        if radiodata == 'Back':
            Direction.D_Back()
        elif radiodata == 'Back_R':
            Direction.D_BackR()
        elif radiodata == 'Back_L':
            Direction.D_BackL()
    if firstLetter == 'R':
        if radiodata == 'Right':
            Direction.D_Right()
    if radiodata == 'E':
        Direction.D_Servo()
    if radiodata == "STOP":
        Direction.D_Stop()


def Line(radiodata):
    retArray = mqp.lineSense()
    display.show('L')
    if retArray == [0, 0, 0, 0, 0, 0]:
        mqp.motor(1, 0, 1, 0)
    elif retArray[2] and retArray[3]:
        mqp.motor(1, 50, 1, 50)
    elif retArray[1] and retArray[2]:
        mqp.motor(1, 30, 1, 60)
    elif retArray[3] and retArray[4]:
        mqp.motor(1, 60, 1, 30)
    elif retArray[0]:
        mqp.motor(2, 20, 1, 90)
        sleep(500)
    elif retArray[5]:
        mqp.motor(1, 90, 2, 20)
        sleep(500)
    elif retArray[4]:
        mqp.motor(1, 60, 2, 30)
    elif retArray[2]:
        mqp.motor(1, 50, 1, 50)
    elif retArray[3]:
        mqp.motor(1, 50, 1, 50)
    elif retArray[1]:
        mqp.motor(2, 30, 1, 60)
    elif retArray[0] and retArray[2] and retArray[3] and retArray[5]:
        radio.send('?')
        mqp.motor(1, 0, 1, 0)
        if radio.receive() == 'Right':
            Direction.L_Right()
        elif radio.receive() == 'Forward':
            mqp.motor(1, 50, 1, 50)
            sleep(1000)
        elif radio.receive() == 'Left':
            Direction.L_Left()
    elif retArray[0] and retArray[5]:
        mqp.motor(1, 0, 1, 0)
        radio.send('?')
        if radio.receive() == 'Right':
            Direction.L_Right()
        elif radio.receive() == 'Left':
            Direction.L_Left()
    elif retArray[5] and retArray[2] and retArray[3]:
        mqp.motor(1, 0, 1, 0)
        radio.send('?')
        if radio.receive() == 'Right':
            Direction.L_Right()
        elif radio.receive() == 'Forward':
            mqp.motor(1, 50, 1, 50)
    elif retArray[0] and retArray[2] and retArray[3]:
        mqp.motor(1, 0, 1, 0)
        radio.send('?')
        if radio.receive() == 'Left':
            Direction.L_Left()
        elif radio.receive() == 'Forward':
            mqp.motor(1, 50, 1, 50)


def Program(radiodata):
    display.show('P')
    numCommands = len(radiodata)
    for inx in range(numCommands):
        if radiodata[inx] == 'F':
            Direction.P_Forward()
            continue
        if radiodata[inx] == 'R':
            Direction.P_Right()
            continue
        if radiodata[inx] == 'B':
            Direction.P_Back()
            continue
        if radiodata[inx] == 'L':
            Direction.P_Left()
            continue

while True:
    radiodata = radio.receive()
    if mode == 1:
        if not radiodata:
            continue
        if radiodata == 'off':
            obj_avoidance = 'off'
            continue
        if obj_avoidance == 'on':
            dist = round(pin1.read_analog() * 520 / 1023, 1)
            if dist < 30:
                Direction.D_Objavoid()
                continue
        if radiodata == 'Line':
            mode = 2
        Driving(radiodata)
    if mode == 2:
        if radiodata == 'Programming':
            mode = 3
        Line(radiodata)
    if mode == 3:
        if not radiodata:
            continue
        if radiodata == 'Driving':
            mode = 1
        Program(radiodata)
