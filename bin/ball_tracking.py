#!/usr/bin/env python3
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

color_dict_HSV = {
    'black': [(180, 255, 30), (0, 0, 0)],
    'white': [(180, 18, 255), (0, 0, 231)],
    'red1': [(180, 255, 255), (159, 50, 70)],
    'red2': [(9, 255, 255), (0, 50, 70)],
    'green1': [(89, 255, 255), (36, 50, 70)],
    'green2': [(64, 255, 255), (29, 86, 6)],
    'blue': [(128, 255, 255), (90, 50, 70)],
    'yellow': [(35, 255, 255), (25, 50, 70)],
    'purple': [(158, 255, 255), (129, 50, 70)],
    'orange': [(24, 255, 255), (10, 50, 70)],
    'gray': [(180, 18, 230), (0, 0, 40)]
}

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--color", type=str, default="red", help="Color to track")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the
# ball in the HSV color space, then initialize the
# list of tracked points
color = args['color']
greenLower = color_dict_HSV[color][1]
greenUpper = color_dict_HSV[color][0]

bufferLength = 64
pts = deque(maxlen=bufferLength)
vs = VideoStream(src=0).start()
# allow the camera to warm up
time.sleep(2.0)
# keep looping
while True:
	# grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (21, 21), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask1 = cv2.inRange(hsv, greenLower, greenUpper)
	mask2 = cv2.erode(mask1, None, iterations=2)
	mask3 = cv2.dilate(mask2, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			# update the points queue
			pts.appendleft(center)
			# loop over the set of tracked points
			for i in range(1, len(pts)):
				# if either of the tracked points are None, ignore
				# them
				if pts[i - 1] is None or pts[i] is None:
					continue
				# otherwise, compute the thickness of the line and
				# draw the connecting lines
				thickness = int(np.sqrt(bufferLength / float(i + 1)) * 2.5)
				cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

vs.stop()
# close all windows
cv2.destroyAllWindows()
