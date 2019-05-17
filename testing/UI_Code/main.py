from game_ctrl import Game

from os import remove
from os import listdir
from os.path import isfile, join
from math import ceil
import datetime

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition 
#from kivy.cache import Cache
from kivy.uix.popup import Popup

"""
gameCtrl = Game() # give initail settings
gamectrl.make_start_LED_array(chess.PAWN) # tell the game to lisght up all pawn square
gameCtrl.chexk_start_up_state() # call after above function to make sure all pawns have beem placed. Will return true once condition is met. then move on to next piece. 
gameCtrl.refresh_board() returns board, time left for each player

"""
gameCtrl = None
screen_list = ['home']

class HelpIcon(Button):

    def open_help(self):
        pop = SimplePopup()
        pop.open()
        
class InfoIcon(Button):

    def toggle_info(self):
        global gameCtrl;
        gameCtrl.toggle_info()

class SimplePopup(Popup):
    
    def dismiss_pop(self):
        self.dismiss()
        pop = ColorPopup()
        pop.open()

class ColorPopup(Popup):
    pass

class EndgamePopup(Popup):
    pass

class ErrorPopup(Popup):
    
    def set_text(self, text):
        self.ids.warning_message.text = text

class SaveGameScreen(Screen):
    
    def on_enter(self):
        screen_list.append(self.name)
        root = self.ids
        now = datetime.datetime.now()
        root.textbox_filename.text = "{}".format(now.strftime("%Y-%m-%d %I:%M%p"))
        
    def save_game(self, filename):
        now = datetime.datetime.now()
        date = "{}".format(now.strftime("%Y-%m-%d"))
        global gameCtrl
        gameCtrl.save_game(filename, date)
        self.manager.current = "home"

class PlayGameScreen(Screen):

    def on_enter(self):
        self.clock = Clock.schedule_interval(self.clock_callback, 10 / 1000)

        if screen_list[-1] == "board_setup":
            pop = SimplePopup()
            pop.open()
        
        screen_list.append(self.name)

    def clock_callback(self, dt):
        global gameCtrl
        gameCtrl.live_move_highlight()
        gameCtrl.assign_highlight()

    def on_leave(self):
        self.clock.cancel()

    def end_turn(self):
        global gameCtrl
        turn, message = gameCtrl.end_turn_move()
        if turn == "illegal":
            pop = ErrorPopup()
            pop.open()
            pop.set_text(message)
        else:
            game_over = gameCtrl.check_end_game()
            self.ids.turn_label.text = "Turn: {}".format(turn)

            if game_over:
                #gameCtrl.clear_board_LED()
                self.manager.current = "home"
                pop = EndgamePopup()
                pop.open()

    
    def game_hint(self):
        global gameCtrl
        gameCtrl.hint()

class LoadGameScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)	

    def on_enter(self, *args):
        screen_list.append(self.name)
        self.ids.table.clear_widgets()

        saved_games = self.list_games()
        saved_games.sort()
        saved_games = saved_games[::-1]
        if len(saved_games) > 6:
            saved_games = saved_games[0:6]
        count = 0
        for game in saved_games:
            game_name = game[:-4]
            bttn2 = ToggleButton(size_hint_y=0.3, group="g", allow_no_selection=False)
            bttn2.text = str(game_name)
            bttn2.font_size = "25sp"
            if count == 0:
                bttn2.state = "down"
            self.ids.table.add_widget(bttn2)
            count = count + 1

        spaces = len(saved_games) % 2
        if spaces == 1:
            self.ids.table.add_widget(Label(text="", size_hint_y=0.2))

        y_spacing = 1 -  0.3*ceil(len(saved_games) / 2)
        for itr in range(0, 2):
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
            #remove("saves/{}.pgn".format(game_name)) #os.remove()
        

class SettingsScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)	

    def on_enter(self):
        screen_list.append(self.name)

    def switch(self, root):
        val = not root.ids.sw1.active
        root.ids.sw2.disabled = val
        root.ids.sw3.disabled = val
        root.ids.sw4.disabled = val
        root.ids.sw5.disabled = val

    def btn_back(self):
        self.manager.current = screen_list[-2]

    def btn_save(self):
        root = self.ids
        sw1_val = root.sw1.active # Tile highlighting
        sw2_val = root.sw2.active # legal moves
        sw3_val = root.sw3.active # illegal moves
        sw4_val = root.sw4.active # king check
        sw5_val = root.sw5.active # Last move

        global gameCtrl
        if sw1_val:
            gameCtrl.update_settings(sw1_val, sw2_val, sw3_val, sw4_val, sw5_val)
        else:
            gameCtrl.update_settings(False, False, False, False, False)
        self.btn_back()

class BoardSetupScreen(Screen):

    current_piece = 1

    def on_enter(self):
        screen_list.append(self.name)

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
                root.img_white.source = "img/knight_w.png"
                root.img_black.source = "img/knight_b.png"
                root.piece_name_label.text = "Knight"
            elif self.current_piece == 3:
                root.img_white.source = "img/bishop_w.png"
                root.img_black.source = "img/bishop_b.png"
                root.piece_name_label.text = "Bishop"
            elif self.current_piece == 4:
                root.img_white.source = "img/rook_w.png"
                root.img_black.source = "img/rook_b.png"
                root.piece_name_label.text = "Rook"
            elif self.current_piece == 5:
                root.img_white.source = "img/queen_w.png"
                root.img_black.source = "img/queen_b.png"
                root.piece_name_label.text = "Queen"
            elif self.current_piece == 6:
                root.img_white.source = "img/king_w.png"
                root.img_black.source = "img/king_b.png"
                root.piece_name_label.text = "King"

            if self.current_piece == 7:
                self.manager.current = "play"
            else:
                gameCtrl.make_start_LED_array(self.current_piece)

    def on_leave(self):
        self.clock.cancel()

class StartScreen_p1(Screen):

    handicap = [None, None]

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)	

    def on_enter(self, *args):
        screen_list.append(self.name)
        root = self.ids
        root.p1_color_white.state = "down"
        root.p1_color_black.state = "normal"
        root.slide_ai_diff.value = 3
        root.tutor_on.state = "down"
        #root.slide_game_timer.value = 0
        #root.slide_move_timer.value = 0

    def start_game(self, *args):
        root = args[0]

        settings = {}
        settings["num players"] = 1
        settings["p1 color"] = root.ids.p1_color_white.state == "down"
        settings["p2 color"] = not settings["p1 color"]
        settings["ai diff"] = int(root.ids.slide_ai_diff.value)
        settings["tutor on"] = root.ids.tutor_on.state == "down"
        #settings["game timer"] = root.ids.slide_game_timer.value
        #settings["move timer"] = root.ids.slide_move_timer.value

        global gameCtrl
        #if gameCtrl != None:
        #    del gameCtrl     
        gameCtrl = Game(settings)
        self.manager.current = "board_setup"

class StartScreen_p2(Screen):
    handicap = [None, None]

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)	

    def on_enter(self, *args):
        screen_list.append(self.name)
        root = self.ids
        root.p1_color_white.state = "down"
        root.p1_color_black.state = "normal"
        root.p2_color_white.state = "normal"
        root.p2_color_black.state = "down"
        root.tutor_on.state = "down"
        #root.slide_game_timer.value = 0
        #root.slide_move_timer.value = 0

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
        #settings["game timer"] = root.slide_game_timer.value
        #settings["move timer"] = root.slide_move_timer.value
        
        # trying to fix problem where new game is not created
        global gameCtrl
        #if gameCtrl != None:
        #    print("Game existed")
        #    gameCtrl.reset_board()
        #    del gameCtrl     
        gameCtrl = Game(settings)
        self.manager.current = "board_setup"


class HomeScreen(Screen):

    def on_enter(self):
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
