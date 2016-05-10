import cv2
import os
import sys
import imghdr
import numpy as np
from imutils import paths
from Tkinter import *

images = ['jpeg', 'png']

def main():
	# Assumed that watermark has transparent background
	wm = raw_input("Provide Watermark: ")
	try: 
		wm_a = os.path.abspath(wm.strip())
		assert os.path.exists(wm_a)
	except:
		sys.exit("Invalid path to watermark.")
	try:
		assert imghdr.what(wm_a) in images	
	except:
		sys.exit("Supported formats: jpeg, png.")

	p = raw_input("Provide Photo: ")		
	try:
		p_a = os.path.abspath(p.strip())
		assert os.path.exists(p_a)
	except:
		sys.exit("Invalid path to photo.")
	try: 
		assert imghdr.what(p_a) in images
	except:
		sys.exit("Supported formats: jpeg, png.")

	color = askcolor() 	
	

if __name__ == "__main__": main()
