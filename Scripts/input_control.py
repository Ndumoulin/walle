import pygame
from pygame.constants import JOYBUTTONDOWN, JOYBUTTONUP, JOYAXISMOTION, JOYHATMOTION

pygame.init()

joysticks = []

for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()

print(joysticks)

while True or KeyboardInterrupt:

    #check for joystick events

    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            if event.button == 0:
                print("Button A down")
            if event.button == 1:
                print("Button B down")
            if event.button == 4:
                print("Button Y down")
            if event.button == 3:
                print("Button X down")
            if event.button == 14:
                print("Button RSB down")
            if event.button == 13:
                print("Button LSB down")
            if event.button == 7:
                print("Button RB down")
            if event.button == 6:
                print("Button LB down")
            if event.button == 11:
                print("Button MENU down")
                