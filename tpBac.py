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
sem5 = infem.Semaphore(0, "Terminaison")
sem6 = infem.Semaphore(1, "Thread Bateau")
sem7 = infem.Semaphore(10, "Thread Voiture")


def ferryRun(self):
    """ fonction principale du bac. Les methodes principales sont:
        - self.traverser()
        - self.revenir()
    """
    cond=infem.ou2Semaphore(sem5, sem6)
    while cond == 2 :
        i = 0
        j = 0
        while i < 4 and cond == 2:
            cond = infem.ou2Semaphore(sem5, sem2)
            i+=1
        if cond == 2:
            self.traverser()
            self.log("Traversée effectuée")
            for i in range(4):
                sem3.V()
        while j < 4 and cond == 2:
            infem.ou2Semaphore(sem5, sem4)
            j+=1
        if cond == 2:
            self.revenir()
            self.log("Retour effectué")
            for i in range(4):
                sem1.V()
            sem6.V()
        cond=infem.ou2Semaphore(sem5, sem6)


    
    
def carRun(self):
    """ fonction principale de chaque voiture. Les méthodes principales sont:
        - self.avancer()
        - self.embarquer()
        - self.debarquer()
    """
    cond=infem.ou2Semaphore(sem5, sem7)
    while cond == 2:
        self.avancer()
        self.log("devant l'eau!")
        if infem.ou2Semaphore(sem5, sem1) == 2:
            self.embarquer()
            self.log("voiture embarquée!")
            sem2.V()
        if infem.ou2Semaphore(sem5, sem3) == 2:
            self.debarquer()
            sem4.V()
            sem7.V()
        cond=infem.ou2Semaphore(sem5, sem7)

def terminateCalled(self):
    """ fonction appelée lors d'un clic sur le bouton de terminaison """
    print("L'application doit se terminer correctement")
    for i in range (32):
     sem5.V()

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
