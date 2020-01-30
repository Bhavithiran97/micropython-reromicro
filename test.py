from reromicro import *
rero = reromicro()
while True:

  rero.ReadLineSensors()

  if rero.LineSensorDetectsLine(1) == True:
    rero.MoveForward(35)
  elif rero.LineSensorDetectsLine(0) == True:
    rero.TurnLeft(35)
  elif rero.LineSensorDetectsLine(2) == True:
    rero.TurnRight(35)
  else :
    rero.brake()
