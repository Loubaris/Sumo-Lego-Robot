#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.ev3devices import ColorSensor
import threading
from time import sleep
ev3 = EV3Brick()

# Initialisation des capteurs\moteurs
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
capteursonic = UltrasonicSensor(Port.S4)
couleur = ColorSensor(Port.S3)
color = couleur.color()
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)
# Initialisation des variables
direction = 1
chronotoupie = 0
chronotime = 0
chrono = 0
chronodistance = 0

# Fonction de la detection de couleur
# Lancé en thread indéfiniment afin de pouvoir detecter la bordure pendant que le robot avance
def color_detect():
    color = couleur.color()
    global direction
    if color == Color.WHITE:
        # Toucher la bordure induit un changement de direction, une marche arrière.
        if direction == 1:
            direction = 0
            chrono = 0
    
couleurthread=threading.Thread(target=color_detect)



while True:
    couleurthread.start() # Detection de la couleur

    while capteursonic.distance() > 630: # Le robot tourne sur lui même tant que aucun objet n'est détécté.
         robot.drive_time(0, 210, 100)
         chronodistance = 0

    if direction == 1: # Aller en avant
        robot.drive(500, 0)
    elif direction == 0: # Aller en arrière
        robot.drive(-500, 0)
        chrono+=1

    if capteursonic.distance() < 220: # Si un objet est détécté, le robot fonce dessus
        chronodistance+=1
        if chronodistance >= 800:
            robot.drive_time(-2000, 0, 1200)
            robot.drive_time(0, 180, 600)
            robot.drive_time(3000, 0, 1000)
        if direction == 1: # Aller en avant rapidement
            robot.drive(2000, 0)
        elif direction == 0: # Aller en arrière rapidement
            robot.drive(-2000, 0)

    # Si un objet est très proche du robot, et qu'il n'avance pas rapidement, activez le mode toupie.
    # Afin de faire tomber les robots ennemies
    if capteursonic.distance() < 100 and left_motor.speed() < 300: 
        chronotoupie = 1 
        chronotime = 0


    if chronotoupie == 1:
        robot.drive_time(0, 720, 3000)
        chronotoupie = 0

    # Durée du mode toupie.
    if chrono >= 50:
        direction = 1
        chrono = 0