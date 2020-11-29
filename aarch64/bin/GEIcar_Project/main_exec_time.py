#Import threads classes
from Human_Detection_Thread_exec_time import Human_Detection
from Hurdles_Detection_Thread_exec_time import Hurdles_Detection
from ROS_publisher_Thread_execution_time import ROS_publisher

#Import execution time analysis library
import execution_time_analysis as execution

#Import global variables
import global_variables as glob
from std_msgs.msg import UInt8

#Import ROS library
import rospy

#Import Video init package
import detectnet_camera_custom_siec_noCV2 as detect

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
    glob.pub.value = rospy.Publisher('detection', UInt8, queue_size=10)
    #Specify the nodes name
    rospy.init_node('talker', anonymous=True)
    print("ROS Topic created\n")

    #Init video input
    glob.input.value = detect.Video_Source_init("csi://0")

    #Create threads
    human_detection_thread = Human_Detection()
    hurdles_detection_thread = Hurdles_Detection()

    ros_thread = ROS_publisher()

    #Run threads
    human_detection_thread.start()
    hurdles_detection_thread.start()
    ros_thread.start()

    while ( (glob.loop_counter_human <= glob.NUMBER_OF_LOOPS_FOR_TEST) or (glob.loop_counter_hurdles <= glob.NUMBER_OF_LOOPS_FOR_TEST) or (glob.loop_counter_ROS <= glob.NUMBER_OF_LOOPS_FOR_TEST) ):
        pass

    print("START EXECUTION TIME ANALYSIS\n")

    #Process execution time analysis
    xtab1 = glob.tab_delta_time_loop_human, 'Loop Human'
    xtab2 = glob.tab_delta_time_loop_hurdles, 'Loop Hurdles'
    xtab3 = glob.tab_delta_time_loop_ROS, 'Loop ROS'
    execution_time_test(xtab1, xtab2, xtab3)


