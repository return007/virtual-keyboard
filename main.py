import cv2
import numpy as np 

from constants import *
from displayKeyboard import *

def nothing(x) :
	pass

# file = open('keys_coordinate.vkb', 'w')

# def writeToFile(x, y) :
# 	global file
# 	file.write(str(x) + "," + str(y) + "\n")

# def checkEvent(event, x, y, flags, param) :
# 	if event == cv2.EVENT_LBUTTONDOWN :
# 		# return (x,y)
# 		writeToFile(x,y)

cap = cv2.VideoCapture(0)

keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', '\n']
keys_location = []

file = open('keys_coordinate.vkb', 'r')
for line in file :
	keys_location.append(line.split(','))

file.close()

for i in range(len(keys_location)) :
	keys_location[i][0] = int(keys_location[i][0])
	keys_location[i][1] = int(keys_location[i][1])

print(len(keys), len(keys_location))

CAPSLOCK = False

# cv2.namedWindow('color-chooser')
# cv2.createTrackbar('lowerH','color-chooser',0,179,nothing)
# cv2.createTrackbar('upperH','color-chooser',0,179,nothing)
# cv2.createTrackbar('lowerS','color-chooser',0,255,nothing)
# cv2.createTrackbar('upperS','color-chooser',0,255,nothing)
# cv2.createTrackbar('lowerV','color-chooser',0,255,nothing)
# cv2.createTrackbar('upperV','color-chooser',0,255,nothing)

keyboard_image = loadKeyboard()
# cv2.namedWindow('keyboard_image')
# cv2.setMouseCallback('keyboard_image', checkEvent)

iters = 0
prevKey = -1

output_file = open('output.txt', 'w')

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
	
	kernel = np.ones((7,7), np.uint8)
	erosion_pointer = cv2.erode(mask_green, kernel, iterations = 1)
	erosion_button = cv2.erode(mask_orange, kernel, iterations = 1)

	dilation_pointer = cv2.dilate(erosion_pointer, kernel, iterations = 1)
	dilation_button = cv2.dilate(erosion_button, kernel, iterations = 1)

	# cv2.imshow('frame', frame)
	# cv2.imshow('mask_orange', mask_orange)
	# cv2.imshow('mask_green', mask_green)
	# cv2.imshow('erosion_pointer', erosion_pointer)
	# cv2.imshow('erosion_button', erosion_button)

	# cv2.imshow('dilation_pointer', dilation_pointer)
	# cv2.imshow('dilation_button', dilation_button)

	_, thresh_pointer = cv2.threshold(dilation_pointer, 127, 255, 0)
	_, thresh_button = cv2.threshold(dilation_button, 1, 255, 0)

	# cv2.imshow('thresh_button', thresh_button)


	contours_pointer, heirarchy = cv2.findContours(thresh_pointer, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	x = y = w = h = 0

	for contour in contours_pointer :
		x,y,w,h = cv2.boundingRect(contour)

		if w*h <= 300 :
			continue

		break

	keyboard_image = loadKeyboard()
	cv2.circle(keyboard_image, (x,y), 5, (0,0,255), -1)
	cv2.imshow('keyboard_image', keyboard_image)

	button_press = False

	contours_button, heirarchy = cv2.findContours(thresh_button, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if len(contours_button) > 0 :
		button_press = True

	# print(button_press)
	matched = False
	if button_press :
		for i in range(len(keys)) :
			if keys_location[2*i][0] <= x <= keys_location[2*i+1][0] and keys_location[2*i][1] <= y <= keys_location[2*i+1][1] :
				matched = True
				break

		if matched == True and iters == 0 and prevKey == keys[i] :
			print(keys[i])
			output_file.write(keys[i])
			iters = (iters + 1) % 5
		elif prevKey != keys[i] :
			iters = 0
		else :
			iters = (iters + 1) % 5			

		prevKey = keys[i]
 
	key_press = cv2.waitKey(1)
	if key_press & 0xFF == ord('q') :
		break

cap.release()
cv2.destroyAllWindows()
file.close()