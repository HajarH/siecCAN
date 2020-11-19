# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import time
import detectnet_camera_custom_siec as detect
import execution_time_analysis as execution
import numpy as np
import os

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

#GLOBAL VARIABLES
NUMBER_OF_ITERATION = 10 #Sets the number of picture analysis, set to -1 if you want infinite loop

im_counter = 0

def execution_time_test(*tabs):
    for current_tab in tabs:
        execution.execution_time_analysis(current_tab[0], current_tab[1])

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def Camera_Init():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    return cap

def Camera_Test(cap):
    if cap.isOpened():
        
        #print('Start get picture\n')
        ret_val, img = cap.read()
        global im_counter
        im_counter += 1
        #print('Picture taken\n')
        cv2.imwrite('./images/currentPic.png', img)
        #print('Picture Saved\n')
        # This also acts as

"""
        keyCode = cv2.waitKey(30) & 0xFF
        # Stop the program on the ESC key
        if keyCode == 27:
            break
        cur_time = time.clock() - cur_time
        print('Time to take a pic: ' + str(cur_time) + 's\n')
"""

def Camera_Close(cap):
    cap.release()
    cv2.destroyAllWindows()
    


def main():
    #We init neural networks
    print("\nSTART CNN INIT\n")
    #net_human = detect.Multiped_Init()
    print("\nMULTIPED INIT IS DONE\n")
    #net_hurdles = detect.Hurdles_Init()
    print("\nHURDLES INIT IS DONE, CNNs OK\n")
    time.sleep(2)

    print("\nSTART CAMERA INIT\n")
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    cap = Camera_Init()
    if cap.isOpened():
        print("\nCAMERA START IS DONE\n")
        
        loop_counter = 0
        first_time = 1

        tab_delta_time_snap_take_n_write = []
        tab_delta_time_human = []
        tab_delta_time_hurdles = []

        while (loop_counter < NUMBER_OF_ITERATION or NUMBER_OF_ITERATION == -1):

            #Get Picture
            delta_time_snap_take_n_write = time.clock() #Measure execution time START
            ret_val, img = cap.read()
            print("PIC TAKEN\n")
            time.sleep(2)
            
            #Store image taken
            cv2.imwrite('./images/currentPic{}.png'.format(loop_counter), img)

            # This also acts as
            keyCode = cv2.waitKey(30) & 0xFF 

            print("PIC STORED\n")
            time.sleep(2)

            delta_time_snap_take_n_write = time.clock() - delta_time_snap_take_n_write #Measure execution time END
            #Store the value for later analysis
            tab_delta_time_snap_take_n_write = np.append(tab_delta_time_snap_take_n_write, delta_time_snap_take_n_write)
            
            #Process Image Detection
            print("\nSTART HUMAN DETECTION\n")
            time.sleep(2)

            delta_time_human = time.clock() #Measure execution time START
            #detect.Imageprocessing(net_human, "./treated_current_pic_human_detection.png")
            delta_time_human = time.clock() - delta_time_human #Measure execution time END
            #Store the value for later analysis
            tab_delta_time_human = np.append(tab_delta_time_human, delta_time_human)
  
            print("\nHUMAN DETECTION DONE, START HURDLES DETECTION\n")
            time.sleep(2)
            
            delta_time_hurdles = time.clock() #Measure execution time START
            #detect.Imageprocessing(net_hurdles, "./treated_current_pic_hurdles.png")
            delta_time_hurdles = time.clock() - delta_time_hurdles #Measure execution time END
            #Store the value for later analysis
            tab_delta_time_hurdles = np.append(tab_delta_time_hurdles, delta_time_hurdles)
            
            print("\nHURDLES DETECTION DONE, DETECTION OK\n")
            loop_counter +=1 #Update loop counter

            if os.path.exists("./images/currentPic.png"):
                os.remove("./images/currentPic.png")
                print("Old picture was deleted")
                time.sleep(2)

            # Stop the program on the ESC key
            if keyCode == 27:
                break
 
        cap.release()
        cv2.destroyAllWindows()

        return tab_delta_time_snap_take_n_write, tab_delta_time_human, tab_delta_time_hurdles

    else:
        print("Unable to open camera")

if __name__ == "__main__":

    cap = Camera_Init()

    while True:
        Camera_Test(cap)
        time.sleep()

    
    #tab1, tab2, tab3 = main()

    #Execution Time test
    #xtab1 = tab1, 'Snaps'
    #xtab2 = tab2, 'Human'
    #xtab3 = tab3, 'Hurdles'
    #execution_time_test(xtab1, xtab2, xtab3)
    

    
