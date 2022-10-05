from PIL import Image
from pytesseract import image_to_string
import pytesseract
import settings
#from w_bot import asci_char, send_rq

tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" tessedit_char_whitelist=0123456789'
pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' 



class Mover(object):
	from settings import logger
	import random

	"""docstring for Mover"""
	def __init__(self, arg):
		super(Mover, self).__init__()
		self.arg = arg



	def get_coordinates ():
		from settings import coordinates_color_low, coordinates_color_high

		from settings import logger
		import cv2 as cv
		import numpy as np
		import time

		x=0
		y=0
		logger.info("trying to get coordinates")


		hsv = cv.imread ('var/2/coordinates.png')
		hsv = cv.cvtColor(hsv, cv.COLOR_BGR2HSV)
		lower = np.array(coordinates_color_low, dtype = "uint8")
		upper = np.array(coordinates_color_high, dtype = "uint8")
 
		mask = cv.inRange(hsv, lower, upper)
		cv.imwrite('var/2/coordinates.png', mask)
		t=str(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
		cv.imwrite(f"var/2/coordinates/coordinates_low{coordinates_color_low}_high{coordinates_color_high}_{t}.png", mask)
		#cv.imshow("coords", mask)
		#cv.waitKey(0)




		c=image_to_string(Image.open('var/2/coordinates.png'), lang='eng', config=tessdata_dir_config+ "")
		logger.info ("OCR = " + c)
		if len(c)>10:
			try:
				x = float(c[0:5])
				y = float(c[7:12])
			except ValueError:
				return (x, y)
			finally:
				return (int(x*100), int(y*100))
		else:
			return (0, 0)

	def find_degree (start, end, target):
		from math import acos, degrees
		from math import sqrt
		from settings import logger
 		
		logger.info (f"find_degree ==== start position: {start}, end position: {end}, target: {target}")
		ax = end[0] - start[0]
		ay = end[1] - start[1]
		bx = target[0] - start[0] 
		by = target[1] - start[1]

		logger.info (f"find_degree ==== ax ={ax}, ay={ay}, bx={bx}, by={by}")
		ma = sqrt(ax * ax + ay * ay)
		mb = sqrt(bx * bx + by * by)
		sc = ax * bx + ay * by
		res = acos(sc / ma / mb)
		#return (degrees(res))
		return (res) 

	@classmethod
	def find_quater(self, start, end, target):
		from settings import logger
		from math import cos, sin, pi
		ax = end[0] - start[0]
		ay = end[1] - start[1]
		bx =target[0] - start[0]
		by = target [1] - start[1]
		logger.info (f"find_quater ==== ax ={ax}, ay={ay}, bx={bx}, by={by}")

		degree = self.find_degree ((0, 0), (7, 0), (bx, by))
		#degree = degree*pi/180
		x1 = ax*cos(degree) - ay*sin(degree)
		y1 = ax*sin(degree) + ay*cos(degree)

		return (round(x1), round(y1))		

	@classmethod
	def move_forward(self):
		from settings import logger
		import random

		r = 'w'
		p = random.randint(40,220)
		m = "on"
		print(self.send_request(ord(r), p, m))
		logger.info("move_forward --- after send_rq")

	@classmethod
	def stop_move(self):
		import random
		r='w'
		p=random.randint(40,220)
		m="off"
		print(self.send_request(ord(r), p, m))

	@classmethod
	def make_turn (self, start, stop, target):

		from settings import logger
		from math import degrees
		degree = self.find_degree (start, stop, target)
		logger.info (f"make_turn degree= {degree} rad")
		logger.info (f"make_turn degree= {degrees(degree)} degrees")
		qtr = self.find_quater (start, stop, target)[1]
		logger.info (f"make_turn quater= {qtr}")
		time_for_turn = 1100 # время для разворота на 180гр.
		p = str(round(time_for_turn *degrees(degree) / 180))
		logger.info (f"make_turn delay= {p}")
		m = "on_dl"
		if qtr < 0:
			r='d'
		elif qtr > 0:
			r = 'a'
		elif qtr == 0:
			r='d' 
		logger.info("make_turn  --- sending request")

		#print(self.send_request (ord(r), p, m))
		print(self.send_request( (ord(r)), 9, "on_dl"))


	@classmethod
	def send_request(self, r, p, m, retries=0):
		global time_keyboard_last_on_dl

		from settings import logger
		from settings import time_keyboard_last_on_dl
		import requests
		import time

		#if win.send_arduino_requests.get() == False:
		#	return "send_arduino_requests = False"
		#	logger.info("send_arduino_requests = False")
		logger.debug("send_rq triyng "+str(retries))
		x=''
		if retries > 10: return
		try:
			data = {"r": r, "p" :p, "m": m, "e": ""}
			if m == "on_dl":
				logger.keylog(f"Pause before: {str(round((time.time()-time_keyboard_last_on_dl)*100))}ms, Key: {chr(r)}, Delay: {p}, Mod: {m}")
				logger.info(f"EMU === Key: {chr(r)}, Delay: {p}, Mod: {m}")
				time_keyboard_last_on_dl = time.time()
			if m == "on":
				logger.info(f"EMU === Key: {chr(r)}, Delay: {p}, Mod: {m}")
			x = requests.get("http://"+settings.arduino_ip, params={"r": r, "p" :p, "m": m, "e": ""})#, timeout=1)
		except requests.exceptions.ConnectTimeout as e:
			retries+=1
			logger.info("triyng "+retries)
			self.send_request(r, p, m, retries)
		except requests.exceptions.RequestException as e:
			logger.info ("OOps: Something Else",e)
		else:
			True
			logger.info("send_rq else")
		finally:
			return x

#print (Mover.find_quater((5,8),(9,9),(-8, 13)))

#print (Mover.find_quater((50,50),(70,50),(50, 70)))
#print (Mover.find_quater((6,4),(9,9),(-8, 13)))
#print (Mover.find_quater((7,1),(5,1),(8, 3)))

