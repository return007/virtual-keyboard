import cv2
import numpy as np 

from constants import *
from displayKeyboard import *

def nothing(x) :
	pass

cap = cv2.VideoCapture(0)

# cv2.namedWindow('color-chooser')
# cv2.createTrackbar('lowerH','color-chooser',0,179,nothing)
# cv2.createTrackbar('upperH','color-chooser',0,179,nothing)
# cv2.createTrackbar('lowerS','color-chooser',0,255,nothing)
# cv2.createTrackbar('upperS','color-chooser',0,255,nothing)
# cv2.createTrackbar('lowerV','color-chooser',0,255,nothing)
# cv2.createTrackbar('upperV','color-chooser',0,255,nothing)

while True :
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)

	# lower_h = cv2.getTrackbarPos('lowerH','color-chooser')
	# upper_h = cv2.getTrackbarPos('upperH','color-chooser')
	# lower_s = cv2.getTrackbarPos('lowerS','color-chooser')
	# upper_s = cv2.getTrackbarPos('upperS','color-chooser')
	# lower_v = cv2.getTrackbarPos('lowerV','color-chooser')
	# upper_v = cv2.getTrackbarPos('upperV','color-chooser')

	# lower_red = np.array([lower_h,lower_s,lower_v])
	# upper_red = np.array([upper_h,upper_s,upper_v])

	############################ ORANGE CAP ###########################################################
	# lower_orange = np.array([0,88,174])
	# upper_orange = np.array([19,255,255])

	########################### GREEN CAP ##########################
	# lower_green = np.array([58,78,0])
	# upper_green = np.array([90,213,255])

	lower_orange = np.array([0,88,174])
	upper_orange = np.array([19,255,255])

	lower_green = np.array([58,78,0])
	upper_green = np.array([90,213,255])

	frame = cv2.blur(frame, (5,5))
	frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	mask_orange = cv2.inRange(frame_hsv, lower_orange, upper_orange)
	mask_green = cv2.inRange(frame_hsv, lower_green, upper_green)

	# cv2.imshow('frame', frame)
	cv2.imshow('mask_orange', mask_orange)
	cv2.imshow('mask_green', mask_green)

	key_press = cv2.waitKey(1)
	if key_press & 0xFF == ord('q') :
		break

cap.release()
cv2.destroyAllWindows()