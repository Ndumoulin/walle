import serial, time
import os
import pygame
from pygame.constants import JOYBUTTONDOWN, JOYBUTTONUP, JOYAXISMOTION, JOYHATMOTION

t = time.localtime()

"""Classe représentant la manette d'XBOX"""
class XBOXController(object):

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    """
    Tableau des commandes avec les valeurs possibles entre parenthèses :
    [0] = moteur dc gauche (100,0,-100)
    [1] = moteur dc droite (100,0,-100)
    [2] = servomoteur taille (1,0,-1)
    [3] = servomoteur épaule (1,0,-1)
    [4] = servomoteur coude (1,0,-1)
    [5] = électro-aimant (1,0)
    [6] = Mode (conduite : 1, Contrôle du bras : 0)
    """
    commands = [0,0,0,0,0,0,1]
    drivingMode = True

    def init(self):
        """Initialiser les composants de la manette"""
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    """Génération d'une commande en String qui sera envoyé au Arduino"""
    def generate_command(self):
        line = ";".join(str(x) for x in self.commands)
        return line

    """Écoutez constamment pour détecter chaques boutons appuyés ou joystick bougé"""
    def listen(self):
        """Connexion à l'arduino"""
        with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as arduino:
            time.sleep(0.1)

            if arduino.isOpen():
                print("{} connecté!". format(arduino.port))

            """Ici, nous vérifions quel type d'évenement il s'agit (axis, button ou hat)"""

            if not self.axis_data:
                self.axis_data = {}

            if not self.button_data:
                self.button_data = {}
                for i in range(self.controller.get_numbuttons()):
                    self.button_data[i] = False

            if not self.hat_data:
                self.hat_data = {}
                for i in range(self.controller.get_numhats()):
                    self.hat_data[i] = (0, 0)

            while True:
                """Copie de la commande précédente qui nous permettra de vérifier si la commande change"""
                previous_commands = self.commands.copy()

                """Écoute chaque évenements venant de la manette en lien avec un axis (RB, LB, Joystick de droite et de gauche)"""
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        self.axis_data[event.axis] = round(event.value,2)
                        
                        if self.drivingMode == True:
                            """
                            Contrôle du moteur DC gauche :
                            La vitesse est fixé à 100, il est possible de la modifier, mais 100 est largement suffisant.
                            Une zone morte de 0.5, sur chaque joystick permet d'éviter plusieurs problèmes si la manette n'est pas bien calibré
                            """
                            if event.axis == 1 and self.axis_data[event.axis] == 0 and self.commands[0] != 0:
                                self.commands[0] = 0
                            if event.axis == 1 and self.axis_data[event.axis] >= 0.5 and self.commands[0] != -100:
                                self.commands[0] = -100
                            if event.axis == 1 and self.axis_data[event.axis] <= -0.5 and self.commands[0] != 100:
                                self.commands[0] = 100
                                
                            """Contrôle du moteur DC droite"""
                            if event.axis == 3 and self.axis_data[event.axis] == 0 and self.commands[1] != 0:
                                self.commands[1] = 0
                            if event.axis == 3 and self.axis_data[event.axis] >= 0.5 and self.commands[1] != -100:
                                self.commands[1] = -100
                            if event.axis == 3 and self.axis_data[event.axis] <= -0.5 and self.commands[1] != 100:
                                self.commands[1] = 100
                            
                        if self.drivingMode == False:
                            """Contrôle du servomoteur épaule"""
                            if event.axis == 3 and self.axis_data[event.axis] == 0 and self.commands[3] != 0:
                                self.commands[3] = 0
                            if event.axis == 3 and self.axis_data[event.axis] >= 0.3 and self.commands[3] != -1:
                                self.commands[3] = -1
                            if event.axis == 3 and self.axis_data[event.axis] <= -0.3 and self.commands[3] != 1:
                                self.commands[3] = 1
                                
                            """Contrôle du servomoteur coude"""
                            if event.axis == 1 and self.axis_data[event.axis] == 0 and self.commands[4] != 0:
                                self.commands[4] = 0
                            if event.axis == 1 and self.axis_data[event.axis] >= 0.3 and self.commands[4] != -1:
                                self.commands[4] = 1
                            if event.axis == 1 and self.axis_data[event.axis] <= -0.3 and self.commands[4] != 1:
                                self.commands[4] = -1
                        
                    elif event.type == pygame.JOYBUTTONDOWN:
                        self.button_data[event.button] = True
                        
                        """Changement de mode"""
                        if event.button == 4 and self.commands[6] == 0:
                            self.commands[6] = 1
                            self.drivingMode = True
                        elif event.button == 4 and self.commands[6] == 1:
                            self.commands[6] = 0
                            self.drivingMode = False

                        """Contrôle du servomoteur taille"""
                        if self.drivingMode == False:
                            if event.button == 7:
                                self.commands[2] = -1
                            if event.button == 6:
                                self.commands[2] = 1
                                
                        """Contrôle de l'électro-aimant"""
                        if event.button == 3:
                            if self.commands[5] == 0:
                                self.commands[5] = 1
                            elif self.commands[5] == 1:
                                self.commands[5] = 0

                    """Si nous relachons RB ou LB, le servomoteur de la taille arrête de tourner"""
                    elif event.type == pygame.JOYBUTTONUP:
                        self.button_data[event.button] = False
                        if event.button == 7:
                            self.commands[2] = 0
                        if event.button == 6:
                            self.commands[2] = 0
                            
                    elif event.type == pygame.JOYHATMOTION:
                        self.hat_data[event.hat] = event.value

                    """Envoie de la commande à l'arduino via le port série"""
                    if previous_commands != self.commands:
                        arduino.write(str.encode(self.generate_command()))
                        print(str.encode(self.generate_command()))
                        
      
def convert_data(x):
    return int(x * 255)
    

def controller_main():
    xbox = XBOXController()
    xbox.init()
    xbox.listen()


controller_main()
