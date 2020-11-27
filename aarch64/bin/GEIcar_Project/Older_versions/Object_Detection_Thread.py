# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import time
import detectnet_camera_custom_siec_noCV2 as detect
import numpy as np
import os
import sys

import random

#LIBRARY FOR MULTI-THREADING
import threading
from threading import Thread, Lock

#GLOBAL VARIABLES
import global_variables as glob

#function that return the right number regarding what was detected
#If net_number = 0 then it is human net
#If net_number = 1 then it is hurdles net
def detection_to_ROS_number(net_number, class_number):
    if net_number: #then it is hurdles net
        if class_number == 1: #Bus
            return 4
        elif class_number == 2: #Car
            return 5
        elif class_number == 3: #Bicycle
            return 6
        elif class_number == 4: #Cat
            return 7
        elif class_number == 5: #Dog
            return 8
        elif class_number == 6: #Motorcycle
            return 9
        else:
            return 0

    else: #then it is human net
        if class_number == 0: #Person
            return 1
        elif class_number == 2: #baggage 
            return 2
        else:
            return 0
            

#Class for CNNs initializations and inferences
class Detection(Thread):

    def __init__(self):
        Thread.__init__(self)

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
            
            #Get detectable classes names
            """
            print("FOR HUMANS:\n")
            for i in range(0,net_human.GetNumClasses()):
                print("Number ", i, " :", net_human.GetClassDesc(i),"END")
                print("\n")

            print("FOR HURDLES:\n")
            for i in range(0,net_hurdles.GetNumClasses()):
                print("Number ", i, " :", net_hurdles.GetClassDesc(i),"END")
                print("\n")
            """

            print("INITS WENT WELL\n")
            time.sleep(2)

            while True:
            
                #We process human detection
                #print("\nSTART HUMAN\n")
                detections_human = detect.Imageprocessing(net_human, input, "./treated_current_pic_human_detection.png")
                #print("Human detection done\n")
                #time.sleep(2)

                #Enumerate all the detections for human detection
                for detection in detections_human:
                        print("\nWe detected a " + net_human.GetClassDesc(detection.ClassID) + "\n")

                        #Acquire detection_number mutex to update it
                        glob.detection_number.MUT.acquire()
                        glob.detection_number.value = detection_to_ROS_number(0, detection.ClassID)
                        glob.detection_number.MUT.release()
                        #Send event that detection is done
                        glob.detection_done.set()
                        #Wait till event sending_done happens
                        #print("Wait sending_done human\n")
                        glob.sending_done.wait()
                        glob.sending_done.clear()
                        

                #print("\nFINISH HUMAN, START HURDLES \n")
                #time.sleep(3)

                #We process hurdles detection
                detections_hurdles = detect.Imageprocessing(net_hurdles, input, "./treated_current_pic_hurdles.png")

                #print("Hurdles detection done\n")

                #Enumerate all the detections for hurdles detection
                for detection in detections_hurdles:
                        print("\nWe detected a " + net_hurdles.GetClassDesc(detection.ClassID) + "\n")
                        #Acquire detection_number mutex to update it
                        glob.detection_number.MUT.acquire()
                        glob.detection_number.value = detection_to_ROS_number(1, detection.ClassID)
                        glob.detection_number.MUT.release()
                        #Send event that detection is done
                        glob.detection_done.set()
                        #Wait till event sending_done happens
                        #print("Wait sending_done hurdles\n")
                        glob.sending_done.wait()
                        glob.sending_done.clear() 
                        

                #print("\nFINISH HURDLES\n")

                #print("\nEND LOOP\n")
    
                #We wait one second between each loop
                #time.sleep(1)
        
#MAIN PROGRAM
if __name__ == "__main__":

    # Création des threads
    detection_thread = Detection()

    # Lancement des threads
    detection_thread.start()

    # Attend que les threads se terminent
    detection_thread.join()

    

    

    
