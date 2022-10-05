import cv2 as cv
import numpy as np
from aiogram import Bot

webcam_number = 0
webcam = cv.VideoCapture(webcam_number, cv.CAP_DSHOW)

#if webcam_processing:
webcam.set(3, 1920)
webcam.set(4, 1080)
webcam.set(5, 15)
cam_dsitortion = "Merlion1080"

#7#
share_bot = Bot(token='504902447:AAFQcok_a6knDNswoUagSUwSuLHrGac3fQc')
share_group = "80162454"
personal_bot = Bot(token='504902447:AAFQcok_a6knDNswoUagSUwSuLHrGac3fQc')
personal_group = "80162454"

color_gray = "gray"
color_lt_gray = "lavender"
color_green = "medium sea green"
color_red = "indian red"
color_blue = "dodger blue"
color_yellow = "gold"

hotkeys = {'1': '<F7>', '2':'<F8>', '3':'<Alt>+<F1>', '4':"`", '5':"'"}


players = {
	"1":{
		"name" : "Goldenva",
		"login": "notarealwowmail@gmail.com",
		"password": "Special4Cev4",
		"wow": 1,
		"maximum_day_session" : 36400,
		"sell_repair": 2500,
		"fly": False,
		"exit": False,
		"not_allow_from": 11,
		"not_allow_to": 12,
		"talents": {
			"Twin Moons": False,
			"Nature's balance": False
		},
		"coordinates_reaching_wayp_range": 0.35, # погрешность достижения цели
		"coordinates_mailbox_reaching_wayp_range": 0.2 # погрешность достижения цели
	}
	,
	"2":{
		"name" : "Sigridsa",
		"login": "tuskarev@gmail.com",
		"password": "Gabella22",
		"wow": 2,
		"maximum_day_session" : 36400,
		"sell_repair": 2000,
		"fly": True,
		"exit": False,
		"not_allow_from": 11,
		"not_allow_to": 12,
		"talents": {
			"Twin Moons": True,
			"Nature's balance": True
		},
		"coordinates_reaching_wayp_range": 0.6, # погрешность достижения цели
		"coordinates_mailbox_reaching_wayp_range": 0.2 # погрешность достижения цели
	}

}

herbal = {
	
	"map_center" : (1610, 686),
	"map_radius" : round(580/2),
	"hsv" :(18, 113, 167, 26, 174, 255), # herbs. stronger
	"stones" : (11, 0, 0, 155, 88, 138),
	"max_sequence" : 9,
	"arrow_radius" : 15,
	"show_windows": False,
	

	"t_start": 0,
	"t_end": 0,
	"y_start": 0,
	"y_end": 0,
	"till_stop": 0,
	"gathering": False,
	"gathered": False,
	"wheel_scrolled": 0,

	"visible_time": 7,
	"visible_count_time": 1
			

}


pbar_full = 12000 # индикация полного бара. вычислчется из логов, по сканированию изображений. моменты opencv
pbar_window_width = 200 # фактическая длина баров в окне
hero_low_health_respawn_value =19000
astral_full_power = 14000
enemy_full_health = 37600
hero_full_health = 32800
sendmail = True


spells = {
	"Goldenva": {
		"bear" : {
			"1": {"cooldown": 2, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"2": {"cooldown": 2, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"3": { "cooldown": 2, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": False, "Enabled":False},
			"4": { "cooldown": 0, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"5": { "cooldown": 4, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": False, "Enabled":False},
			"6": { "cooldown": 32, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": 60, "Enabled":True},
			"7": { "cooldown": 0, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": 55, "Enabled":False},

			
			"x": { "cooldown": 181, "elapsed": 0, "cast": True, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"v": { "cooldown": 181, "elapsed": 0, "cast": True, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"h": { "cooldown": 6, "elapsed": 0, "cast": True, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"g": { "cooldown": 6, "elapsed": 0, "cast": True, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"f": { "cooldown": 91, "elapsed": 0, "cast": True, "casttime": 0, "Click": True, "heal": False, "Enabled":True},
			"t": { "cooldown": 91, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": 50, "Enabled":True},
		}
	},
	"Sigridsa": {
		"moonkin" : {
			"1": {"cooldown": 2, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"2": {"cooldown": 2, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"3": { "cooldown": 2, "elapsed": 0, "cast": False, "casttime": 1.3, "Click": False, "heal": False, "Enabled":True},
			"4": { "cooldown": 0, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"5": { "cooldown": 4, "elapsed": 0, "cast": False, "casttime": 1.3, "Click": False, "heal": False, "Enabled":True},
			"6": { "cooldown": 2, "elapsed": 0, "cast": False, "casttime": 0.6, "Click": False, "heal": 60, "Enabled":True},
			"7": { "cooldown": 15, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": 55, "Enabled":True},

			
			"v": { "cooldown": 181, "elapsed": 0, "cast": True, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"h": { "cooldown": 91, "elapsed": 0, "cast": True, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"g": { "cooldown": 61, "elapsed": 0, "cast": True, "casttime": 0, "Click": False, "heal": False, "Enabled":True},
			"f": { "cooldown": 61, "elapsed": 0, "cast": True, "casttime": 0, "Click": True, "heal": False, "Enabled":False},
			"t": { "cooldown": 91, "elapsed": 0, "cast": False, "casttime": 0, "Click": False, "heal": 30, "Enabled":True},
			"x": { "cooldown": 61, "elapsed": 0, "cast": False, "casttime": 4, "Click": False, "heal": 90, "Enabled":True}
		}
	},
}

key_shortcuts = {
	"loot": {"key": "r", "period": 40, "elapsed": 0, "gather_time": 8, "time_of_begin": 0},
	"friendly_enemy": {"key": "`"},
	"cat_invisible": {"key": "6"},
	"target_enemy": {"key": "z"},
	"accept_group": {"key": "!"},
	"leave_group": {"key": ")"},
	"herbal_view": {"key": "$"},
	"setview": {"key": "%"},
	"mamont_saveview": {"key": "^"},
	"mamont_setview": {"key": "&"},
	"repop": {"key": "@"},
	"retrivecorpse": {"key": "#"},
	"camera_on": 	{'key': '*', 'status': False},
	"camera_off": 	{'key': '(', 'status': False},
	"reload": {"key": "_"},
	"heal": 	{'key': ')', 'status': False},
	"travel": 	{'key': '8', 'status': False},
	"moonkin": 	{'key': '9', 'status': False},
	"cat": 		{'key': '-', 'status': False},
	"bear": 		{'key': '0', 'status': False},
	"mamont": 	{'key': '=', 'status': False},
	"stop_casting": {"key": "e"},
	"heal": {"key": "+", "repeat": 1}, # repeat - count of casts in macros
	"map_zoomin": {"key": "]"},
	"map_zoomout": {"key": "["},
	"pitch_up": {"key": " "},
	"pitch_down": {"key": "{"},
	"retrieve": {"key": "~"},
}

recorpse = {
	"57.41, 54.50": {
		"1":{
			"key": "w",
			"delay": 700,
			"comment": "near invaders and lift to the rest zone"

		},
		"recorpse": True
	},
	"54.15, 38.30": {
		"1":{
			"key": "d",
			"delay": 100,
			"comment": "near birds respawn and lift to the rest zone"
		},
		"2":{
			"key": "w",
			"delay": 1100
		},
		"recorpse": True
	},
	"41.80, 48.52": {
		"1":{
			"key": "w",
			"delay": 1000,
			"comment": "on the mount near dungeon. die on foxes near bridge",
		},
		"recorpse": True
	},
	"42.65, 64.06": {
		"1":{
			"key": "w",
			"delay": 1000,
			"comment": "on the mount near snow. not actual for now",
		},
		"recorpse": True
	},
	"50.14, 72.30": {
		"1":{
			"key": "w",
			"delay":400,
			"comment": "near aspirant's rest",
		},
		"recorpse": True
	},
	"44.05, 28.39": {
		"1":{
			"key": "w",
			"delay":400,
			"comment": "near larion's. blue",
		},
		"recorpse": True
	},
	"61.50, 40.17": {
		"1":{
			"key": "w",
			"delay":1000,
			"comment": "near larion's. blue",
		},
		"recorpse": True
	}
}

first_input_of_coordinates=True
coordinates_error_range = 1 # разность координат более которой считать предыдущие координаты недействительными
coordinates_small_difference_range = 0.03 # разность координат, менее которой, считать координаты равными предыдущим
coordinates_reaching_wayp_range = 0.6 # погрешность достижения цели
coordinates_mailbox_reaching_wayp_range = 0.2 # погрешность достижения цели
coordinates_time_error_range = 7 # сек. разница в измерении времении после которой сохраненные ранее координаты считать недействительными
time_for_turn = 600 # время для разворота на 180гр.
waypoint_time_reach_for_move = 75
waypoint_time_reach_for_aggro = 40
count_30_yard_attack_maxvalue = 20
template_err_pixel_rate = 4
template_non_zero_find = False
cant_reach_waypoint_count = 0
cant_reach_waypoint_count_max = 4

center_cursor_move = {
	"x": 860,
	"y": 630
}

timers = {
	"maximum_for_attack": 300,
	"maximum_for_attack_break": 360,
	"sell_repair": 2500,
	"waypoint_reach_for_aggro": 60,
	"waypoint_reach_for_move": 180,
	"start_of_attack_cycle": 0,
	"last_save_session": 0,
	"period_session_save": 300,
	"current_session": 0,
	"current_session_max": 0,
	"maximum_day_session": 36400, # 32400s - 9 hours
	"session_min_time": 9300,
	"session_max_time": 10400,
	"session_pause_time_min": 10,
	"session_pause_time_max": 50,
	"save_camshot": 15,
	"last_camshot":0,
	"save_camshot_temporary": 0,
	"cannot_reach_lift": 10, # время, после которого отбегаем от портала, чтобы опять подойти близко к порталу на нужное расстояние, чтобы акивировать взаимодействие
	"invite_to_group_max": 20,
	"invite_to_group_start": 0,
	"swiftmend": 10, # repeat healing macros in the to attack
	"coordinates_write_period": 5,
	"coordinates_last_save": 0,
	"pitch_up": 1,
	"pitch_down": 1,
	"window_camshot_update": 15,
	"window_camshot_update_last": 0,
	"window_camshot_temporary": 0,
	"chat_say_send_camshot": 40,
	"chat_say_send_camshot_last": 0
}

arduino_ip = "192.168.2.172"
server_ip = "192.168.88.7"
server_port = 1172
tg_server_port = 1180
folder_name = "src_172_philips274e_2eFHD"

screen_crop = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0} #, 'x2': 119, 'y2': 399}
btn_width=121  # ширина кнопки на экране
btn_diff_x=137   # растояние между крайними левыми/правыми точками кнопки. шаг
btn_posx=500      # координата левого верхнего угла кнопки
btn_posy=420 #+ 16 # 16 -уровень героя 60 
btn_diff_y=142  # разница между первым и вторым рядом кнопок
in_button_difference_y1 = 0 # требует настройки. Настройка включается переменной find_button_coordinates
in_button_difference_y2 = 142 # должны быть помещены в папку src заготовки активных спелов на кнопках. Заготавливается переменной Saved_coords_processing
in_button_difference_x1 = 0

screen_resizing = [0, 0, 0, 0] # x1, y1, x2, y2
screen_rotation_coef = 0
coords = {
"button_area": (btn_posx,btn_posy,btn_posx+btn_diff_x*7, btn_posy+btn_diff_y*2,"",0,0, ""),
"coordinates": (623, 706, 1094, 801,"", 0, 0, "") # Doris PP

#["coordinates", 1120, 251, 1490, 306,"", 0, 0, ""] # 2002
#["coordinates", 1260, 279, 1663, 357,"", 0, 0, ""] # Friz BQuadrada
#["coordinates", 1281, 285, 1642, 357,"", 0, 0, ""] # AR Zhonkai #3
}

status = {
"attack": (1191, 95 , 1267, 159, 20),			#
"enemy_beast": (637, 358 , 748, 397, 20),		#
"enemy_attack": (546, 137 , 609, 192, 20),		#
"30_yard": (256, 104 , 363, 143, 20),			#
"vehicle":	(1202, 756, 1318, 882, 20)			#
#"target_in_front": (1667, 218, 1868, 291)

}

status_lines = {
	"attack": (945, 96, 1179, 159, "", 800, 0, color_red),
	"health": (833, 178, 1265, 255, " ", 0, 0, color_green),				#
	"astral": (830, 259, 1264, 295, " ", 0, 0, color_blue),					#
	"target_in_front": (1699, 228, 1907, 402, "", 1400, 0, color_red),		#
	"enemy_health": (0, 213, 613, 291, " ", 0, 0, color_green),				#
	"enemy_type": (0, 132, 542, 188, " ", 0, 0, color_lt_gray),				#
	"enemy_mana": (0, 313, 620, 361, " ", 0, 0, color_lt_gray),
	"chat": (0, 808, 1073, 1048, " ", 500, 0)				#
	}

digits = {
	"1": (0, 0, 55, 79, " ", 0, 0),
	"2": (55, 0, 101, 79, " ", 0, 0),
	"3": (119, 0, 168, 79, "", 0, 0),
	"4": (168, 0, 211, 79, " ", 0, 0),
	"5": (261, 0, 306, 79, " ", 0, 0),
	"6": (306, 0, 353, 79, " ", 0, 0),
	"7": (375, 0, 423, 79, " ", 0, 0),
	"8": (423, 0, 477, 79, " ", 0, 0)
}



dead = {
	"dead":	(970, 191, 1134, 250, False),				#
	"ghost":	(970, 191, 1134, 250, False)			#
}

widgets = {
	#"1scr_wc_logo": (52, 28, 617, 146, False),
	"1scr_castle":	(1103, 901, 1633, 1032, False),
	"invite_to_group":	(1636, 409, 1747, 682, False),
	"inbox":	(629, 325, 999, 410, False),
	"win_wow_icon":	(155, 439, 313, 672, False)
	,"invaders": (1513, 542, 1571, 598, False)
}

widget_background = {
	"win_bg":	(845, 112, 1306, 205, False)	
}

ocr = {
	"bag": (347, 418, 462, 476)
}

attack_color_low1	=(0,120,120)
attack_color_high1	=(10,255,255)
attack_color_low2 	=(170,120,120)
attack_color_high2	=(180,255,255)

health_color_low1	=(46,75,50)
health_color_high1	=(86,255,255)

astral_color_low1	=(135,80,60)
astral_color_high1	=(165,255,255)

chat_low	=(132,110,127)
chat_high	=(138,137,164)

enemy_type_yellow_low = (30,100,108)
enemy_type_yellow_high = (66,255,255)

enemy_mana_low = (110,240,76)
enemy_mana_high = (122,255,205)

enemy_type_red_low = (0,100,128)
enemy_type_red_high = (20,255,255)

red_low1	=(0,65,100)
red_high1	=(35,255,255)
red_low2 	=(135,65,100)
red_high2	=(180,255,255)

coord_color_low		=(0,0,215)
coord_color_high	=(180,120,255)

win_bg_low 		=(90,37,150)
win_bg_high		=(153,170,217)

win_bg_black_low 		=(0,0,0)
win_bg_black_high		=(180,0,0)

coord_low_threshold = 7500
coord_high_threshold = 8500

#enemy_yellow_low1		=(28,135,210) #135,210 #100, 150 желтая полоса животных в главной области экрана 
#enemy_yellow_high1	=(32,150,255) #148,217


mtx = np.array(
		[[2.52639442e+03, 0.00000000e+00, 1.10650551e+03],
 		[0.00000000e+00, 2.45795088e+03, 6.22374286e+02],
 		[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
 			)
dist = np.array(
		[[ 2.93691116e-01, -1.83414437e+00, -1.90269079e-04,  9.03910231e-04,
   3.44965312e+00]]
  		)