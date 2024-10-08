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
sem1 = infem.Semaphore(4,"Embarquement voiture")
sem2 = infem.Semaphore(0,"Débarquement voiture")
sem3 = infem.Semaphore(0,"Aller")
sem4 = infem.Semaphore(0,"Retour")
sem5 = infem.Semaphore(0,"Terminaison propre")
sem6 = infem.Semaphore(1,"Thread Bateau")
sem7 = infem.Semaphore(10,"Threads voiture")


def ferryRun(self):
    """ fonction principale du bac. Les methodes principales sont:
        - self.traverser()
        - self.revenir()
    """
    timeout = 100.
    cond = infem.ou2Semaphore(sem5,sem6,timeout)
    while cond == 2:
        self.log("En attente des voitures")
        for i in range(4):
            if infem.ou2Semaphore(sem5,sem3,timeout)==1:
                return 0
        self.log("Eh ze bardi !")
        self.traverser()
        for i in range(4):
            sem2.release()
        for i in range(4):
            if infem.ou2Semaphore(sem5,sem4,timeout)==1:
                return 0
        self.log("Eh za revient !")
        self.revenir()
        for i in range(4):
            sem1.release()
        sem6.release()
        cond = infem.ou2Semaphore(sem5,sem6,timeout)

    self.log("Fin de tâche")

def carRun(self):
    """ fonction principale de chaque voiture. Les méthodes principales sont:
        - self.avancer()
        - self.embarquer()
        - self.debarquer()
    """
    timeout = 100.
    cond = infem.ou2Semaphore(sem5,sem7,timeout)
    while cond == 2:
        self.avancer()
        self.log("Devant l'eau!")
        if infem.ou2Semaphore(sem5,sem1,timeout)==1:
            return 0
        else:
            self.embarquer()
            sem3.release()
        if infem.ou2Semaphore(sem5,sem2,timeout)==1:
            return 0
        else:
            self.debarquer()
            sem4.release()
            sem7.release()
        cond = infem.ou2Semaphore(sem5,sem7,timeout)
    
    self.log("Fin de tâche")

def terminateCalled(self):
    """ fonction appelée lors d'un clic sur le bouton de terminaison """
    print("L'application doit se terminer correctement")
    for i in range(11):
        sem5.release()

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
