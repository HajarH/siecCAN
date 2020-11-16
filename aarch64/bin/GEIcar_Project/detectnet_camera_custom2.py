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
import time

def Multiped_Init():
        #Variables
        network = "multiped"
        threshold = 0.5
        arguments = ['./images/currentPic.png', './treated_current_pic_human_detection.png']
        Overlay = "box,labels,conf"

         # load the object detection network
        net = jetson.inference.detectNet(network, arguments, threshold)

        return net

def Hurdles_Init():
        #Variables
        network = "ssd-mobilenet-v2"
        threshold = 0.5
        arguments = ['--model=networks/hurdles/ssd-mobilenet.onnx', '--labels=networks/hurdles/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', './images/currentPic.png', './treated_current_pic_hurdles.png']
        Overlay = "box,labels,conf"

         # load the object detection network
        net = jetson.inference.detectNet(network, arguments, threshold)

        return net

def Imageprocessing(net, output_pic_name):
        #Variables
        input_URI = ""
        output_URI = ""
        pic_name = "./images/currentPic.png"
        argments = ['']
        Overlay = "box,labels,conf"

        # create video sources & outputs
        input = jetson.utils.videoSource(pic_name)
        #output = jetson.utils.videoOutput(treated_pic_name) #We do not need it anymore

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
                #output.Render(img)
                jetson.utils.saveImage(output_pic_name, img) #only save the image

                # update the title bar
                #output.SetStatus("{:s} | Network {:.0f} FPS".format(network, net.GetNetworkFPS()))

                # print out performance info
                net.PrintProfilerTimes()

                # exit on input/output EOS
                if not input.IsStreaming() or not output.IsStreaming():
                        break


if __name__ == "__main__":
        net_human = Multiped_Init()
        print("\nMULTIPED INIT IS DONE \n")
        time.sleep(3)

        
        net_hurdles = Hurdles_Init()
        print("\nHurdles INIT IS DONE \n")
        time.sleep(3)

        print("\nSTART HUMAN DETECTION \n")
        time.sleep(3)
        Imageprocessing(net_human, "./treated_current_pic_human_detection.png")

        print("\nFINISH HUMAN, START HURDLES \n")
        time.sleep(3)
        Imageprocessing(net_hurdles, "./treated_current_pic_hurdles.png")

