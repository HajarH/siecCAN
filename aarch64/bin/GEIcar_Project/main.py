#CLEAR EVENTS AT THE BEGINNING

#Import threads classes
from Human_Detection_Thread import Human_Detection
from Hurdles_Detection_Thread import Hurdles_Detection
from ROS_publisher_Thread import ROS_publisher


#Import global variables
import global_variables as glob

#Import ROS library
import rospy
from std_msgs.msg import UInt8

#MAIN PROGRAM
if __name__ == "__main__":
    
    #Create the topic "detection"and the publisher 
    glob.pub.value = rospy.Publisher('detection', UInt8, queue_size=10)
    #Specify the nodes name
    rospy.init_node('talker', anonymous=True)
    print("ROS Topic created\n")

    #Create threads
    human_detection_thread = Human_Detection()
    hurdles_detection_thread = Hurdles_Detection()
    ros_thread = ROS_publisher()

    #Run threads
    human_detection_thread.start()
    #hurdles_detection_thread.start()
    ros_thread.start()

    #Infinite loop because detection_thread has a while true
    human_detection_thread.join()
