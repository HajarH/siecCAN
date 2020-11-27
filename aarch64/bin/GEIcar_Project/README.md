author = benistant

# FILES LIST:

# CUSTOM PACKAGES

      - detectnet_camera_custom_siec_noCV2.py
      - execution_time_analysis.py
      - Human_Detection_Thread.py
      - Hurdles_Detection_Thread.py
      - ROS_publisher_Thread.py
      - global_variables.py 
 

# MAINS:
      - main.py

# HOW IT WORKS:

The main software is in "main.py".

All the other functions are split in the packages.

"global_variables.py" contains all the variables to be used simultaneaously in different python files.

"detectnet_camera_custom_siec_noCV2.py" has all the function to initialize CNNs and the video input.

"execution_time_analysis.py" has all the function to analyze execution time arrays we create in the main software.

"Human_Detection_Thread.py" contains everything related to the real implementation of the human CNN. It detects continuously and when it detects something it sets a detection flag and send a ROS message on "detection" topic.

"Hurdles_Detection_Thread.py" contains everything related to the real implementation of the hurdles CNN. It detects continuously and when it detects something it sets a detection flag and send a ROS message on "detection" topic.

"ROS_publisher_Thread.py" sends continuously a ROS message at 100Hz to say nothing was detected. When detection_flag is set, it clears the flag and stops sending the no_detection ROS message for 5s.

In the main "main.py" the three previous thread classes are imported. First the ROS Topic is created, then threads objects are declared and run.

# Corresponding classes and their corresponding class numbers for nets and ROS are in:
      - classes_training.txt

      
