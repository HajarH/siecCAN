author = benistant

# FILES LIST:

# CUSTOM PACKAGES

      - detectnet_camera_custom_original.py
      - detectnet_camera_custom_siec_noCV2.py
      - execution_time_analysis.py
      - Object_Detection_Thread.py
      - ROS_publisher_Thread.py
      - global_variables.py 
 

# MAIN:
      - main.py

# HOW IT WORKS:

The main software is in "main.py"

All the other functions are split in the packages

"global_variables.py" contains all the variables to be used simultaneaously in different python files.

"detectnet_camera_custom_siec_noCV2.py" has all the function to initialize the CNN's and the video input

"execution_time_analysis.py" has all the function to process execution time arrays we create in the main software

"Object_Detection_Thread.py" contains everything related to the detection thread. It declares the detection thread class and a bunch of function we use to exploit the detection results.

"ROS_publisher_Thread.py" contains everything relates to the ROS publisher thread; it declares the ROS publisher threads.

In the main "main.py" both previous thread classes are imported. First the ROS Topic is created, then threads objects are declared and run. Synchronization is ensured using "threading.Event" objects. Detection are made and for all objects detected, detection waits till each single detected human or hurdles piece of information is sent. ROS_publisher thread wait until there is something to send, then send it, and finally give the hand back to detection thread.

# Corresponding classes and their corresponding class numbers for nets and ROS are in:
      - classes_training.txt

      
