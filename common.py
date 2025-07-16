from dataclasses import dataclass

SENSOR_BUF_SIZE = 1024 
COMMAND_BUF_SIZE = 1024


# aici sunt date placeholder
@dataclass
class SensorData:
    x: float #placeholder, poți băga aici vectori din numpy
    y: float
    z: float


# datele de comandă trimise efectiv la motor
# placeholder, dar cam așa ar veni comanda la motoare folosind modulul ăla de comandă
@dataclass
class CommandData:
    rightMotorTuration: float # aici ar fi probabil cv valoare de la 0 la 1 pt pwn
    rightMotorOrientation: int # pt direcție (1 în față, -1 în spate)
    leftMotorTuration: float # aici ar fi probabil cv valoare de la 0 la 1 pt pwn
    leftMotorOrientation: int # pt direcție (1 în față, -1 în spate)
    