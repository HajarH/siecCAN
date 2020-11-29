#CLEAR EVENTS AT THE BEGINNING

#Import threads classes
from Object_Detection_Thread_exec_time import Detection
from ROS_publisher_Thread import ROS_publisher

#Import execution time analysis library
import execution_time_analysis as execution

#Import global variables
import global_variables as glob
from std_msgs.msg import UInt8

#Import ROS library
import rospy

"""
This function will use the arrays created while running the software was running
in order to estimate mean execution time for all the parts of the detections
"""
def execution_time_test(*tabs):
    for current_tab in tabs:
        execution.execution_time_analysis(current_tab[0], current_tab[1])

#MAIN PROGRAM
if __name__ == "__main__":
    
    #Create the topic "detection"and the publisher 
    glob.pub = rospy.Publisher('detection', UInt8, queue_size=10)
    #Specify the nodes name
    rospy.init_node('talker', anonymous=True)
    print("ROS Topic created\n")
    

    #Set events to false
    glob.detection_done.clear()
    glob.sending_done.clear()

    #Create threads
    detection_thread = Detection()

    ros_thread = ROS_publisher()

    #Run threads
    detection_thread.start()
    ros_thread.start()

    #Infinite loop because detection_thread has a while true
    detection_thread.join()
    print("START EXECUTION TIME ANALYSIS\n")

    #Process execution time analysis
    xtab = glob.tab_delta_time_loop, 'Loop'
    execution_time_test(xtab)


