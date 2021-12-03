from microbit import *
import machine
import time
import MaqueenPlus as mqpbot


mqp = mqpbot.MaqueenPlus()

def D_Servo():
    mqp.servo(1, 20)
    sleep(500)
    mqp.servo(1, 110)
    return

def D_Forward():
    mqp.motor(1, 100, 1, 100)
    mqp.RGB(2, 2)
    return


def D_ForwardR():
    mqp.motor(1, 100, 1, 40)
    mqp.RGB(2, 2)
    return


def D_ForwardL():
    mqp.motor(1, 40, 1, 100)
    mqp.RGB(2, 2)
    return


def D_Back():
    mqp.motor(2, 100, 2, 100)
    mqp.RGB(2, 2)
    return

def D_BackR():
    mqp.resetMotorCounter()
    mqp.motor(2, 100, 2, 40)
    mqp.RGB(2, 2)
    return

def D_BackL():
    mqp.motor(2, 40, 2, 100)
    mqp.RGB(2, 2)
    return

def D_Right():
    mqp.motor(1, 100, 1, 0)
    mqp.RGB(2, 2)
    return

def D_Left():
    mqp.motor(1, 0, 1, 100)
    mqp.RGB(2, 2)
    return

def D_Stop():
    mqp.motor(1, 0, 1, 0)
    mqp.RGB(1, 1)
    return

def D_Objavoid():
    mqp.motor(2, 40, 2, 40)
    sleep(1000)
    return

def P_Forward():
    mqp.motor(1, 100, 1, 100)
    sleep(500)
    mqp.motor(1, 0, 1, 0)
    sleep(500)
    return

def P_Back():
    mqp.motor(2, 100, 2, 100)
    sleep(500)
    mqp.motor(1, 0, 1, 0)
    sleep(500)
    return

def P_Left():
    mqp.motor(2, 50, 1, 50)
    sleep(900)
    mqp.motor(1, 0, 1, 0)
    return


def P_Right():
    mqp.motor(1, 50, 2, 50)
    sleep(900)
    mqp.motor(1, 0, 1, 0)
    return

def L_Right():
    mqp.motor(1, 50, 2, 50)
    sleep(600)
    mqp.motor(1, 0, 1, 0)
    return

def L_Left():
    mqp.motor(2, 50, 1, 50)
    sleep(600)
    mqp.motor(1, 0, 1, 0)
    return
