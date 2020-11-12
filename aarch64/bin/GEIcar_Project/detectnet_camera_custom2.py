#!/usr/bin/python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import jetson.inference
import jetson.utils

import sys

def Imageprocessing():
        #Variables
        network = "multiped"
        threshold = 0.5
        input_URI = ""
        output_URI = ""
        pic_name = "./images/currentPic.png"
        treated_pic_name = "./treatedCurrentPic.png"
        arguments =['detectnet_camera_custom.py', '--network=multiped', '--camera=csi://0', './images/currentPic.png', './treated_current_pic.png']
        pic_names = ["./images/currentPic.png", "treatedCurrentPic.png"]
        Overlay = "box,labels,conf"
        
        # load the object detection network
        net = jetson.inference.detectNet(network, arguments, threshold)

        # create video sources & outputs
        input = jetson.utils.videoSource(pic_name)
        output = jetson.utils.videoOutput(treated_pic_name)

        # process frames until the user exits
        while True:
                # capture the next image
                img = input.Capture()

                # detect objects in the image (with overlay)
                detections = net.Detect(img, overlay=Overlay)

                # print the detections
                print("detected {:d} objects in image".format(len(detections)))

                for detection in detections:
                        print(detection)

                # render the image
                output.Render(img)

                # update the title bar
                output.SetStatus("{:s} | Network {:.0f} FPS".format(network, net.GetNetworkFPS()))

                # print out performance info
                net.PrintProfilerTimes()

                # exit on input/output EOS
                if not input.IsStreaming() or not output.IsStreaming():
                        break


if __name__ == "__main__":
        Imageprocessing()
        

