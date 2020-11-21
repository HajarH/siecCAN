# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import time
import detectnet_camera_custom_siec_noCV2 as detect
import execution_time_analysis as execution
import numpy as np
import os
import sys

import random

#LIBRARY FOR MULTI-THREADING
import threading
from threading import Thread, Lock

#GLOBAL VARIABLES

"""
def detection_inference(self):
    #We initialize neural networks
    #print("\nSTART CNN INIT\n")

    #We init human detection CNN
    net_human = detect.Multiped_Init()
    #print("\nMULTIPED INIT IS DONE\n")

    #We init hurdles detection CNN
    net_hurdles = detect.Hurdles_Init()
    #print("\nHURDLES INIT IS DONE, CNNs OK\n")
    #time.sleep(2)

    #We init the Camera as an input
    input = detect.Video_Source_init("csi://0")

    while True:

        #We acquire the mutex
        self.mot_sens.MUT.acquire()
        
        #We process human detection
        #print("\nSTART HUMAN\n")
        self.detections_human = detect.Imageprocessing(net_human, input, "./treated_current_pic_human_detection.png")
        
        #print("\nFINISH HUMAN, START HURDLES \n")
        #time.sleep(3)

        #We process hurdles detection
        self.detections_hurdles = detect.Imageprocessing(net_hurdles, input, "./treated_current_pic_hurdles.png")

        #print("\nFINISH HURDLES\n")

        #print("\nEND LOOP\n")
        #time.sleep(10)

        #Enumerate all the detections for human detection
        for detection in self.detections_human:
                print("\nWe detected a " + net_human.GetClassDesc(detection.ClassID) + "\n")

        #Enumerate all the detections for hurdles detection
        for detection in detections_hurdles:
                print("\nWe detected a " + net_hurdles.GetClassDesc(detection.ClassID) + "\n")

        #We release the mutex
        self.mot_sens.MUT.release()
        time.sleep(1)
"""
                

#Class for CNNs initializations and inferences
class Detection(Thread):

    def __init__(self,lettre):
        Thread.__init__(self)
        self.lettre = lettre
        
        #ADD ATTRIBUTES HERE
        self.detections_human = []
        self.detections_hurdles = []
        self.MUT = Lock()

        def run(self):

            i=0
            while i < 20:
                sys.stdout.write(self.lettre)
                sys.stdout.flush()
                attente = 0.2
                attente += random.randint(1, 60) / 100
                time.sleep(attente)
                i += 1

            
"""
            #We initialize neural networks
            #print("\nSTART CNN INIT\n")

            #We init human detection CNN
            net_human = detect.Multiped_Init()
            #print("\nMULTIPED INIT IS DONE\n")

            #We init hurdles detection CNN
            net_hurdles = detect.Hurdles_Init()
            #print("\nHURDLES INIT IS DONE, CNNs OK\n")
            #time.sleep(2)

            #We init the Camera as an input
            input = detect.Video_Source_init("csi://0")

            while True:
                
                #We acquire the mutex
                self.mot_sens.MUT.acquire()
        
                #We process human detection
                #print("\nSTART HUMAN\n")
                self.detections_human = detect.Imageprocessing(net_human, input, "./treated_current_pic_human_detection.png")

                #print("\nFINISH HUMAN, START HURDLES \n")
                #time.sleep(3)

                #We process hurdles detection
                self.detections_hurdles = detect.Imageprocessing(net_hurdles, input, "./treated_current_pic_hurdles.png")

                #print("\nFINISH HURDLES\n")

                #print("\nEND LOOP\n")
                #time.sleep(10)

                #Enumerate all the detections for human detection
                for detection in self.detections_human:
                        print("\nWe detected a " + net_human.GetClassDesc(detection.ClassID) + "\n")

                #Enumerate all the detections for hurdles detection
                for detection in detections_hurdles:
                        print("\nWe detected a " + net_hurdles.GetClassDesc(detection.ClassID) + "\n")

                #We release the mutex
                self.mot_sens.MUT.release()
                time.sleep(1)
"""

class Detection(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self):
        Thread.__init__(self)
        self.detections_human = []
        self.detections_hurdles = []
        self.MUT = Lock() 

    def run(self):
            #We initialize neural networks
            #print("\nSTART CNN INIT\n")

            #We init human detection CNN
            net_human = detect.Multiped_Init()
            #print("\nMULTIPED INIT IS DONE\n")

            #We init hurdles detection CNN
            net_hurdles = detect.Hurdles_Init()
            #print("\nHURDLES INIT IS DONE, CNNs OK\n")
            #time.sleep(2)

            #We init the Camera as an input
            input = detect.Video_Source_init("csi://0")

            while True:
                
                #We acquire the mutex
                self.MUT.acquire()
        
                #We process human detection
                #print("\nSTART HUMAN\n")
                self.detections_human = detect.Imageprocessing(net_human, input, "./treated_current_pic_human_detection.png")

                #print("\nFINISH HUMAN, START HURDLES \n")
                #time.sleep(3)

                #We process hurdles detection
                self.detections_hurdles = detect.Imageprocessing(net_hurdles, input, "./treated_current_pic_hurdles.png")

                #print("\nFINISH HURDLES\n")

                #print("\nEND LOOP\n")
                #time.sleep(10)

                #Enumerate all the detections for human detection
                for detection in self.detections_human:
                        print("\nWe detected a " + net_human.GetClassDesc(detection.ClassID) + "\n")

                #Enumerate all the detections for hurdles detection
                for detection in self.detections_hurdles:
                        print("\nWe detected a " + net_hurdles.GetClassDesc(detection.ClassID) + "\n")

                #We release the mutex
                self.MUT.release()
                time.sleep(1)

        
#MAIN PROGRAM
if __name__ == "__main__":

    # Création des threads
    detection_thread = Detection()

    # Lancement des threads
    detection_thread.start()

    # Attend que les threads se terminent
    detection_thread.join()

    

    

    
