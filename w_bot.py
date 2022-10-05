from settings import *
from mv import Mover

class HttpProcessor(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('content-type','text/html')
		self.end_headers()
		self.wfile.write("hello !".encode())


def make_screenshot(coords, rand=''):
	global screenshot

	#logger.info (coords)
	for asset, x1, y1, x2, y2, source, ypos, xpos, color in coords:
		#logger.info("begin of reading screenshot")
		#logger.info("end of reading screenshot")
		resized = screenshot [int(y1):int(y2), int(x1):int(x2)]
		#logger.info ("x1=" + str(x1) + " y1=" + str(y1) + " x2=" + str(x2) + " y2=" + str(y2)+ " asset="+asset)

		screenshot_name = 'var/'+str(resolution)+'/'+asset+rand+'.png'
		#logger.info(screenshot_name)
		cv.imwrite(screenshot_name, resized)
		#logger.info("screenshot saved")
		#screenshot.save(screenshot_name)
	return screenshot_name


def key_1():
	global stateOn
	if stateOn.get():
		stateOn.set(False)
	else:
		stateOn.set(True)
		x=threading.Thread(target=game_bot)
		x.start()
	logger.info("f1")

def key_2():
	global send_keys_mouse_events
	global mouse_start_x
	global mouse_start_y, coords


	if send_keys_mouse_events.get():
		send_keys_mouse_events.set(False)
		startListener(False)
	else:
		send_keys_mouse_events.set(True)
		mouse_start_x = mouse.Controller().position[0]
		mouse_start_y = mouse.Controller().position[1]
		startListener(True)
	print("F2")
	logger.info("f2")

def key_3():
	global screenshot, coords, coordinates_color_low, coordinates_color_high
	target = (5369, 2886)

	logger.info("f3")

	print(Mover.send_request( (ord('d')), 9, "on_dl"))
	time.sleep(3)
	print(Mover.send_request( (ord('d')), 9, "on_dl"))
	return

	while True:
		capture_fromcam(1)
		screenshot = cv.imread ('var/screen.png')
		logger.info("f3--- making screenshot ")
		make_screenshot (coords)
		logger.info("f3--- screenshot made")
		start = Mover.get_coordinates()
		if start[0]>100 and start[1]>100: break

	logger.info("f3--- coordinates captured")
	Mover.move_forward()
	logger.info("f3--- moved forward")
	time.sleep (1)

	Mover.stop_move()
	logger.info("f3--- move stopped")	
	#time.sleep (0.5)
	capture_fromcam(1)
	logger.info("f3--- captured from cam")
	screenshot = cv.imread ('var/screen.png')
	make_screenshot (coords)
	stop = Mover.get_coordinates()
	logger.info("f3--- end f3")
	logger.info(Mover.find_degree(start, stop, target))

	Mover.make_turn (start, stop, target)
	logger.info("f3--- turn made")



def f12():
	global exit
	logger.info ("stop")
	#threading.stop()

	Listener = None
	exit = True
	import sys
	sys.exit()
	return False

def on_keypress(key):
	global send_keys_mouse_events
	#print("key_press")
	#print(f"send_keys {send_keys_mouse_events}, value={send_keys_mouse_events.get()}")
	if send_keys_mouse_events.get():
		#print("trying send keys")
		r=asci_char(key)
		p=random.randint(40,220)
		m="on"
		send_rq(r,p,m)
	else:
		return False

def on_keyrelease(key):
	global stateOn
	global t1
	global send_keys_mouse_events

	if send_keys_mouse_events.get():
		r = asci_char(key)
		p = random.randint(40,70)
		m = "off"
		#logger.info (m)
		if send_arduino_requests.get():
			send_rq(r,p,m)
	else:
		return False

def on_move(x, y):
	#
	global send_keys_mouse_events
	global send_arduino_requests
	global mouse_start_x
	global mouse_start_y

	if send_keys_mouse_events.get():
		if x == mouse_start_x and y == mouse_start_y:
			logger.info("mouse not move")
			r = 0
			p = 0
		else:
			r = x - mouse_start_x
			p = y - mouse_start_y
			m = "mv"
			#print(mouse.Controller().position)
			if send_arduino_requests.get():
				send_rq(r,p,m)
			
		
		#print("x="+str(x)+" y="+str(y))
		#print("start x="+str(mouse_start_x)+" start y="+str(mouse_start_y))
		#print("current x="+str(r)+" current y="+str(p))
		#print("")
	else:
		return False

def on_click(x,y, button, pressed):
	#
	global send_keys_mouse_events

	if send_keys_mouse_events.get():
		r=x
		p=y
		if button == mouse.Button.left:
			m="b1"
		if button == mouse.Button.right:
			m="b2"
		if pressed:
			m=m+"on"
		else:
			m=m+"off"
		#print(m)
		send_rq(r,p,m)
	else:
		return False

def main ():
	global Listener
	global exit
	global stateOn


	#if find_button_coordinates.get():
	#	stateOn = True
	#	game_bot()

	logger.info("Starting http servers...")

	#threading.Thread(target=start_local_http_server).start()

	logger.info("Local http server started")

	threading.Thread(target=start_remote_http_server).start()
	logger.info("Remote http server started")

	threading.Thread(target=win.run).start()
	logger.info("main window started")
	

	print ("enter")
	startListener(False)

	print ("not exit")

	quit()


def game_bot ():
	global stateOn
	global t1, localtime, t_start
	global coords, last_trying_key
	global window
	global bg, pbar_width, pbar_enemy_type
	global color_green, color_red, color_yellow, color_lt_gray, color_gray, color_blue
	global screenshot
	global loot_time

	last_trying_key = ''
	t_start = int(time.time())
	target_needs_try=0
	target_needs_to_be_in_front_of_you =False
	trying_to_begin_attack = False
	time_of_begin_attack = 0
	spells_time[13][1] = time.time() # первій сбор лута пропускаем

	while stateOn.get():
				
		i= int(-1)
		t1 = int(time.time())
		localtime = time.localtime()

		logger.info("---------------------- Starting stateOn loop ---------------------")

		bg['tab'].set(color_lt_gray)

		if webcam_processing.get():
			capture_fromcam()

		screenshot = cv.imread ('var/screen.png')

		if Saved_coords_processing.get():
			make_screenshot (saved_coords, "_"+str(time.strftime("%Y-%m-%d %H-%M-%S", localtime)))

		make_screenshot (coords)
		for asset, x1, y1, x2, y2, source, ypos, xpos, color in saved_coords:
			i +=1 
			if asset!="button_area" and asset!="hero_status_area" and asset!="sys_msg_area":
				find_template (source, asset, ypos, xpos, i)
		logger.info ("finished find_templates")

		make_screenshot(status_lines) # проверка статусов характеристик с барами (здоровье, атака)
		logger.info("finished make_screenshot(status_lines)")

		key = ""
		dlay=0

		win.update()
		enemy_present = False
		enemy_type_beast = False
		enemy_type_is_blue =False


		# --------- type of enemy ------------------
		#if check_hero_bar_status(enemy_type_red_low, enemy_type_red_high, "enemy_type"): #enemy_attack, средняя точка на графе. full - x=71, 50% - x=37
		#	logger.info("enemy_type_is_red")
		#	enemy_type_is_red = True
		#	pbar_enemy_type["enemy_type"].set(color_red)

		#	if trying_to_begin_attack: # 
		#		time_of_begin_attack = time.time()
		
		#elif check_hero_bar_status(enemy_type_yellow_low, enemy_type_yellow_high, "enemy_type"): #health, средняя точка на графе. full - x=71, 50% - x=37
		#	logger.info ("enemy_type_beast")
		#	enemy_type_beast = True
		#	pbar_enemy_type["enemy_type"].set(color_yellow)
		
		#elif check_hero_bar_status(enemy_type_blue_low, enemy_type_blue_high, "enemy_type"): #health, средняя точка на графе. full - x=71, 50% - x=37
		#	enemy_type_is_blue = True
		#	pbar_enemy_type["enemy_type"].set(color_blue)
		#	logger.info("enemy_type_is_blue")
		if act_spells[13] == True:
			enemy_type_beast = True 
			pbar_enemy_type["enemy_type"].set(color_yellow)
			logger.info ("beast enemy")
		else: 
			pbar_enemy_type["enemy_type"].set(color_lt_gray)
			logger.info ("no enemy")


		if check_attack_status("target_in_front", target_in_front_low1, target_in_front_high1, target_in_front_low2, target_in_front_high2):
			target_in_front = True
			pbar_width["target_in_front"].set(pbar_window_width)
			logger.info("-------------------------------------------------target in front")
		else:
			target_in_front = False
			pbar_width["target_in_front"].set(1)
			

		# --------- End type of enemy -----------------------

		if act_spells[12] == True:
			logger.info("enemy_attack is on")
			enemy_attack = True

		else:
			enemy_attack = False
			logger.info("enemy_attack is off")

		astral_power = check_hero_bar_status(astral_color_low1, astral_color_high1, "astral") #astral, средняя точка на графе. full - x=71, 50% - x=37
		logger.info("astral_power is "+str(astral_power))

		enemy_health = check_hero_bar_status(health_color_low1, health_color_high1, "enemy_health") #astral, средняя точка на графе. full - x=71, 50% - x=37
		logger.info ("enemy_health is "+str(enemy_health))
		
		hero_health = check_hero_bar_status(health_color_low1, health_color_high1, "health") #health, средняя точка на графе. full - x=71, 50% - x=37
		logger.info("hero_health = "+str(hero_health))

		if enemy_health > 10 and enemy_type_beast == False:
			enemy_type_is_blue = True

		if hero_health < hero_low_health_respawn_value:

			#if act_spells[11] == True: # 12- кнопка. Regrowth
			#logger.info (health_line)
			key='6'
			dlay=random.randint(90,180)
			modifier="on_dl"

		# --------------- begin of attack commands -------------------------------------------------------------------------
		elif act_spells[12] == True: #attack
			attack_status_is_on = True
			logger.info ("attack_status is on")

			if check_hero_bar_status(astral_color_low1, astral_color_high1, "astral")>90 and last_trying_key!='4':
				key='4'
				dlay=random.randint(100,250)
				modifier="on_dl"
		

			elif t1 - spells_time[6][1] > spells_time[6][0]: #act_spells[3] == True: # 4- кнопка. 3 мин cooldown
				logger.info("t1="+str(t1)+" t2=" + str(spells_time[6][1]) + " t3=" + str(spells_time[6][0]))
				spells_time[6][1]=t1
				key='v'
				dlay=random.randint(100,250)
				modifier="on_dl"

			elif t1 - spells_time[5][1] > spells_time[5][0]: #act_spells[5] == True: # 6- кнопка. 1,5 мин спелл
				spells_time[5][1]=t1
				key='h'
				dlay=random.randint(100,250)
				modifier="on_dl"

			elif t1 - spells_time[4][1] > spells_time[4][0]: #act_spells[4] == True: # 5 - кнопка. 60 сек спелл
				spells_time[4][1]=t1
				key='g'
				dlay=random.randint(100,250)
				modifier="on_dl"
			
			elif t1 - spells_time[3][1] > spells_time[3][0]: #act_spells[4] == True: # 5 - кнопка. 45 сек спелл
				spells_time[3][1]=t1
				key='f'
				dlay=random.randint(100,250)
				modifier="on_dl"
		
			#elif act_spells[2] == True: # 3 - кнопка. зависит от наполнения бара с маной
			#	key='t'
			#	dlay=random.randint(40,90)
			#	modifier="on"

			elif act_spells[10] == True: # - кнопка. cStarfire. 2 sec
				if target_in_front:
					turn_around_and_attack ('5', target_needs_try)
					continue
				else:
					key='5'
					dlay=random.randint(90,180)
					modifier="on_dl"
					target_needs_try =0

			elif act_spells[8] == True: # 3- кнопка внизу. Wraith. 2 sec
				if target_in_front:
					turn_around_and_attack ('3', target_needs_try)
					continue					
				else:
					key='3'
					dlay=random.randint(90,180)
					modifier="on_dl"
					target_needs_try =0

			elif act_spells[7] == True: # 2- кнопка. 
				key='2'
				dlay=random.randint(90,180)
				modifier="on_dl"
		
			elif act_spells[6] == True: # 1- кнопка. 
				key='1'
				dlay=random.randint(90,180)
				modifier="on_dl"
			else:
				key='2'
				dlay=random.randint(90,180)
				modifier="on_dl"
				logger.info ("Other attacks not ready or not in conditions. Try simple attack, eg. 1, 2")
				#logger.info ("key="+key+", ")
				new_target_attack()
				key=''
		else:  # loot
			if t1 - spells_time[13][1] > spells_time[13][0]: #act_spells[4] == True: # 5 - кнопка. 45 сек спелл
				spells_time[13][1]=t1
				time_of_begin_loot = time.time()
				logger.info("trying to catch loot")
				while time_of_begin_loot + loot_time > time.time():
					key = "r"
					dlay = random.randint(70,110)
					m = "on_dl"
					send_rq(ord(key), dlay, "on_dl") 
					time.sleep(dlay/1000)
				key = ""
			if enemy_type_is_blue is False and enemy_attack is False:
				trying_to_begin_attack = True
				#new_target_attack()
				find_new_target()
			
		#time.sleep(0.5)
		if len(key)>0:
			press_spell_key (key, dlay, modifier)
			#send_rq(ord(key),dlay,"off")
			#logger.info("time from begining = "+str(t_start-t1))

			if random.randint(1,3)==1:
				find_new_target()

		# ------- end of attack commands ------------------------------------------------------------------------------
def press_spell_key(key, dlay, modifier):
	global last_trying_key, bg

	last_trying_key = key
	logger.info("--- Key "+key+" ----")
	try:
		bg[key].set(color_green)  # изменение цвета выбранной кнопкb
	except:
		True
		# unused keys skip like 'd' 'a'
	win.update()

	send_rq(ord(key),dlay,modifier)

def turn_around_and_attack(attack_key, target_needs_try):
	global last_trying_key

	if target_needs_try >= 1:
		if random.randint(0,1) ==1:
			key ='a'
		else:
			key='d'
		dlay=random.randint(1100,1150)
		modifier="on_dl"
		target_needs_try =0	
		logger.info (f"sleeping for {dlay/1000}ms before return complete")
		time.sleep(dlay/1000)
		press_spell_key(key, dlay, modifier)
		
		dlay=random.randint(90,180)
		press_spell_key(attack_key, dlay, modifier)
		logger.info (f"sleeping for {dlay/1000}ms before spell complete")
		dlay=random.randint(900,1150)
		time.sleep(dlay/1000)
	else:
		logger.info ("from turn_around_and_attack.... target_needs_try ="+str(target_needs_try))
		new_target_attack()
		target_needs_try +=1


def check_color_line(color_mask): # проверка баров здоровья, атаки и т.д.
	global show_color_lines_info

	moments = cv.moments(color_mask, 1) # получим моменты 
	x_moment = moments['m01']
	y_moment = moments['m10']
	area = moments['m00']
	if x_moment==0 or area==0:
		if show_color_lines_info.get():
			logger.info ("check_color_line return 0")
		return 0
	x = int(x_moment / area) # Получим координаты x,y кота
	y = int(y_moment / area) # и выведем текст на изображение
	if show_color_lines_info.get():
		logger.info("check_color_line x_moment="+str(x_moment)+", y_moment="+str(y_moment))
		logger.info("check_color_line x="+str(x)+", y="+str(y))
		logger.info("----------------------")
	return x

def check_hero_bar_status(color_low, color_high, asset):
	global show_color_lines_info
	global pbar, pbar_full, pbar_width, pbar_window_width

	if show_color_lines_info.get():
		logger.info("----------------------")
		logger.info ("current asset="+asset)
	#----------- check health status
	frame_hsv = cv.imread ('var/'+str(resolution)+'/'+asset+'.png')
	#<class 'numpy.ndarray'> (380, 596, 3)
	frame_hsv = cv.cvtColor(frame_hsv, cv.COLOR_BGR2HSV)
	lower1 = np.array(color_low, dtype = "uint8")
	upper1 = np.array(color_high, dtype = "uint8")
 
	mask = cv.inRange(frame_hsv, lower1, upper1)        #применяем маску по цвету
	if show_cv_windows. get():
		#logger.info("lower1:")
		#logger.info(lower1)
		#logger.info("upper1:")
		#logger.info(upper1)
		#logger.info("mask:")
		#logger.info(mask)
		cv.imshow(asset, mask)
		cv.waitKey(0)
	c = check_color_line(mask[0])
	if asset != "enemy_type":
		pbar_width[asset].set(int(pbar_window_width/pbar_full*c)) # изменение ширины прогресс-баров в GUI
	win.update()
	return c

def check_attack_status(asset, attack_color_low1=attack_color_low1, attack_color_high1=attack_color_high1, attack_color_low2=attack_color_low2, attack_color_high2=attack_color_high2): # проверка текущего состояния атаки по красному ореолу вокруг окошек героев
	global show_color_lines_info
	global pbar_width

	#----------- check attack status
	if show_color_lines_info.get():
		logger.info("----------------------")
		logger.info ("current asset="+asset)
	frame_hsv = cv.imread ('var/'+str(resolution)+'/'+asset+'.png')
	#<class 'numpy.ndarray'> (380, 596, 3)
	frame_hsv = cv.cvtColor(frame_hsv, cv.COLOR_BGR2HSV)
	lower_red1 = np.array(attack_color_low1, dtype = "uint8")
	upper_red1 = np.array(attack_color_high1, dtype = "uint8")
	lower_red2 = np.array(attack_color_low2, dtype = "uint8")
	upper_red2 = np.array(attack_color_high2, dtype = "uint8")
 
	red_mask1 = cv.inRange(frame_hsv, lower_red1, upper_red1)        #применяем маску по цвету
	red_mask2 = cv.inRange(frame_hsv, lower_red2, upper_red2)  #для красного таких 2
	red_mask_full = red_mask1 + red_mask2
	if show_cv_windows.get():
		cv.imshow(asset, red_mask_full)
		cv.waitKey(0)
	if check_color_line(red_mask_full[0]):
		pbar_width[asset].set(pbar_window_width)
		logger.info("attack is active")
		return True
	else:
		pbar_width[asset].set(1)
		if asset != "target_in_front":
			logger.info ("find new target called from check_attack_status func")
			find_new_target()
	logger.info("-------------------------")

def find_template(img1, templ1, ypos, xpos, i):
	global show_color_lines_info
	global bg
	global color_gray
	global color_lt_gray

	img = cv.imread('var/2/'+img1+'.png',0)
	img2 = img.copy()
	template = cv.imread('var/2/src/'+templ1+'.png',0)
	w, h = template.shape[::-1]
	# All the 6 methods for comparison in a list
	methods = [
				'cv.TM_SQDIFF'] 
				#'cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR','cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
	for meth in methods:
		img = img2.copy()
		method = eval(meth)
		# Apply template Matching
		res = cv.matchTemplate(img,template,method)
		min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
		# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
		if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
			top_left = min_loc
		else:
			top_left = max_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)
		if find_button_coordinates.get():
			logger.info ("asset = "+templ1 +", min_val="+str(min_val)+" max_val="+ str(max_val)+" min_loc="+ str(min_loc)+" max_loc="+  str(max_loc)+" ypos="+  str(ypos)+" xpos="+  str(xpos))

		if (ypos-5 < min_loc[0] < ypos+5) and (xpos-5 < min_loc[1] < xpos+5) : # 0 - искать в любой позиции, без привязки к кокретной точке.
			logger.info (templ1+' yes')
			bg[templ1].set(color_lt_gray) # цвета кнопок в окне
			f = True
		else :
			if (ypos==xpos==0):
				logger.info (templ1+' yes')
				bg[templ1].set(color_lt_gray)
				f = True
			else:			
				logger.info (templ1+' no')
				bg[templ1].set(color_gray)
				f = False
		act_spells.insert(i, f)	
		win.update()
		if find_button_coordinates.get():
			cv.rectangle(img,top_left, bottom_right, 255, 2)
			plt.subplot(121),plt.imshow(res,cmap = 'Spectral')
			plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
			plt.subplot(122),plt.imshow(img,cmap = 'Spectral')
			plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
			plt.suptitle(templ1)
			plt.show()


def find_new_target():
	global bg
	bg['q'].set(color_green)
	win.update()
	send_rq	(ord('q'), random.randint(90,180),"on_dl") #keyboard.Key.tab
		
	#send_rq	(asci_char(keyboard.Key.tab), random.randint(40,70),"off")

def new_target_attack():
	global bg

	logger.info ("new target attack")
	if random.randint(1,2)==1:
		rand1="'1'"
		rand2="'2'"
	else:
		rand1="'2'"
		rand2="'1'"
	bg[rand1[1:2]].set(color_green)
	win.update()
	send_rq	(asci_char(rand1), random.randint(90,180),"on_dl")

	#send_rq	(asci_char(rand1), random.randint(40,70),"off")
	dlay=2+random.randint(10,200)/1000
	logger.info (f"sleeping for {dlay}ms before return complete")
	time.sleep(dlay)
	bg[rand2[1:2]].set(color_green)
	win.update()
	send_rq	(asci_char(rand2), random.randint(90,180),"on_dl")
	#send_rq	(asci_char(rand2), random.randint(40,70),"off")


def send_rq(r,p,m, retries=0):
	global send_arduino_requests
	global time_keyboard_last_on_dl
	if send_arduino_requests.get() == False:
		return "send_arduino_requests = False"
		logger.info("send_arduino_requests = False")
	logger.debug("send_rq triyng "+str(retries))
	if retries > 10: return
	try:
		data = {"r": r, "p" :p, "m": m, "e": ""}
		if m == "on_dl":
			try:
				logger.keylog(f"Pause before: {str(round((time.time()-time_keyboard_last_on_dl)*100))}ms, Key: {chr(r)}, Delay: {p}, Mod: {m}")
				logger.info(f"EMU === Key: {chr(r)}, Delay: {p}, Mod: {m}")
			except UnicodeEncodeError:
				logger.keylog(f"Pause before: {str(round((time.time()-time_keyboard_last_on_dl)*100))}ms, Key: {r}, Delay: {p}, Mod: {m}")
				logger.info(f"EMU === Key: {r}, Delay: {p}, Mod: {m}")
		if m == "on":
			try:
				logger.info(f"EMU === Key: {chr(r)}, Delay: {p}, Mod: {m}")
			except UnicodeEncodeError:
				logger.info(f"EMU === Key: {r}, Delay: {p}, Mod: {m}")
		r = requests.get("http://"+arduino_ip, params={"r": r, "p" :p, "m": m, "e": ""})#, timeout=1)
		time_keyboard_last_on_dl = time.time()
	except requests.exceptions.ConnectTimeout as e:
		retries+=1
		logger.info("triyng "+retries)
		send_rq(r, p, m, retries)
	except requests.exceptions.RequestException as e:
		logger.info ("OOps: Something Else",e)
	else:
		True
		#logger.info("send_rq else")
	finally:
		return r

def capture_fromcam (VideoCapture = -1):
		global webcam
		global update_window_image, webcam_extra_screenshots
		localtime = time.localtime()

		if update_window_image.get()==False:
			logger.info("-----------------------------------------------------------------------------")
			logger.info ("capture_fromcam step")
		if VideoCapture>-1:
			webcam.release()
			webcam = cv.VideoCapture(VideoCapture)
			webcam.set(3, 1920)
			webcam.set(4, 1080)
			#time.sleep(1)
		success, screenshot = webcam.read()
		
		if success:
			screenshot_name = 'var/screen'
			if webcam_window_show:
				scale_percent = 60 # percent of original size
				width = int(screenshot.shape[1] * scale_percent / 100)
				height = int(screenshot.shape[0] * scale_percent / 100)
				dim = (width, height)
				resized = cv.resize(screenshot, dim)
				cv.imshow(arduino_ip, resized)
			#if cv.waitKey(100) & 0xFF == ord('q'):
			#	quit()
			cv.imwrite(screenshot_name+".png", screenshot)
			if update_window_image.get():
				win.update_screenshot()
			if webcam_extra_screenshots.get():
				logger.info("Saving webcam_extra_screenshot -- "+str(time.strftime("%Y-%m-%d %H-%M-%S", localtime))+".png")
				cv.imwrite(screenshot_name+"_"+str(time.strftime("%Y-%m-%d %H-%M-%S", localtime))+".png", screenshot)
			#logger.info ("capture_fromcam step 3")
			#cv.destroyAllWindows()
			#logger.info ("capture_fromcam step 4")
			#cv.VideoCapture(1).release()		
			#logger.info ("capture_fromcam step 5")

def asci_char(key):
	#logger.info (Key)
	if key == keyboard.Key.tab:
		return 179
	elif key == keyboard.Key.up:
		return 218
	elif key == keyboard.Key.space:
		return 32
	elif key == keyboard.Key.down:
		return 217
	elif key == keyboard.Key.left:
		return 216
	elif key == keyboard.Key.right:
		return 215
	elif key == keyboard.Key.enter:
		return 176
	elif key == keyboard.Key.up:
		return 218
	elif key == keyboard.Key.alt:
		return 130	
	elif key == keyboard.Key.alt_l:
		return 130	
	elif key == keyboard.Key.alt_r:
		return 130	
	elif key == keyboard.Key.ctrl:
		return 132
	elif key == keyboard.Key.ctrl_l:
		return 132
	elif key == keyboard.Key.ctrl_r:
		return 132
	elif key == keyboard.Key.backspace:
		return 178
	elif key == keyboard.Key.shift:
		return 129
	elif key == keyboard.Key.shift_l:
		return 129
	elif key == keyboard.Key.shift_r:
		return 129
	elif key == keyboard.Key.esc:
		return 177
	elif key == keyboard.Key.insert:
		return 209
	elif key == keyboard.Key.delete:
		return 212
	elif key == keyboard.Key.page_up:
		return 211
	elif key == keyboard.Key.page_down:
		return 214
	elif key == keyboard.Key.home:
		return 210
	elif key == keyboard.Key.end:
		return 213
	elif key == keyboard.Key.caps_lock:
		return 193
	else:	
		#logger.info("Key= "+str(key))
		if len(str(key))<4:
			return (ord(str(key)[1:2]))
		else:
			return 0

def startListener (flag):
	global Listener
	if Listener:
		Listener.stop()
		logger.info ("Listener Stop")
		logger.info (Listener)
		Listener.stop()
		logger.info ("Listener Stop")
		logger.info (Listener)
	with keyboard.Listener(on_press=on_keypress, on_release = on_keyrelease, suppress=flag) as Listener:
		with mouse.Listener(on_move=on_move, on_click = on_click, suppress=flag) as Listener:
			with keyboard.GlobalHotKeys({
					'<'+key1_name+'>': key_1,
					'<'+key2_name+'>': key_2,
					'<'+key3_name+'>': key_3,
					'<f12>': f12
					}, suppress=False) as Listener:
				Listener.join()
	logger.info("Listener started")
	logger.info (Listener)

def start_local_http_server ():

	serv = HTTPServer(("localhost", 80),HttpProcessor)
	serv.serve_forever()

def start_remote_http_server ():

	serv = HTTPServer((server_ip, 80),HttpProcessor)
	serv.serve_forever()


class win(object):
	"""docstring for window"""
	def __init__(self, arg):
		super(window, self).__init__()
		self.arg = arg

		
	def run():
		global arduino_ip
		global send_arduino_requests
		global padx, pady
		global window, window_image, window_copy_of_image, window_label, window_frm_image
		global show_cv_windows
		global webcam_processing, webcam_extra_screenshots
		global Saved_coords_processing
		global find_button_coordinates
		global stateOn, send_keys_mouse_events
		global show_color_lines_info
		global update_window_image
		global saved_coords, bg, btn, pbar, pbar_width, pbar_enemy_type, status_lines
		global WINDOW_IMAGE_SCALE_PERCENT
		
		bg = {}
		btn = {}
		pbar = {}
		pbar_width = {}
		pbar_enemy_type = {}
		pbar_label = {}
		window = tk.Tk()
		i=0
		j=0

		# ------------- variables section ------------
		send_arduino_requests = tk.BooleanVar()
		send_arduino_requests.set(False)

		show_cv_windows = tk.BooleanVar()
		show_cv_windows.set(False)
		
		webcam_processing = tk.BooleanVar()
		webcam_processing.set(False)
		
		find_button_coordinates = tk.BooleanVar()
		find_button_coordinates.set(False)
		
		Saved_coords_processing = tk.BooleanVar()
		Saved_coords_processing.set(False)

		webcam_extra_screenshots = tk.BooleanVar()
		webcam_extra_screenshots.set(True)

		stateOn = tk.BooleanVar()
		stateOn.set(False)

		send_keys_mouse_events = tk.BooleanVar()
		send_keys_mouse_events.set(False)

		show_color_lines_info = tk.BooleanVar()
		show_color_lines_info.set(False)

		update_window_image = tk.BooleanVar()
		update_window_image.set(False)

		for asset, x1, y1, x2, y2, source, ypos, xpos, color in saved_coords:
			bg[asset] = tk.StringVar(value=color_gray)
		bg['tab'] = tk.StringVar(value=color_lt_gray)
		bg['~'] = tk.StringVar(value=color_lt_gray)
		
		# --------------------------------------------

		#window.columnconfigure(0, minsize=250)
		#window.rowconfigure([0, 1], minsize=100)
		

		

		frm1 = tk.Frame(master=window, relief=tk.FLAT, borderwidth=1)
		#frm1.grid(row=0, column=0, padx=padx, pady=pady, sticky="w")
		frm1.pack()

		frm1.columnconfigure([0, 1], minsize=pbar_window_width)

		pbar_enemy_type['enemy_type'] = tk.StringVar(value=color_lt_gray)
		for asset, x1, y1, x2, y2, source, ypos, xpos, color in status_lines:
			#if i == 0 or i == 4:
			#	height = 10
			#else:
			height = 20
			if i>2:
				j=1
				i=0
			pbar_width[asset] = tk.IntVar(value=pbar_window_width)
			pbar[asset] = tk.Canvas(master=frm1, width=pbar_width[asset].get(), height=height, bg=color)
			pbar[asset].create_text(15, 4, text=asset, anchor="nw")
			pbar[asset].grid(row=i, column=j, padx=5, pady=2, sticky="w")

			#pbar_label[asset] = tk.Canvas(master=pbar[asset], width=100, height=20)
			#pbar_label[asset].create_text(1, 1, text=asset, anchor="nw")
			#pbar_label[asset].grid()
			i +=1
		i=1
		j=0


		frm_btn = tk.Frame(master=frm1, relief=tk.FLAT, borderwidth=1)
		frm_btn.grid(row=4, rowspan=2, column=0, columnspan=2, padx=padx, pady=pady, sticky="wn")

		btn['~'] = tk.Button(master=frm_btn, text='~', width=3, height=1, bg=color_lt_gray)
		btn["~"].grid(row=0, column=0, padx=3, pady=3)

		btn['tab'] = tk.Button(master=frm_btn, text='TAB', width=3, height=1, bg=color_lt_gray)
		btn["tab"].grid(row=1, column=0, padx=3, pady=3)

		for asset, x1, y1, x2, y2, source, ypos, xpos, color in saved_coords[0:11]: # 0:11 водим только кнопки
			if i>6: # кнопки в 2 ряда по 6шт в каждом
				j=1
				i=1

			btn[asset] = tk.Button(master=frm_btn, text=asset.upper(), width=3, height=1, bg=bg[asset].get())
			btn[asset].grid(row=j, column=i, padx=3, pady=3)
			i +=1
		


		chk_stateOn = tk.Checkbutton(frm1, text=key1_name+' (запуск бота)', 
		    variable=stateOn, onvalue=True, offvalue=False)
		chk_stateOn.grid(row=0, column=2, padx=padx, pady=pady+5, sticky="w")


		chk_send_keys_mouse_events = tk.Checkbutton(frm1, text=key2_name+' (клава + мышь)', 
		    variable=send_keys_mouse_events, onvalue=True, offvalue=False)
		chk_send_keys_mouse_events.grid(row=0, column=3, padx=padx, pady=pady+5, sticky="w")


		chk_arduino_requests = tk.Checkbutton(frm1, text='Эмулятор', 
		    variable=send_arduino_requests, onvalue=True, offvalue=False)
		chk_arduino_requests.grid(row=1, column=2, padx=padx, pady=pady, sticky="w")

		
		chk_webcam_extra_screenshots = tk.Checkbutton(frm1, text='Снимки вебки', 
		    variable=webcam_extra_screenshots, onvalue=True, offvalue=False)
		chk_webcam_extra_screenshots.grid(row=3, column=2, padx=padx, pady=pady, sticky="w")


		chk_webcam_processing = tk.Checkbutton(frm1, text='Анализ вебки', 
		    variable=webcam_processing, onvalue=True, offvalue=False)
		chk_webcam_processing.grid(row=2, column=2, padx=padx, pady=pady, sticky="w")

		
		chk_Saved_coords_processing = tk.Checkbutton(frm1, text='Заготовки кнопок', 
		    variable=Saved_coords_processing, onvalue=True, offvalue=False)
		chk_Saved_coords_processing.grid(row=1, column=3, padx=padx, pady=pady, sticky="w")


		chk_find_button_coordinates = tk.Checkbutton(frm1, text='Координаты кнопок', 
		    variable=find_button_coordinates, onvalue=True, offvalue=False)
		chk_find_button_coordinates.grid(row=2, column=3, padx=padx, pady=pady, sticky="w")


		chk_show_cv_windows = tk.Checkbutton(frm1, text='Линейные минизаготовки', 
		    variable=show_cv_windows, onvalue=True, offvalue=False)
		chk_show_cv_windows.grid(row=3, column=3, padx=padx, pady=pady, sticky="w")


		chk_show_color_lines_info = tk.Checkbutton(frm1, text='Расчет баров', 
		    variable=show_color_lines_info, onvalue=True, offvalue=False)
		chk_show_color_lines_info.grid(row=1, column=4, padx=padx, pady=pady, sticky="w")


		chk_update_window_image = tk.Checkbutton(frm1, text='Обн. изоб-ние', command=win.update, 
		    variable=update_window_image, onvalue=True, offvalue=False, )
		chk_update_window_image.grid(row=2, column=4, padx=padx, pady=pady, sticky="w")

		window_frm_image = tk.Frame(master=frm1, relief=tk.FLAT, borderwidth=1, width=960, height=540)
		window_frm_image.grid(row=6, column=0, columnspan=6, padx=padx, pady=pady, sticky="w")


		window_image = Image.open('var/screen.png')
		#---- resizing
		scale_percent = WINDOW_IMAGE_SCALE_PERCENT # percent of original size
		width, height= window_image.size
		width = int(width * scale_percent / 100)
		height = int(height * scale_percent / 100)
		dim = (width, height)
		#---- resizing
		window_image = window_image.resize(dim)
		window_copy_of_image = window_image.copy()
		photo = ImageTk.PhotoImage(window_image)
		window_label = tk.Label(window_frm_image, image = photo)
		#window_label.bind('<Configure>', win.resize_image)
		window_label.pack(expand = 1)

		window.title(f"{hero_name}, {arduino_ip}")
		#window.after(100, win.update)
		window.mainloop()


	def resize_image(event):
		global window_image, window_copy_of_image

		new_width = event.width
		new_height = event.height
		window_image = window_copy_of_image.resize((new_width, new_height))
		photo = ImageTk.PhotoImage(window_image)
		window_label.config(image = photo)
		window_label.image = photo #avoid garbage collection

	def update_screenshot():
		global window_image, window_label, window_copy_of_image, window_frm_image
		logger.info ("begin of update screenshot")
		window_image = Image.open('var/screen.png')
		#---- resizing
		scale_percent = WINDOW_IMAGE_SCALE_PERCENT # percent of original size
		width, height= window_image.size
		width = int(width * scale_percent / 100)
		height = int(height * scale_percent / 100)
		dim = (width, height)
		#---- resizing
		window_image = window_image.resize(dim)
		photo = ImageTk.PhotoImage(window_image)
		window_label.config(image = photo)
		window_label.image = photo
		window_label.pack(expand = 1)
		logger.info("end of update screenshot")

	def update():
		global window, webcam_processing, send_keys_mouse_events, localtime
		global window_stop_updates
		global bg, btn, saved_coords
		global pbar_width, status_lines, pbar_enemy_type

		for asset, x1, y1, x2, y2, source, ypos, xpos, color in saved_coords:
			btn[asset].configure(background=bg[asset].get())
		#window.after(100, win.update)	
		btn['~'].configure(background=bg['~'].get())
		btn['tab'].configure(background=bg['tab'].get())	

		for asset, x1, y1, x2, y2, source, ypos, xpos, color in status_lines:
			pbar[asset].configure(width=pbar_width[asset].get())

		pbar['enemy_type'].configure(background=pbar_enemy_type['enemy_type'].get())


		if update_window_image.get() and stateOn.get()==False:
			localtime = time.localtime()
			capture_fromcam()
			window.after(20, win.update)
			#print("window.after(100, win.update)")
			stop_updates=True
		else:
			if window_stop_updates:
				window.after(10000000, win.update)
				print("window.after(10000, win.update)")
				stop_updates = False
			

main()