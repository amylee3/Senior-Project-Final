from microbit import *
import struct
import time

I2caddr = 0x10


class MaqueenPlus:

    lineSensors = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20]
    offsetL = 0
    offsetR = 0
    debug = False
    blinkEndTime = 0
    blinkState = False
    isBlinking = False
    blinkCounter = 1

    # initialize object
    def __init__(self):
        self.offsetL = 0
        self.offsetR = 0
        self.resetMotorCounter()
        self.blinkEndTime = 0
        return

    def blink44(self, delay=150, repeat=1):
        display.set_pixel(4, 4, 5)
        self.blinkEndTime = time.ticks_ms() + delay
        self.blinkState = True
        self.isBlinking = True
        self.blinkCounter = repeat
        return

    def blinkTick(self):
        if not self.isBlinking:
            return
        if time.ticks_ms() > self.blinkEndTime:
            self.blinkState = not self.blinkState
            self.isBlinking = False
            if self.blinkState:
                display.set_pixel(4, 4, 5)
            else:
                display.set_pixel(4, 4, 0)
            return
        return

    # index：corresponds to the servo interface 1-3
    # servo 1 = 0x14
    # angle：Servo angle
    def servo(self, index, angle):
        if index not in range(1, 3):
            return False
        buf = bytearray(2)
        buf[0] = 0x13 + index
        buf[1] = angle
        try:
            i2c.write(I2caddr, buf)
        except OSError:
            display.clear()
            display.show("I2C NA 1", wait=False, loop=False)
            return False

        return True

    # Maqueen Plus motor control
    # direction:1 forward  2 back
    # speed：0~255
    def motor(self, directionL, speedL, directionR, speedR):
        buf = bytearray(5)
        buf[0] = 0x00
        buf[1] = directionL
        buf[2] = speedL
        buf[3] = directionR
        buf[4] = speedR
        try:
            i2c.write(I2caddr, buf)
        except OSError:
            display.clear()
            display.show("I2C NA 2", wait=False, loop=False)

        return

    #
    # Get the motor speed
    # Return left motor speed, right motor speed
    def motorSpeed(self):
        buf = bytearray(1)
        buf[0] = 0
        try:
            i2c.write(I2caddr, buf)
        except OSError:
            display.clear()
            display.show("I2C NA 3", wait=False, loop=False)
            return 0, 0

        motorSpeed_d = struct.unpack(">BBBB", i2c.read(I2caddr, 8))
        return motorSpeed_d[1], motorSpeed_d[3]

    # Get rotation counter for motors:
    # Return left motor, right motor
    def motorRotations(self):
        buf = bytearray(1)
        buf[0] = 0
        try:
            i2c.write(I2caddr, buf)
            motorSpeed_d = struct.unpack(">BBBBBBBB", i2c.read(I2caddr, 8))
        except OSError:
            display.clear()
            display.show("I2C NA 4", wait=False, loop=False)
            return 0, 0

        # return motorSpeed_d[5] - self.offsetL, motorSpeed_d[7] - self.offsetR
        return motorSpeed_d[5], motorSpeed_d[7]

    # Reset motor counter
    # Brute force - read offsets and subtract from future motorRotations calls
    def resetMotorCounter(self):
        buf = bytearray(1)
        buf[0] = 0
        try:
            i2c.write(I2caddr, buf)
            motorSpeed_d = struct.unpack(">BBBBBBBB", i2c.read(I2caddr, 8))
        except OSError:
            display.clear()
            display.show("I2C NA 5", wait=False, loop=False)
            return

        self.offsetL = motorSpeed_d[5]
        self.offsetR = motorSpeed_d[7]
        if self.debug:
            display.scroll(self.offsetL)
            display.scroll(self.offsetR)
        return

    # Get the motor direction
    # State:0=stop;1=forward;2=reverse
    # Return left motor direction, right motor direction
    def motorDirection(self, direction):
        buf = bytearray(1)
        buf[0] = 0
        try:
            i2c.write(I2caddr, buf)
            motorSpeed_d = struct.unpack(">BBBB", i2c.read(I2caddr, 8))
        except OSError:
            display.clear()
            display.show("I2C NA 6", wait=False, loop=False)
            return 0, 0

        return motorSpeed_d[0], motorSpeed_d[2]

    # Corresponding sensor parameter： L3:1, L2:2, L1:3, R1:4, R2:5, R3:6
    # Return all sensor data as above
    def lineSense(self):
        index = 0
        retarray = [0, 0, 0, 0, 0, 0]
        buf = bytearray(1)
        buf[0] = 0x1D
        try:
            i2c.write(I2caddr, buf)
            line_d = struct.unpack("b", i2c.read(I2caddr, 1))
        except OSError:
            display.clear()
            display.show("I2C NA 7", wait=False, loop=False)
            return retarray

        for index in range(6):
            retarray[index] = line_d[0] & self.lineSensors[index]
        return retarray

    # Corresponding sensor parameter： L3:1, L2:2, L1:3, R1:4, R2:5, R3:6
    # Sensor greyscale for all sensors
    def grayscaleValue(self):
        retarray = [0, 0, 0, 0, 0, 0]
        buf = bytearray(1)
        buf[0] = 0x1E
        i2c.write(I2caddr, buf)
        grayscaleValue_d = struct.unpack(">HHHHHH", i2c.read(I2caddr, 12))
        for index in range(6):
            retarray[index] = grayscaleValue_d[index]
        return retarray

    # Each number represents a color,
    # and color out of the RGB color range cannot be displayed.
    # RGB color range 1~7
    def RGB(self, colourL, colourR):
        buf = bytearray(3)
        buf[0] = 0x0B
        buf[1] = colourL
        buf[2] = colourR
        try:
            i2c.write(I2caddr, buf)
        except OSError:
            display.clear()
            display.show("I2C NA 8", wait=False, loop=False)

        return

    # PID parameters open:0 close:1
    def PID(self, switch):
        buf = bytearray(2)
        buf[0] = 0x0A
        buf[1] = switch
        try:
            i2c.write(I2caddr, buf)
        except OSError:
            display.clear()
            display.show("I2C NA 9", wait=False, loop=False)

        return
