from microbit import *
import machine
import time
import radio
import array
import Controller


radio.config(channel=7, group=0, queue=1)
radio.on()


ctrl = Controller.Controller()
codeArray = [None] * 10
codeInx = 0
DrivingMode = 1
LineMode = 2
ProgramMode = 3
mode = 1
High = 650
Low = 450
wait_sleep = 1000
debounce = 300

while True:
    if mode == 1:
        if button_a.is_pressed():
            display.show('L')
            sleep(wait_sleep)
            radio.send('Line')
            mode = 2

        if button_b.is_pressed():
            radio.send('off')
            display.show('off', wait=True)

        elif ctrl.Yvalue() < Low and ctrl.Xvalue() > Low and ctrl.Xvalue() < High:
            display.show(Image.ARROW_S)
            radio.send('Back')
        elif ctrl.Xvalue() > High and ctrl.Yvalue() > Low and ctrl.Yvalue() < High:
            display.show(Image.ARROW_E)
            radio.send('Right')
        elif ctrl.Xvalue() < Low and ctrl.Yvalue() > Low and ctrl.Yvalue() < High:
            display.show(Image.ARROW_W)
            radio.send('Left')
        elif ctrl.Yvalue() > High and ctrl.Xvalue() > Low and ctrl.Xvalue() < High:
            display.show(Image.ARROW_N)
            radio.send('Forward')
        elif ctrl.Yvalue() < Low and ctrl.Xvalue() > High:
            display.show(Image.ARROW_SE)
            radio.send('Back_R')
        elif ctrl.Yvalue() < Low and ctrl.Xvalue() < Low :
            display.show(Image.ARROW_SW)
            radio.send('Back_L')
        elif ctrl.Yvalue() > High and ctrl.Xvalue() > High:
            display.show(Image.ARROW_NE)
            radio.send('Forward_R')
        elif ctrl.Yvalue() > High and ctrl.Xvalue() < Low :
            display.show(Image.ARROW_NW)
            radio.send('Forward_L')
        elif ctrl.ButtonE():
            display.show('E')
            radio.send('E')
        else:
            display.clear()
            radio.send("STOP")

    if mode == 2 :
        if button_a.is_pressed():
            display.show('P')
            sleep(wait_sleep)
            radio.send('Programming')
            mode = 3

        if radio.receive() == '?':
            display.show('?', delay=500, wait=True)
            if ctrl.Xvalue() > High and ctrl.Yvalue() > Low and ctrl.Yvalue() < High:
                display.show(Image.ARROW_E)
                radio.send('Right')
            elif ctrl.Xvalue() < Low and ctrl.Yvalue() > Low and ctrl.Yvalue() < High:
                display.show(Image.ARROW_W)
                radio.send('Left')
            elif ctrl.Yvalue() > High and ctrl.Xvalue() > Low and ctrl.Xvalue() < High:
                display.show(Image.ARROW_N)
                radio.send('Forward')
        else:
            display.clear()

    if mode == 3:
        if button_a.is_pressed():
            display.show('D')
            sleep(wait_sleep)
            radio.send('Driving')
            mode = 1

        if button_b.is_pressed():
            string = ''
            for x in codeArray:
                if x is None:
                    break
                string = string + x
            radio.send(string)
            sleep(wait_sleep)
            codeArray = [None] * 10
            codeInx = 0
            continue

        if codeInx > 9:
            display.scroll('ERROR', loop=False)
            codeArray = [None] * 10
            codeInx = 0
            continue
        if ctrl.ButtonE():
            codeArray[codeInx] = 'F'
            codeInx = codeInx + 1
            sleep(debounce)
            continue
        elif ctrl.ButtonD():
            codeArray[codeInx] = 'R'
            codeInx = codeInx + 1
            sleep(debounce)
            continue
        elif ctrl.ButtonC():
            codeArray[codeInx] = 'B'
            codeInx = codeInx + 1
            sleep(debounce)
            continue
        elif ctrl.ButtonF():
            codeArray[codeInx] = 'L'
            codeInx = codeInx + 1
            sleep(debounce)
            continue

        display.show(codeInx, delay=500, wait=True)

