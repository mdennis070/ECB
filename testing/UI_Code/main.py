import kivy
from kivy.app import App
from kivy.clock import Clock
#from kivy.uix.gridlayout import GridLayout
#from kivy.uix.boxlayout import BoxLayout
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

class BoardSetupScreen(Screen):
	pass

class StartScreen_p1(Screen):

	def btn_clicked(self, val_1, val_2, val_3):
		print(val_1, val_2, val_3)
	
class HomeScreen(Screen):
	pass
	#def btn_press_single_player(self):
	#	self.manager.current = "start_p1"

def clock_callback(dt):
	pass
	#print(time.ctime())

class ChessUIApp(App):

	def build(self):
		sm = ScreenManager(transition=NoTransition()) 
		sm.add_widget(HomeScreen(name="home"))
		sm.add_widget(StartScreen_p1(name="start_p1"))
		sm.add_widget(BoardSetupScreen(name="board_setup"))

		clock = Clock.schedule_interval(clock_callback, 10 / 1000)

		return sm

ChessUIApp().run()
