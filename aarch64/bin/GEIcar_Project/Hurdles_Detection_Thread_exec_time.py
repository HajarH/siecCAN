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

#ROS Library
import rospy
from std_msgs.msg import UInt8

#GLOBAL VARIABLES
import global_variables as glob

#function that return the right number regarding what was detected for Hurdles CNN
def hurdles_detection_to_ROS_number(class_number):
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
            

#Class for CNNs initializations and inferences
class Hurdles_Detection(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        #We init hurdles detection CNN
        #print("\nHURDLES INIT START\n") #Debug
        net_hurdles = detect.Hurdles_Init()
        #print("\nHURDLES INIT IS DONE\n") #Debug
        #time.sleep(2) #Debug

        #Get detectable classes names
        """
        print("FOR HURDLES:\n")
        for i in range(0,net_hurdles.GetNumClasses()):
            print("Number ", i, " :", net_hurdles.GetClassDesc(i),"END")
            print("\n")
        """

        print("HURDLES INIT WENT WELL\n")
        time.sleep(2) #Just to have time to see the debug message

        while ( (glob.loop_counter_human <= glob.NUMBER_OF_LOOPS_FOR_TEST) or (glob.loop_counter_hurdles <= glob.NUMBER_OF_LOOPS_FOR_TEST) or (glob.loop_counter_ROS <= glob.NUMBER_OF_LOOPS_FOR_TEST) ):

            delta_time_loop_hurdles = time.clock() #Measure execution time START
            
            #print("\nSTART HURDLES DETECTION\n") #Debug
            #time.sleep(2) #Just to have time to see the debug message

            #We process hurdles detection
            detections_hurdles = detect.Imageprocessing(net_hurdles, "./treated_current_pic_hurdles.png")

            #print("Hurdles detection done\n") #Debug
            #time.sleep(2) #Just to have time to see the debug message
            #if we detect something set flag to block ROS periodic sending, ROS thread clears it
            if (len(detections_hurdles) != 0):
                glob.detection_flag.MUT.acquire()
                glob.detection_flag.value = 1
                glob.detection_flag.MUT.release()

            #glob.detection_flag.MUT.acquire() #Debug
            #print("FLAG = ", glob.detection_flag.value) #Debug
            #glob.detection_flag.MUT.release() #Debug

            #Enumerate all the detections for hurdles detection
            for detection in detections_hurdles:
                    print("\nWe detected a " + net_hurdles.GetClassDesc(detection.ClassID) + "\n")
                    glob.pub.MUT.acquire()
                    glob.pub.value.publish(hurdles_detection_to_ROS_number(detection.ClassID))
                    glob.pub.MUT.release()

            delta_time_loop_hurdles = time.clock() - delta_time_loop_hurdles #Measure execution time END
            #Store the value for later analysis
            if(glob.loop_counter_hurdles <= glob.NUMBER_OF_LOOPS_FOR_TEST):
                glob.tab_delta_time_loop_hurdles = np.append(glob.tab_delta_time_loop_hurdles, delta_time_loop_hurdles)

            glob.loop_counter_hurdles += 1
 
            #print("\nFINISH HURDLES\n") #Debug

            #print("\nEND LOOP\n") #Debug

            #We wait one second between each loop
            #time.sleep(1)
        
#MAIN PROGRAM
if __name__ == "__main__":

    #Create the topic "detection" and the publisher 
    glob.pub.value = rospy.Publisher('detection', UInt8, queue_size=10)
    #Specify the nodes name
    rospy.init_node('talker', anonymous=True)
    print("ROS Topic created\n")
    
    # Création des threads
    detection_thread = Detection()

    # Lancement des threads
    detection_thread.start()

    # Attend que les threads se terminent
    detection_thread.join()

    

    

    
