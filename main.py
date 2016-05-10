import cv2
import os
import sys
import imghdr
import numpy as np
from imutils import paths

images = ['jpeg', 'png']
chars = set('GHIJKLMNOPQRSTUVWXYZ')

# Validate images provided by user
def validate(str, name):
	path = os.path.abspath(str.strip())
	try:
		assert os.path.exists(path)
	except: 
		sys.exit("Invalid path to " + name + ".")
	try: 
		assert imghdr.what(path) in images 
	except: 
		sys.exit("Supported formats: jpeg, png.")	
	return path

# Screen for valid hex color codes
def check_color(color):
	try:
		assert color.isalnum()
		assert len(color) == 6
		assert not any((c in chars) for c in color)
	except:
		sys.exit("Invalid hex color code.")

def main():
	# Assumed that watermark has transparent background
	wm = raw_input("Provide Watermark: ")
	wm = validate(wm, 'watermark')

	p = raw_input("Provide Photo: ")		
	p = validate(p, 'photo')

	color = raw_input("Provide Hex Color Code: #")
	color = check_color(color)

if __name__ == "__main__": main()
