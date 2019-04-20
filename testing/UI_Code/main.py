from os import listdir
from os.path import isfile, join
from math import ceil

import kivy
from kivy.app import App
from kivy.clock import Clock
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
#from kivy.uix.popup import Popup
#from kivy.properties import ObjectProperty
#from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition 

"""
gameCtrl = Game() # give initail settings
gamectrl.make_start_LED_array(chess.PAWN) # tell the game to lisght up all pawn square
gameCtrl.chexk_start_up_state() # call after above function to make sure all pawns have beem placed. Will return true once condition is met. then move on to next piece. 
gameCtrl.refresh_board() returns board, time left for each player

"""

screen_list = []

class SaveGameScreen(Screen):
	
	def on_leave(self):
		screen_list.append(self.name)


class PlayGameScreen(Screen):
	
	def on_leave(self):
		screen_list.append(self.name)


class LoadGameScreen(Screen):

	def __init__(self, **kwargs):
		super(Screen, self).__init__(**kwargs)	

	def on_leave(self):
		screen_list.append(self.name)

	def on_enter(self, *args):
		self.ids.table.clear_widgets()

		saved_games = self.list_games()
		saved_games.sort()
		for game in saved_games:
			bttn2 = ToggleButton(text=str(game), size_hint_y=0.2, group="g")
			self.ids.table.add_widget(bttn2)
		
		spaces = len(saved_games) % 3
		if spaces == 1:
			self.ids.table.add_widget(Label(text="", size_hint_y=0.2))
			self.ids.table.add_widget(Label(text="", size_hint_y=0.2))
		elif spaces == 2:
			self.ids.table.add_widget(Label(text="", size_hint_y=0.2))
		
		y_spacing = 1 -  0.2*ceil(len(saved_games) / 3)
		for itr in range(0, 3):
			self.ids.table.add_widget(Label(text="", size_hint_y=y_spacing))

	def list_games(self):
		myPath = "./saves"
		return [f for f in listdir(myPath) if isfile(join(myPath, f))]
	
	def load_game(self, *args):
		pass

class SettingsScreen(Screen):

	def __init__(self, **kwargs):
		super(Screen, self).__init__(**kwargs)	

	def on_leave(self):
		#screen_list.append(self.name)
		pass
	
	def switch(self, root):
		val = not root.ids.sw1.active
		root.ids.sw2.disabled = val
		root.ids.sw3.disabled = val
		root.ids.sw4.disabled = val
		root.ids.sw5.disabled = val

	def btn_back(self):
		self.manager.current = screen_list[-1]
	
	def btn_save(self):
		#game.settings()
		self.btn_back()

class BoardSetupScreen(Screen):

	def on_enter(self):
		self.clock = Clock.schedule_interval(self.clock_callback, 3)#10 / 1000)

	def clock_callback(self, dt, *args):
		root = self.ids
		root.img_white.source = "img/knight_white.jpg"
		root.img_black.source = "img/knight_white.jpg"
		print(dt)

	def on_leave(self):
		screen_list.append(self.name)
		self.clock.cancel()

	def btn_skip(self, root):
		pass

class StartScreen_p1(Screen):
	handicap = [None, None]

	def __init__(self, **kwargs):
		super(Screen, self).__init__(**kwargs)	

	def on_leave(self):
		screen_list.append(self.name)

	def on_enter(self, *args):
		root = self.ids
		root.p1_color_white.state = "down"
		root.p1_color_black.state = "normal"
		root.slide_ai_diff.value = 3
		root.tutor_on.state = "down"
		#for child in root.p1_handicap.children:
		#	child.state = "normal"
		#root.p1_handicap_none.state = "down"
		#for child in root.cpu_handicap.children:
		#	child.state = "normal"
		#root.cpu_handicap_none.state = "down"
		root.slide_game_timer.value = 0
		root.slide_move_timer.value = 0
		

	def start_game(self, *args):
		root = args[0]
		
		settings = {}
		settings["num players"] = 1
		settings["p1 color"] = root.ids.p1_color_white.state == "down"
		settings["p2 color"] = None
		settings["ai diff"] = root.ids.slide_ai_diff.value
		settings["tutor on"] = root.ids.tutor_on.state == "down"
		settings["game timer"] = root.ids.slide_game_timer.value
		settings["move timer"] = root.ids.slide_move_timer.value
	
		#Game.start(settings)
		self.manager.current = "board_setup"

	def btn_clicked(self, p1=0, p2=0):
		if p1 != 0:
			self.handicap[0] = p1
		elif p2 != 0:
			self.handicap[1] = p2

class StartScreen_p2(Screen):
	handicap = [None, None]

	def __init__(self, **kwargs):
		super(Screen, self).__init__(**kwargs)	

	def on_leave(self):
		screen_list.append(self.name)

	def on_enter(self, *args):
		root = self.ids
		root.p1_color_white.state = "down"
		root.p1_color_black.state = "normal"
		root.p2_color_white.state = "normal"
		root.p2_color_black.state = "down"
		root.tutor_on.state = "down"
		#for child in root.p1_handicap.children:
		#	child.state = "normal"
		#root.p1_handicap_none.state = "down"
		#for child in root.p2_handicap.children:
		#	child.state = "normal"
		#root.p2_handicap_none.state = "down"
		root.slide_game_timer.value = 0
		root.slide_move_timer.value = 0

	def start_game(self, *args):
		root = args[0].ids

		p1_color = root.p1_color_white.state
		p2_color = root.p2_color_white.state
		
		if p1_color == p2_color:
			return

		settings = {}
		settings["num players"] = 2
		settings["p1 color"] = root.p1_color_white.state == "down"
		settings["p2 color"] = not settings["p1 color"]
		settings["ai diff"] = None
		settings["tutor on"] = root.tutor_on.state == "down"
		settings["game timer"] = root.slide_game_timer.value
		settings["move timer"] = root.slide_move_timer.value

		#Game.start(settings)
		self.manager.current = "board_setup"

	def btn_clicked(self, p1=0, p2=0):
		if p1 != 0:
			self.handicap[0] = p1
		elif p2 != 0:
			self.handicap[1] = p2
	
class HomeScreen(Screen):
	
	def on_leave(self):
		screen_list.append(self.name)

class ChessUIApp(App):

	def build(self):
		sm = ScreenManager(transition=NoTransition()) 
		sm.add_widget(HomeScreen(name="home"))
		sm.add_widget(StartScreen_p1(name="start_p1"))
		sm.add_widget(StartScreen_p2(name="start_p2"))
		sm.add_widget(BoardSetupScreen(name="board_setup"))
		sm.add_widget(SettingsScreen(name="settings"))
		sm.add_widget(LoadGameScreen(name="load"))
		sm.add_widget(SaveGameScreen(name="save"))
		

		return sm

ChessUIApp().run()
