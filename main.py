import cv2
import os
import sys
import struct
import imghdr
import colorsys
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
from PIL.ImageColor import getrgb
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
	rgbcolor = hex_to_rgb(color)

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
			border.putpixel((x,y), rgbcolor)

	# Paste the image on the border
	border.paste(img, (width, width))
	
	# Save copy of image without watermark
	borderpic = os.path.basename(os.path.normpath(p))
	borderpic = borderpic.split('.', 1)[0]
	picname = borderpic + "-border.png"
	print "Saving bordered picture as " + str(picname)
	border.save(picname)	

	wmark = Image.open(wm).convert('RGBA')
	wmarkpix = wmark.load()
	ww, wh = wmark.size
	wwmark = Image.new('RGBA', (ww, wh))
	# Make all non-transparent pixels white
	print str(wh) + " " + str(ww)
	for x in range(ww):
		for y in range(wh):
			print str(x) + " " + str(y)
			r, g, b, a = wmarkpix[x, y]
			if (a == 255):
				wwmark.putpixel((x,y), (255, 255, 255, 255))
			else:
				wwmark.putpixel((x,y), (255, 255, 255, 0))
	wwmark.show()
	wwmark.save('Hi.png')

	hexcolor = '#' + str(color).lower()
	r, g, b = getrgb(hexcolor)
	h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)	
	res = wmark.copy()
	wnew = res.load()
	for y in range(wmark.size[1]):
		for x in range(wmark.size[0]):
			r2, g2, b2, a = wnew[x,y]
			h2, l2, s2 = colorsys.rgb_to_hls(r2/255.0, g2/255.0, b2/255.0)
			r3, g3, b3 = colorsys.hls_to_rgb(h, l2, s)
			wnew[x, y] = (int(r3*255.99), int(g3*255.99), int(b3*255.99), a)	
	waterpic = os.path.basename(os.path.normpath(wm)) 
	waterpic = waterpic.split('.', 1)[0]
	wname = waterpic + "-recolor.png"
	print "Saving recolored watermark as " + str(wname)
	res.save(wname)

	# Alter watermark size, maintaining aspect ratio
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
