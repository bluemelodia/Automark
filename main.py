import cv2
import os
import sys
import numpy as np
from imutils import paths
from Tkinter import *

def main():
	wm = raw_input("Provide Watermark: ")
	try: 
		assert os.path.isfile(wm)
		wm = os.path.abspath(wm)
	except:
		sys.exit("Invalid path to watermark.")
	p = raw_input("Provide Photo: ")		
	try:
		assert os.path.isfile(p)
		p = os.path.abspath(p)
	except:
		sys.exit("Invalid path to photo.")
	
	

if __name__ == "__main__": main()
