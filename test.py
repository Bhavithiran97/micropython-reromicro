from reromicro import *
import music

rero = reromicro()
distance = 0
Mode = 0
strip = neopixel.NeoPixel(pin1, 7)
music.play(music.POWER_UP)
sleep_ms(1000)

def ultrasonicPushPull():
    distance = rero.ReadUltrasonic()
    if distance > 35:
        rero.Brake()
    elif distance > 15:
        speed = ((distance - 15) * 5)
        rero.RunMotor(speed, speed)
    else :
        speed = ((15 - distance) * 5)
        rero.RunMotor(-(speed), -(speed))

def lineFollow():
    if rero.ReadUltrasonic() < 10:
        rero.Brake()
    else:
        rero.ReadLineSensors()
        if rero.LineSensorDetectsLine(rero.leftSensor) and rero.LineSensorDetectsLine(rero.centerSensor):
            rero.RunMotor(25, 40)
        elif rero.LineSensorDetectsLine(rero.rightSensor) and rero.LineSensorDetectsLine(rero.centerSensor):
            rero.RunMotor(40, 25)
        elif rero.LineSensorDetectsLine(rero.centerSensor):
            rero.RunMotor(40, 40)
        elif rero.LineSensorDetectsLine(rero.leftSensor):
            rero.RunMotor(10, 30)
        elif rero.LineSensorDetectsLine(rero.rightSensor):
            rero.RunMotor(30, 10)
        else:
            rero.Brake()

while True:
    if button_a.was_pressed():
        Mode = 1
        rero.Brake()

    elif button_b.was_pressed():
        Mode = 2
        rero.Brake()

    elif  button_a.is_pressed() and button_b.is_pressed():
        Mode = 3
        rero.Brake()

    if Mode == 1:
        ultrasonicPushPull()
    elif Mode == 2:
        lineFollow()
    elif Mode == 3:
        music.play(music.BIRTHDAY)
        sleep_ms(13000)
        Mode = 0
    else:
        for index in range(7):
            strip[index] = (255,0,0)
            strip.show()
        sleep_ms(500)
        for index in range(7):
            strip[index] = (0,255,0)
            strip.show()
        sleep_ms(500)
        for index in range(7):
            strip[index] = (0,0,255)
            strip.show()
        sleep_ms(500)
