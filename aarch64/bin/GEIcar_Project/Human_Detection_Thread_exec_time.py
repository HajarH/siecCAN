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

#function that return the right number regarding what was detected for the human net
def human_detection_to_ROS_number(class_number):
    if class_number == 0: #Person
        return 1
    elif class_number == 2: #Baggage 
        return 2
    else:
        return 0
            

#Class for CNNs initializations and inferences
class Human_Detection(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        #We init human detection CNN
        #print("\nSTART HUMAN CNN INIT\n") #Debug
        net_human = detect.Multiped_Init()
        #print("\nMULTIPED INIT IS DONE\n") #Debug

        #Get detectable classes names
        """
        print("FOR HUMANS:\n")
        for i in range(0,net_human.GetNumClasses()):
            print("Number ", i, " :", net_human.GetClassDesc(i),"END")
            print("\n")
        """

        print("HUMAN INIT WENT WELL\n") #Debug
        time.sleep(2) #Just to get enough time to see that init went well

        while ( (glob.loop_counter_human <= glob.NUMBER_OF_LOOPS_FOR_TEST) or (glob.loop_counter_hurdles <= glob.NUMBER_OF_LOOPS_FOR_TEST) or (glob.loop_counter_ROS <= glob.NUMBER_OF_LOOPS_FOR_TEST) ):

            delta_time_loop_human = time.clock() #Measure execution time START

            #We process human detection
            #print("\nSTART HUMAN\n") #Debug
            detections_human = detect.Imageprocessing(net_human, "./treated_current_pic_human_detection.png")
            #print("Human detection done\n") #Debug
            #time.sleep(2) #Just to get enough time to see debug message

            #if we detect something set flag to block ROS periodic sending, ROS thread clears it
            if (len(detections_human) != 0):
                glob.detection_flag.MUT.acquire()
                glob.detection_flag.value = 1
                glob.detection_flag.MUT.release()

            #glob.detection_flag.MUT.acquire() #Debug
            #print("FLAG = ", glob.detection_flag.value) #Debug
            #glob.detection_flag.MUT.release() #Debug
            
            #Enumerate all the detections for human detection if there is one
            for detection in detections_human:
                    print("\nWe detected a " + net_human.GetClassDesc(detection.ClassID) + "\n")
                    glob.pub.MUT.acquire()
                    glob.pub.value.publish(human_detection_to_ROS_number(detection.ClassID))
                    glob.pub.MUT.release()

            delta_time_loop_human = time.clock() - delta_time_loop_human #Measure execution time END
            #Store the value for later analysis
            if (glob.loop_counter_human <= glob.NUMBER_OF_LOOPS_FOR_TEST):
                glob.tab_delta_time_loop_human = np.append(glob.tab_delta_time_loop_human, delta_time_loop_human)
            glob.loop_counter_human += 1 #Update loop counter

            #print("\nFINISH HUMAN DETECTION\n") #Debug
            #time.sleep(2) #Just to get enough time to see debug message 

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
    detection_thread = Human_Detection()

    # Lancement des threads
    detection_thread.start()

    # Attend que les threads se terminent
    detection_thread.join()

    

    

    
