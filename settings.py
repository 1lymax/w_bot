from PIL import ImageTk, Image
import time
import cv2 as cv
import numpy as np
import random
import requests
import threading
import tkinter as tk
import imutils
import logging

from matplotlib import pyplot as plt
from datetime import datetime
from pynput import keyboard
from pynput import mouse
from pynput.keyboard import Key
from http.server import BaseHTTPRequestHandler,HTTPServer



global hero_last_turn
global send_keys 
global webcam
global mouse_start_x
global mouse_start_y
global t_start, localtime
global last_pressed_key
global target_needs_try
global window, window_image, window_copy_of_image, window_label, window_frm_image
global update_window_image
global color1, color2, color3

global arduino_ip
global send_arduino_requests
global webcam_processing
global webcam_extra_screenshots
global find_button_coordinates
global show_cv_windows
global key1_name, key2_name
global Saved_coords_processing, screenshot
global stateOn
global send_keys_mouse_events, mover
global show_color_lines_info

global bg, btn, pbar, pbar_width, pbar_enemy_type
global time_keyboard_last_on_dl
global Mover1

#logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)


logging.KEYBOARD = 60 
logging.addLevelName(logging.KEYBOARD, "KEYBOARD")
def keylog(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    self._log(logging.KEYBOARD, message, args, **kws) 
logging.Logger.keylog = keylog

logger = logging.getLogger(__name__)
# Create handlers
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('logs/app.log')
d_handler = logging.FileHandler('logs/debug.log')
k_handler = logging.FileHandler('logs/keys.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)
d_handler.setLevel(logging.DEBUG)
k_handler.setLevel(logging.KEYBOARD)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
d_format = logging.Formatter('%(asctime)s - %(message)s')
k_format = logging.Formatter('%(asctime)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
d_handler.setFormatter(d_format)
k_handler.setFormatter(k_format)
# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.addHandler(d_handler)
logger.addHandler(k_handler)



webcam_window_show = False

hero_name = "Grenato"
key1_name = "F1"
key2_name = "F2"
key3_name = "F3"
pbar_full = 162 # индикация полного бара. вычислчется из логов, по сканированию изображений. моменты opencv
pbar_window_width = 200 # фактическая длина баров в окне
hero_low_health_respawn_value =110
loot_time = 8


color_gray = "gray"
color_lt_gray = "lavender"
color_green = "medium sea green"
color_red = "indian red"
color_blue = "dodger blue"
color_yellow = "gold"
WINDOW_IMAGE_SCALE_PERCENT = 70
window_stop_updates = False

webcam = cv.VideoCapture(1)#, cv.CAP_DSHOW)
#if webcam_processing:
webcam.set(3, 1920)
webcam.set(4, 1080)


screen_size =(1920, 1080)
resolution =2  # 1- 1920x1080, 2 - 1280x1024
Listener = None
last_pressed_key =''
target_needs_to_be_in_front_of_you= False
target_needs_try =0
time_keyboard_last_on_dl = 0 # служит для вычисления паузы между нажатыми клавишами
padx=9
pady=2

exit = False
act_spells = []
arduino_ip = "192.168.2.177"
server_ip = "192.168.2.100"

if resolution == 1:
	
	coords = [
	["status_of_hero", 82, 22, 201, 24],
	["health_box",92,48,204,54],
	["astral", 92, 57, 204, 65],
	["button1_1", 569, 980, 601, 1012],
	["button1_2",609,980,642,1012],
	["button1_3",652,980,685,1012],
	["button1_4",693,980,726,1012],
	["button1_5",736,980,770,1012],
	["button1_6",780,980,810,1012],
	["button2_1",567,1028,599,1062],
	["button2_2",609,1028,642,1062],
	["button2_3",652,1028,682,1062],
	["button2_4",693,1028,723,1062],
	["button2_5",736,1028,766,1062],
	["button2_6",780,1028,810,1062],
	#["button_area"565,976,],
	]
else:

	btn_width=93  # ширина кнопки на экране
	btn_diff_x=101   # растояние между крайними левыми/правыми точками кнопки. шаг
	btn_posx=632      # координата левого верхнего угла кнопки
	btn_posy=246 #+ 16 # 16 -уровень героя 60 
	btn_diff_y=109  # разница между первым и вторым рядом кнопок
	in_button_difference_1 = 2 # требует настройки. Настройка включается переменной find_button_coordinates
	in_button_difference_2 = 109 # должны быть помещены в папку src заготовки активных спелов на кнопках. Заготавливается переменной Saved_coords_processing
	coords = [
	["sys_msg_area", 1132, 242, 1500, 355,"", 0, 0, ""],
	["hero_status_area", 1289, 9, 1412, 60,"", 0, 0, ""],
	["button_area",btn_posx,btn_posy,btn_posx+btn_diff_x*6, btn_posy+btn_diff_y*2,"",0,0, ""],
	["enemy_type_area", 727, 142, 837, 195,"", 0, 0, ""],
	#["coordinates", 1260, 281, 1663, 357,"", 0, 0, ""]
	["coordinates", 1281, 281, 1642, 357,"", 0, 0, ""] # AR Zhonkai #3
	]
	saved_coords = [
	#["enemy_yellow", 0, 200, 1270, 790, "enemy", 0, 0],
	["q", (btn_posx+btn_width/2)+btn_diff_x*0, btn_posy, btn_posx+btn_diff_x*1, btn_posy+btn_width,"button_area",btn_width/2+btn_diff_x*0,in_button_difference_1, ""],
	["t", (btn_posx+btn_width/2)+btn_diff_x*1, btn_posy, btn_posx+btn_diff_x*2, btn_posy+btn_width,"button_area",btn_width/2+btn_diff_x*1,in_button_difference_1, ""], #
	["f", (btn_posx+btn_width/2)+btn_diff_x*2, btn_posy, btn_posx+btn_diff_x*3, btn_posy+btn_width,"button_area",btn_width/2+btn_diff_x*2,in_button_difference_1, ""],
	["g", (btn_posx+btn_width*0)+btn_diff_x*3, btn_posy, btn_posx+btn_diff_x*4, btn_posy+btn_width,"button_area",btn_width*0+btn_diff_x*3,in_button_difference_1, ""],
	["h", (btn_posx+btn_width*0)+btn_diff_x*4, btn_posy, btn_posx+btn_diff_x*5, btn_posy+btn_width,"button_area",btn_width*0+btn_diff_x*4,in_button_difference_1, ""], # width*0 - полная кнопка
	["v", (btn_posx+btn_width*0)+btn_diff_x*5, btn_posy, btn_posx+btn_diff_x*6, btn_posy+btn_width,"button_area",btn_width*0+btn_diff_x*5,in_button_difference_1, ""],
	#["v", (btn_posx+btn_width*0)+btn_diff_x*6, btn_posy, btn_posx+btn_diff_x*7, btn_posy+btn_width,"button_area",btn_width*0+btn_diff_x*6,2, ""],
	["1", (btn_posx+btn_width/2)+btn_diff_x*0, btn_posy+btn_diff_y, btn_posx+btn_diff_x*1, btn_posy+btn_diff_y+btn_width,"button_area",btn_width/2+btn_diff_x*0,in_button_difference_2, ""],
	["2", (btn_posx+btn_width/2)+btn_diff_x*1, btn_posy+btn_diff_y, btn_posx+btn_diff_x*2, btn_posy+btn_diff_y+btn_width,"button_area",btn_width/2+btn_diff_x*1,in_button_difference_2, ""],
	["3", (btn_posx+btn_width/2)+btn_diff_x*2, btn_posy+btn_diff_y, btn_posx+btn_diff_x*3, btn_posy+btn_diff_y+btn_width,"button_area",btn_width/2+btn_diff_x*2,in_button_difference_2, ""],
	["4",	(btn_posx+btn_width/2)+btn_diff_x*3, btn_posy+btn_diff_y, btn_posx+btn_diff_x*4, btn_posy+btn_diff_y+btn_width,"button_area",btn_width/2+btn_diff_x*3,in_button_difference_2, ""],
	["5", (btn_posx+btn_width/2)+btn_diff_x*4, btn_posy+btn_diff_y, btn_posx+btn_diff_x*5, btn_posy+btn_diff_y+btn_width,"button_area",btn_width/2+btn_diff_x*4,in_button_difference_2, ""],
	["6", (btn_posx+btn_width/2)+btn_diff_x*5, btn_posy+btn_diff_y, btn_posx+btn_diff_x*6, btn_posy+btn_diff_y+btn_width,"button_area",btn_width/2+btn_diff_x*5,in_button_difference_2, ""],
	["attack",1340, 15 , 1402, 52, "hero_status_area", 51, 5, ""],
	["enemy_beast",729, 148 , 828, 181, "enemy_type_area", 2, 6, ""]
	
	#["target_in_front", 1135, 248, 1249, 283, "sys_msg_area", 1, 6, ""]

	]

	status_lines = [
		#["attack", 				523, 39, 880, 66, " ", 0, 0, color_red],
		#["attack", 1, 1, 350, 350, " ", 4, 11],
		["health", 				991, 76, 1317, 108, " ", 0, 0, color_green],
		["astral", 				987, 125, 1274, 145, " ", 0, 0, color_blue],
		["target_in_front", 1135, 248, 1249, 283, "", 1, 6, color_red],
		#["enemy", 				0, 200, 1270, 790, " ", 0, 0],
		#["enemy_attack", 	910, 35, 1280, 52, " ", 0, 0, color_red],
		["enemy_health", 	346, 87, 588, 112, " ", 0, 0, color_green],
		["enemy_type", 		358, 33, 627, 43, " ", 0, 0, color_lt_gray]
		#["is_dead", 	910, 113, 1266, 135, " ", 0, 0, color_gray],
		]

	# очередность соответствует предыдущему массиву
	spells_time = [
		[2, 0],
		[2, 0],
		[0, 0],
		[90, 0],
		[45, 0],
		[60, 0],
		[180, 0],
		[2, 0],
		[2, 0],
		[4, 0],
		[0, 0],
		[4, 0],
		[2, 0],
		[40,0] # 13 - счетчик сбора добычи. Мобы пропадают через 2 минуты 

	]

	attack_color_low1	=(0,120,120)
	attack_color_high1	=(10,255,255)
	attack_color_low2 	=(170,120,120)
	attack_color_high2	=(180,255,255)

	health_color_low1	=(50,140,220)
	health_color_high1	=(65,255,255)

	astral_color_low1	=(145,80,200)
	astral_color_high1	=(155,255,255)

	enemy_type_yellow_low = (30,100,108)
	enemy_type_yellow_high = (66,255,255)

	enemy_type_blue_low = (100,130,128)
	enemy_type_blue_high = (122,255,255)

	enemy_type_red_low = (0,100,128)
	enemy_type_red_high = (20,255,255)

	target_in_front_low1	=(0,80,100)
	target_in_front_high1	=(35,255,255)
	target_in_front_low2 	=(145,80,100)
	target_in_front_high2	=(180,255,255)

	coordinates_color_low	=(0,0,245)
	coordinates_color_high	=(180,50,255)

	#enemy_yellow_low1		=(28,135,210) #135,210 #100, 150 желтая полоса животных в главной области экрана 
	#enemy_yellow_high1	=(32,150,255) #148,217





	key_codes = []