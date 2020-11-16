# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import time
import detectnet_camera_custom2 as detect

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

TIME_TO_WAIT_IN_S = 1
PIC_FOLDER = './images/currentPic.png'

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


def show_camera():
    #We init neural networks
    print("\nSTART CNN INIT\n")
    net_human = detect.Multiped_Init()
    print("\nMULTIPED INIT IS DONE\n")
    net_hurdles = detect.Hurdles_Init()
    print("\nHURDLES INIT IS DONE, CNNs OK\n")
    time.sleep(2)

    print("\nSTART CAMERA INIT\n")
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        print("\nCAMERA START IS DONE\n")

        #im_counter=0 #If we store images 
        cur_time = 0
        hello = 1 #To do the loop once

        while hello:
            hello = 0 #To do the loop once
            cur_time = time.clock() - cur_time #Measure loop execution time
            #Get Picture
            ret_val, img = cap.read()
            #im_counter += 1 #I we store images
            
            #Store image taken
            cv2.imwrite('./images/currentPic.png', img)

            #Process Image Detection
            print("\nSTART HUMAN DETECTION\n")
            time.sleep(2)
            detect.Imageprocessing(net_human, "./treated_current_pic_human_detection.png")
            print("\nHUMAN DETECTION DONE, START HURDLES DETECTION\n")
            time.sleep(2)
            detect.Imageprocessing(net_hurdles, "./treated_current_pic_hurdles.png")
            print("\nHURDLES DETECTION DONE, DETECTION OK\n")

            # This also acts as
            keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                break
            print('Time to take and Process a pic: ' + str(cur_time) + 's\n')
 
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
