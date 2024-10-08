#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
sys.path.append("sys")
sys.path.append("bac")
import infem
import infemGUI
from baseThreads import *

import time

#déclaration des sémaphores: valeur init, info pour le debug
sem1 = infem.Semaphore(4,"Attente du chargement de 4 voitures")
sem2 = infem.Semaphore(0, "Autorise la traversée")
sem3 = infem.Semaphore(0, "Autoriser le débarquement")
sem4 = infem.Semaphore(0, "Autoriser la traversée")

def ferryRun(self):
    """ fonction principale du bac. Les methodes principales sont:
        - self.traverser()
        - self.revenir()
    """
    while True :
        for i in range(4):
            sem2.P()
        self.traverser()
        for i in range(4):
            sem3.V()
        for i in range(4):
            sem4.P()
        self.revenir()
        for i in range(4):
            sem1.V()


    
    
def carRun(self):
    """ fonction principale de chaque voiture. Les méthodes principales sont:
        - self.avancer()
        - self.embarquer()
        - self.debarquer()
    """
    while True:
        self.avancer()
        self.log("devant l'eau!")
        sem1.P()
        self.embarquer()
        self.log("voiture embarquée!")
        sem2.V()
        sem3.P()
        self.debarquer()
        sem4.V()

def terminateCalled(self):
    """ fonction appelée lors d'un clic sur le bouton de terminaison """
    print("L'application doit se terminer correctement")

#associe les fonctions aux methodes de classes (ne pas modifier)
ferry.run = ferryRun
car.run = carRun

#main…
if __name__ == '__main__':
    from bacGUI import MainWindow
    MainWindow.terminateCalled = terminateCalled
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_() #event loop
