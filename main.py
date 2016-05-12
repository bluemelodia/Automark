import cv2
import os
import sys
import struct
import imghdr
import numpy as np
from PIL import Image
from PIL import ImageDraw
from imutils import paths

width = 5
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
	
	wm_size = raw_input("Width of Watermark: ")
	try:
		assert float(wm_size) >= 0.0 and float(wm_size) <= 100.0
	except:
		sys.exit("Invalid watermark percentage.")

	color = raw_input("Provide Hex Color Code: #")
	check_color(color)
	color = hex_to_rgb(color)

	uw = raw_input("Provide Border Width (max 100px): ") 
	try:
		assert uw.strip().isdigit() 
		assert int(uw) > 0 and int(uw) <= 100
	except:
		sys.exit("Invalid border value.")
	width = int(uw)

	img = Image.open(p)
	w, h = img.size

	# Create border in desired color
	bh = w+width*2
	bw = h+width*2
	border = Image.new('RGB', (bh, bw))
	for x in range(0, border.size[0]):
		for y in range(0, border.size[1]):
			border.putpixel((x,y), color)

	# Paste the image on the border
	border.paste(img, (width, width))
	
	# Save copy of image without watermark
	borderpic = os.path.basename(os.path.normpath(p))
	borderpic = borderpic.split('.', 1)[0]
	picname = borderpic + "-border.png"
	print "Saving bordered picture as " + str(borderpic) + "-border.png."
	border.save(picname)	

	# Alter watermark size, maintaining aspect ratio
	wmark = Image.open(wm).convert('RGBA')
	size = int(w*(float(wm_size)/100)), int(h*(float(wm_size)/100))
	wmark.thumbnail(size, Image.ANTIALIAS)	
	wmark.show()

	wmarkpic = Image.open(os.path.abspath(picname))
	ww, wh = wmarkpic.size

	wdraw = ImageDraw.Draw(wmark)

	# Place the watermark in the right corner
	wmarkpic.paste(wmark, (width, width))
	print "Saving watermarked picture as " + str(borderpic) + "-wm.png."
	wmarkpic.save(borderpic + "-wm.png")

if __name__ == "__main__": main()
