from microbit import *
from machine import time_pulse_us
from utime import ticks_us, sleep_us, sleep_ms
import neopixel

class reromicro():

    trig = pin2
    echo = pin2
    maxCmDistance = 255

    AT24_I2C_ADDR = 80
    lineEepromAddress = 100

    rightLineSensor = pin13
    centerLineSensor = pin14
    leftLineSensor = pin15

    lineSensorPins = [leftLineSensor, centerLineSensor, rightLineSensor]
    lineSensorMax = [1500, 1500, 1500]
    lineSensorMin = [0, 0, 0]
    lineSensorValues = [0, 0, 0]
    lineSensorThreshold = [580, 580, 580]

    leftMotor = 0
    rightMotor = 1
    bothMotor = 2

    leftSensor = 0
    centerSensor = 1
    rightSensor = 2

    def __init__(self):
        pin8.set_analog_period_microseconds(256) #3.91kHz
        pin16.set_analog_period_microseconds(256)
        ui32EeData = 0
        ui32EeData = self.EE_Read32bit(self.lineEepromAddress)
        if ui32EeData == 1919251055:
            for i in range(3):
                ui32EeData = self.EE_Read32bit(self.lineEepromAddress + 4 + (i * 4))
                self.lineSensorMax[i] = ui32EeData >> 16
                self.lineSensorMin[i] = ui32EeData & 0xFFFF
                self.lineSensorThreshold[i] = ((self.lineSensorMax[i] + self.lineSensorMin[i]) >> 1) - ((self.lineSensorMax[i] - self.lineSensorMin[i]) >> 2)

    def EE_Read32bit(self,addr):
        buf = bytearray(1)
        buf[0] = addr
        i2c.write(self.AT24_I2C_ADDR,buf)
        data = i2c.read(self.AT24_I2C_ADDR,4)
        data = int.from_bytes(data, "big") # convert bytes to int with big endian
        return data

    def ReadUltrasonic(self):
        self.trig.set_pull(self.trig.NO_PULL)
        self.trig.write_digital(0)
        sleep_us(2)
        self.trig.write_digital(1)
        sleep_us(10)
        self.trig.write_digital(0)
        self.echo.read_digital()
        d = time_pulse_us(self.echo, 1, self.maxCmDistance * 38)
        if d <= 0:
            return 255

        return d//58

    def ReadLineSensors(self):
        bFlag = True
        nTimer = 1500
        nMaxTimer = 1500
        nStartTime = 0
        bPinState = 1

        for i in range(3):
            nTimer = 1500
            bFlag = True
            if ticks_us() >= 62000:
                sleep_us(4000)
            nStartTime = ticks_us()
            self.lineSensorPins[i].write_digital(1)
            sleep_us(10)
            self.lineSensorPins[i].set_pull(self.lineSensorPins[i].NO_PULL)
            bPinState = self.lineSensorPins[i].read_digital()
            while bFlag == True and (ticks_us() - nStartTime) < nMaxTimer:
                bPinState = self.lineSensorPins[i].read_digital()
                if bPinState == 0:
                    nTimer = ticks_us() - nStartTime
                    nTimer = nTimer - 600  #Scaled
                    bFlag = False

            self.lineSensorValues[i] = max(0, min(nTimer, 1500))

    def LineSensorDetectsLine(self, sensor):
        return True if self.lineSensorValues[sensor] > self.lineSensorThreshold[sensor] else False

    def LineIrIntensity(self, sensor):
        return self.lineSensorValues[sensor]

    def LineAdjustThresholds(self, leftThreshold, centerThreshold, rightThreshold):
        self.lineSensorThreshold[0] = leftThreshold
        self.lineSensorThreshold[1] = centerThreshold
        self.lineSensorThreshold[2] = rightThreshold

    def Brake(self):
        pin12.write_digital(0)
        pin8.write_analog(512)
        pin16.write_analog(512)

    def RunMotor(self, nLeftSpeed, nRightSpeed):
        nLeftSpeed = (100 + nLeftSpeed) * 1024 / 200
        nLeftSpeed = max(0, min(nLeftSpeed, 1023))
        nRightSpeed = (100 + nRightSpeed) * 1024 / 200
        nRightSpeed = max(0, min(nRightSpeed, 1023))

        pin8.write_analog(nLeftSpeed)
        pin16.write_analog(nRightSpeed)
        pin12.write_digital(1)
