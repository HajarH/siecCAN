import time
import numpy as np
import os
import sys

#LIBRARY FOR MULTI-THREADING
import threading
from threading import Thread, Lock

#ROS library
import rospy
from std_msgs.msg import UInt8

#Import global variables
import global_variables as glob

#Class for publishing messages on ROS
class ROS_publisher(Thread):

    def __init__(self):
        Thread.__init__(self) 

    def run(self):
        """
        #Create the topic "detection"and the publisher 
        pub = rospy.Publisher('detection', UInt8, queue_size=10)
        #Specify the nodes name
        rospy.init_node('talker', anonymous=True)
        """

        #Specify the rate (we do note need it here)
        #rate = rospy.Rate(10) # 10hz

        while not rospy.is_shutdown():
            #Wait event detection_done
            glob.detection_done.wait()
            glob.detection_done.clear()

            #Acquire mutex for detection_number
            glob.detection_number.MUT.acquire()
            
            #Used for debug
            rospy.loginfo(glob.detection_number.value)
            
            #published the message
            glob.pub.publish(glob.detection_number.value)

            #Release mutex for detection_number
            glob.detection_number.MUT.release()

            #Send event sending_done
            glob.sending_done.set()

            #rate.sleep() #Only if we uses fixed rate

#MAIN PROGRAM
if __name__ == "__main__":

    #Create the topic "detection"and the publisher 
    glob.pub = rospy.Publisher('detection', UInt8, queue_size=10)
    #Specify the nodes name
    rospy.init_node('talker', anonymous=True)

    #Create thread
    ros_thread = ROS_publisher()

    #Start thread
    ros_thread.start()

    while True:
        pass
