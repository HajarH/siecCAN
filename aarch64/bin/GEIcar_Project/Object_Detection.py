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

#GLOBAL VARIABLES
NUMBER_OF_ITERATION = 2 #Sets the number of picture analysis, set to -1 if you want infinite loop

"""
This function will use the arrays created while running the software was running
in order to estimate mean execution time for all the parts of the detections
"""
def execution_time_test(*tabs):
    for current_tab in tabs:
        execution.execution_time_analysis(current_tab[0], current_tab[1])

def main():
    #We init neural networks
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

    #We declare arrays to store execution time
    tab_delta_time_human = []
    tab_delta_time_hurdles = []

    #Loop counter variable
    loop_counter = 0

    while (loop_counter < NUMBER_OF_ITERATION or NUMBER_OF_ITERATION == -1):

        #We process human detection
        #print("\nSTART HUMAN\n")

        delta_time_human = time.clock() #Measure execution time START
        detect.Imageprocessing(net_human, input, "./treated_current_pic_human_detection.png")
        delta_time_human = time.clock() - delta_time_human #Measure execution time END
        #Store the value for later analysis
        tab_delta_time_human = np.append(tab_delta_time_human, delta_time_human)

        #print("\nFINISH HUMAN, START HURDLES \n")
        #time.sleep(3)

        #We process hurdles detection
        delta_time_hurdles = time.clock() #Measure execution time START
        detect.Imageprocessing(net_hurdles, input, "./treated_current_pic_hurdles.png")
        delta_time_hurdles = time.clock() - delta_time_hurdles #Measure execution time EN
        #Store the value for later analysis
        tab_delta_time_hurdles = np.append(tab_delta_time_hurdles, delta_time_hurdles)

        #print("\nFINISH HURDLES\n")

        #print("\nEND LOOP\n")
        #time.sleep(10)

        loop_counter +=1 #Update loop counter


    return tab_delta_time_human, tab_delta_time_hurdles

        
#MAIN PROGRAMM
if __name__ == "__main__":
     tab1, tab2 = main()

     #Execution Time test
     xtab1 = tab1, 'Human'
     xtab2 = tab2, 'Hurdles'
     #execution_time_test(xtab1, xtab2)
         

    

    

    
