# rero:micro Extension for MicroPython

This MicroPython package/extension/library provides driver for [**rero:micro** educational robot](https://my.cytron.io/p-rero-micro?currency=usd).<br />


* Use ``from reromicro import *`` at the top of your program
* Use ``rero = reromicro()`` to create instance object

## Let's make some noise!

* rero:micro's built-in piezo buzzer works with the default music module that comes with MicroPython on the BBC micro:bit.
* Use ``import music`` at the top of your program

```python
# Play melody "POWER_UP"
music.play(music.POWER_UP)
```

## Let's move it, move it~

* Use ``rero.RunMotor(leftMotorSpeed, rightMotorSpeed)`` to navigate rero:micro. Negative speed (-100 to -1) reverses the robot (eg: ``-50``), positive speed (1 to 100) moves it forward (eg: ``80``) and zero speed (``0``) brakes the motor. Note that the direction refers to rero:micro's movement, NOT motor's rotating direction.

* Use ``rero.Brake()`` to brake rero:micro.

```python
# rero:micro move forward at speed 50, for 1 second
rero.RunMotor(50, 50)
sleep_ms(1000)

# rero:micro turn left at speed 30, for 500 miliseconds
rero.RunMotor(-30, 30)
sleep_ms(500)

# rero:micro brakes
rero.Brake()
```

## Sensing obstacle

* ``rero.ReadUltrasonic()`` returns the distance in centimeter between ultrasonic sensor and any obstacle in front of it.

```python
# Forever loop
while True:

    # Brake rero:micro when obstacle is detected at 15cm away or nearer.
    # Otherwise, keep moving forward at speed 50.
    if (rero.ReadUltrasonic() < 15):
      rero.Brake()

    else:
      rero.RunMotor(50, 50)

```

## Line tracking

### ~ hint
``rero.ReadLineSensors()`` function must be called to read all three line sensors first before using ``rero.LineSensorDetectsLine(rero.(x))`` and/or ``rero.LineIrIntensity(rero.(x))`` to get the result.
### ~

* Use ``rero.LineSensorDetectsLine(rero.(x))`` to get the boolean value of line detection. Returns ``true`` when line is detected, otherwise ``false``.

* Use ``rero.LineIrIntensity(rero.(x))`` to get the reflected infrared (IR) intensity value, ranging from ``0`` to ``1500``.

```python
# Forever loop
while True:

    # read all three line sensors first
    rero.ReadLineSensors()

    # Move forward if only center sensor detects line.
    # Turn right if only right sensor detects line.
    # Turn left if only left sensor detects line.
    # Note: This simple program ignores all other possible conditions.
    if rero.LineSensorDetectsLine(rero.centerSensor):
      rero.RunMotor(50, 50)

    elif rero.LineSensorDetectsLine(rero.rightSensor):
       rero.RunMotor(-40, 40)

     elif rero.LineSensorDetectsLine(rero.leftSensor):
       rero.RunMotor(40, -40)

```

## Colour Splash!

* This robot also has 7x NeoPixels (WS2812B programmable RGB LEDs) built-in.

### ~ hint
See [bbcmicrobit/micropython-neopixel](https://microbit-micropython.readthedocs.io/en/latest/neopixel.html#module-neopixel) for NeoPixels support.
### ~

```python
# Create a NeoPixel strip at pin P1 with 7 LEDs
strip = neopixel.NeoPixel(pin1, 7)

# Show red colour for 1 sec.
for LED in range(7):
        strip[LED] = (255,0,0)
        strip.show()
sleep_ms(1000)

# Show blue colour for 1 sec.
for LED in range(7):
        strip[LED] = (0,0,255)
        strip.show()
sleep_ms(1000)

```
