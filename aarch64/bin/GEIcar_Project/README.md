author = benistant

# FILES LIST:

# CUSTOM PACKAGES

      - detectnet_camera_custom_original.py
      - detectnet_camera_custom_siec_noCV2.py
      - execution_time_analysis.py

# MAINS:
      - Object_Detection.py (no thread)
      - Object_Detection_Thread.py (with thread)

# HOW IT WORKS:

The main software is in "Object_Detection.py"

All the other functions are split in the packages

"detectnet_camera_custom_siec_noCV2.py" has all the function to initialize the CNN's and the video input

"execution_time_analysis.py" has all the function to process execution time arrays we create in the main software

"Object_Detection.py" uses the initializing functions, process a limited number of loops, store execution times for each detection in arrays, and call execution time analysis function


      
