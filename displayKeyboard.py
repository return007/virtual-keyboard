import cv2
from constants import *

# loads and returns keyboard image of type number 
# Default keyboard is type 1
def loadKeyboard(type = 1) :
	image = cv2.imread("./images/keyboard"+str(type)+".png", cv2.IMREAD_COLOR)
	# resizedImage = cv2.resize(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
	return image

# display Keyboard
def displayKeyboard(type = 1) :
	image = loadKeyboard(type)
	cv2.imshow('virtual-keyboard',image)