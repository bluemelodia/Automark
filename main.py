import cv2
import os
import sys
import struct
import imghdr
import numpy as np
from PIL import Image
from PIL import ImageDraw
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

# Change hex to RGB
def hex_to_rgb(color):
	return tuple(ord(c) for c in color.decode('hex'))

def main():
	# Assumed that watermark has transparent background
	wm = raw_input("Provide Watermark: ")
	wm = validate(wm, 'watermark')

	p = raw_input("Provide Photo: ")		
	p = validate(p, 'photo')

	color = raw_input("Provide Hex Color Code: #")
	check_color(color)
	color = hex_to_rgb(color)

	img = Image.open(p)
	w, h = img.size
	print w 
	print h

	# Create border in desired color
	bh = w+10
	bw = h+10
	border = Image.new('RGB', (bh, bw))
	print bh 
	print bw
	for x in range(0, border.size[0]-1):
		for y in range(0, border.size[1]-1):
			print str(x) + " " + str(y)
			border.putpixel((x,y), color)
	border.show()	

if __name__ == "__main__": main()
