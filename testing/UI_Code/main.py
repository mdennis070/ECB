from game_ctrl import Game

from os import listdir
from os.path import isfile, join
from math import ceil
import datetime

import kivy
from kivy.app import App
from kivy.clock import Clock
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.label import Label
#from kivy.uix.popup import Popup
#from kivy.properties import ObjectProperty
#from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition 
from kivy.cache import Cache

"""
gameCtrl = Game() # give initail settings
gamectrl.make_start_LED_array(chess.PAWN) # tell the game to lisght up all pawn square
gameCtrl.chexk_start_up_state() # call after above function to make sure all pawns have beem placed. Will return true once condition is met. then move on to next piece. 
gameCtrl.refresh_board() returns board, time left for each player

"""
gameCtrl = None
screen_list = []

class SaveGameScreen(Screen):
    
    def on_enter(self):
        root = self.ids
        now = datetime.datetime.now()
        root.textbox_filename.text = "{}".format(now.strftime("%Y-%m-%d %I:%M%p"))
        
    def save_game(self, filename):
        now = datetime.datetime.now()
        date = "{}".format(now.strftime("%Y-%m-%d"))
        global gameCtrl
        gameCtrl.save_game(filename, date)
        self.manager.current = "home"

    def on_leave(self):
        screen_list.append(self.name)


class PlayGameScreen(Screen):

    def on_enter(self):
        self.clock = Clock.schedule_interval(self.clock_callback, 10 / 1000)

    def clock_callback(self, dt):
        global gameCtrl
        gameCtrl.live_move_highlight()
        gameCtrl.assign_highlight()

    def on_leave(self):
        screen_list.append(self.name)
        self.clock.cancel()

    def end_turn(self):
        global gameCtrl
        turn = gameCtrl.end_turn_move()
        self.ids.turn_label.text = "Turn: {}".format(turn)
    
    def game_hint(self):
        global gameCtrl
        gameCtrl.hint()

class LoadGameScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)	

    def on_leave(self):
        screen_list.append(self.name)

    def on_enter(self, *args):
        self.ids.table.clear_widgets()

        saved_games = self.list_games()
        saved_games.sort()
        count = 0
        for game in saved_games:
            game_name = game[:-4]
            bttn2 = ToggleButton(size_hint_y=0.2, group="g", allow_no_selection=False)
            bttn2.text = str(game_name)
            if count == 0:
                bttn2.state = "down"
            self.ids.table.add_widget(bttn2)
            count = count + 1

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
        game_name = None
        
        for game in ToggleButtonBehavior.get_widgets("g"):
            if game.state == "down":
                game_name = game.text
        
        if game_name != None:
            global gameCtrl
            if gameCtrl != None:
                del gameCtrl
            gameCtrl = Game()
            gameCtrl.load_game(str(format(game_name)))
            self.manager.current = "board_setup"
        

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
        root = self.ids
        sw1_val = root.sw1.active # Tile highlighting
        sw2_val = root.sw2.active # legal moves
        sw3_val = root.sw3.active # illegal moves
        sw4_val = root.sw4.active # king check
        sw5_val = root.sw5.active # Last move

        global gameCtrl
        if sw1_val:
            gameCtrl.update_settings(sw2_val, sw3_val, sw4_val, sw5_val)
        else:
            gameCtrl.update_settings(False, False, False, False)
        self.btn_back()

class BoardSetupScreen(Screen):

    current_piece = 1

    def on_enter(self):
        self.clock = Clock.schedule_interval(self.clock_callback, 10 / 1000)
        self.current_piece = 1
        self.ids.img_white.source = "img/pawn_w.png"
        self.ids.img_black.source = "img/pawn_b.png"
        self.ids.piece_name_label.text = "Pawn"
        gameCtrl.make_start_LED_array(self.current_piece)

    def clock_callback(self, dt, *args):
        setup = False

        if self.current_piece < 7:
            setup = gameCtrl.check_start_up_state(self.current_piece)
            gameCtrl.make_start_LED_array(self.current_piece)
        
        if setup:
            self.current_piece = self.current_piece + 1
            root = self.ids

            if self.current_piece == 2:
                #root.img_white.source = "img/knight_white.jpg"
                #root.img_black.source = "img/knight_black.jpg"
                root.img_white.source = "img/knight_w.png"
                root.img_black.source = "img/knight_b.png"
                root.piece_name_label.text = "Kinght"
            elif self.current_piece == 3:
                #root.img_white.source = "img/bishop_white.jpg"
                #root.img_black.source = "img/bishop_black.jpg"
                root.img_white.source = "img/bishop_w.png"
                root.img_black.source = "img/bishop_b.png"
                root.piece_name_label.text = "Bishop"
            elif self.current_piece == 4:
                #root.img_white.source = "img/rook_white.jpg"
                #root.img_black.source = "img/rook_black.jpg"
                root.img_white.source = "img/rook_w.png"
                root.img_black.source = "img/rook_b.png"
                root.piece_name_label.text = "Rook"
            elif self.current_piece == 5:
                #root.img_white.source = "img/queen_white.jpg"
                #root.img_black.source = "img/queen_black.jpg"
                root.img_white.source = "img/queen_w.png"
                root.img_black.source = "img/queen_b.png"
                root.piece_name_label.text = "Queen"
            elif self.current_piece == 6:
                #root.img_white.source = "img/king_white.jpg"
                #root.img_black.source = "img/king_black.jpg"
                root.img_white.source = "img/king_w.png"
                root.img_black.source = "img/king_b.png"
                root.piece_name_label.text = "King"

            if self.current_piece == 7:
                self.manager.current = "play"
            else:
                gameCtrl.make_start_LED_array(self.current_piece)

    def on_leave(self):
        screen_list.append(self.name)
        self.clock.cancel()

    def btn_skip(self, root):
        self.manager.current = "play"

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
        root.slide_game_timer.value = 0
        root.slide_move_timer.value = 0

    def start_game(self, *args):
        root = args[0]

        settings = {}
        settings["num players"] = 1
        settings["p1 color"] = root.ids.p1_color_white.state == "down"
        settings["p2 color"] = None
        settings["ai diff"] = int(root.ids.slide_ai_diff.value)
        settings["tutor on"] = root.ids.tutor_on.state == "down"
        settings["game timer"] = root.ids.slide_game_timer.value
        settings["move timer"] = root.ids.slide_move_timer.value
        
        global gameCtrl
        gameCtrl = Game(settings)
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
        
        global gameCtrl
        gameCtrl = Game(settings)
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
        sm.add_widget(PlayGameScreen(name="play"))

        return sm

ChessUIApp().run()
