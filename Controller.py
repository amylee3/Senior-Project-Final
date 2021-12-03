# Write your code here :-)
from microbit import *

class Controller:

    def __init__(self):
        pin16.set_pull(pin16.PULL_UP)
        pin15.set_pull(pin15.PULL_UP)
        pin14.set_pull(pin14.PULL_UP)
        pin13.set_pull(pin13.PULL_UP)
        pin8.set_pull(pin8.PULL_UP)
        pin2.set_pull(pin2.NO_PULL)
        pin1.set_pull(pin1.NO_PULL)

    def ButtonF(self):
        return not pin16.read_digital()

    def ButtonE(self):
        return not pin15.read_digital()

    def ButtonD(self):
        return not pin14.read_digital()

    def ButtonC(self):
        return not pin13.read_digital()

    def ButtonZ(self):
        return not pin8.read_digital()

    def Xvalue(self):
        return pin1.read_analog()

    def Yvalue(self):
        return pin2.read_analog()

