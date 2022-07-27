import random

from kivy.config import Config

Config.set("graphics", "width", "700")
Config.set("graphics", "height", "950")

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.core.audio import SoundLoader


class FirstWindow(Screen):
    pass


class SecondWindow(Screen):
    pass


class WindowManager(ScreenManager):
    first_player = StringProperty("")
    second_player = StringProperty("")
    first_player_score = NumericProperty(0)
    second_player_score = NumericProperty(0)
    x_player = StringProperty("")
    o_player = StringProperty("")
    sign = StringProperty("o")
    player_winner = StringProperty("")
    sound_manager = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound_manager = SoundLoader()
        self.load_sound('sounds/enter_game.wav')

    def load_sound(self, song):
        sound = self.sound_manager.load(song)
        sound.play()
        sound.volume = 0.55

    def start(self):
        self.load_sound('sounds/returner.wav')

    def toss_me(self):
        self.first_player = self.ids["player1"].text
        self.second_player = self.ids["player2"].text
        my_list = [self.first_player, self.second_player]
        winner = random.choice(my_list)
        self.x_player = str(winner)
        if self.x_player == self.first_player:
            self.o_player = str(self.second_player)
        else:
            self.o_player = str(self.first_player)

        self.start()
        return winner

    def animate_it(self, widget, *args):
        animate = Animation(color=(0, 0, 1, 0),
                            pos=(.1, .1), duration=1)
        animate.start(widget)
        self.load_sound('sounds/Alien-takeoff.wav')

    def animate_me(self, widget, *args):
        animate = Animation(opacity=0, duration=1)
        animate += Animation(size_hint=(.01, .01))
        animate.start(widget)
        self.load_sound('sounds/Alien-takeoff.wav')

    def mark_me(self):
        self.sign = "o" if self.sign == 'x' else 'x'
        return self.sign

    @staticmethod
    def check_values(*args):
        control_value = args[0]
        if all(arg == control_value for arg in args):
            return control_value
        return False

    def check_if_winner(self):
        combinations = [('btn1', 'btn2', 'btn3'), ('btn4', 'btn5', 'btn6'), ('btn7', 'btn8', 'btn9'),
                        ('btn1', 'btn4', 'btn7'), ('btn2', 'btn5', 'btn8'), ('btn3', 'btn6', 'btn9'),
                        ('btn1', 'btn5', 'btn9'), ('btn3', 'btn5', 'btn7')]
        for comb in combinations:
            field_one = self.ids[comb[0]].text
            field_two = self.ids[comb[1]].text
            field_three = self.ids[comb[2]].text
            if all([field_one, field_two, field_three]) and self.check_values(field_one, field_two, field_three):
                winner = self.ids[comb[0]].text
                self.player_winner = eval(f'self.{winner}_player')
                if eval(f'self.{winner}_player') == self.first_player:
                    self.first_player_score += 1
                else:
                    self.second_player_score += 1
                self.update_score()
                return True
        return False

    def check_if_tie(self):
        buttons = [widget for widget in self.ids.keys() if widget.startswith('btn')]
        disabled = sum(1 for btn in buttons if self.ids[btn].disabled)
        if disabled == 9 and not self.check_if_winner():
            self.load_sound('sounds/tie.wav')
            Factory.TiePopup().open()

    def reset_all(self):
        self.sign = "o"
        if self.x_player == self.first_player:
            self.x_player = self.second_player
            self.o_player = self.first_player
        else:
            self.o_player = self.second_player
            self.x_player = self.first_player
        for name, widget in self.ids.items():
            if name.startswith('btn'):
                widget.disabled = False
                widget.text = ''
        self.ids["label1"].text = f"{self.x_player} is X and plays first"

    def reset_score_players(self):
        self.first_player_score = 0
        self.first_player = ""
        self.second_player_score = 0
        self.second_player = ""

    def update_score(self):
        self.ids["score1"].text = str(self.first_player_score)
        self.ids["score2"].text = str(self.second_player_score)
        self.ids["score1"].disabled = True
        self.ids["score2"].disabled = True
        self.load_sound('sounds/start.wav')


class TicTacToe(MDApp):
    def __init__(self, **kwargs):
        super(TicTacToe, self).__init__(**kwargs)
        self.theme_cls.primary_palette = 'Teal'


if __name__ == "__main__":
    TicTacToe().run()
