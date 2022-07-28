import random

from kivy.config import Config

Config.set("graphics", "width", "700")
Config.set("graphics", "height", "950")

from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.metrics import dp


class FirstWindow(MDScreen):
    pass


class SecondWindow(MDScreen):
    counter = 1

    def on_enter(self, *args):
        Clock.schedule_interval(self.btn_create, 0.27)

    def btn_create(self, time):
        if self.counter < 10:
            btn = Button(on_press=lambda x: self.mark_me(x), font_size=dp(120), on_release=lambda x: self.check())
            btn.opacity = 0  # Set the opacity of the button to 0
            self.manager.ids[f'btn{self.counter}'] = btn
            self.manager.ids.grid.add_widget(btn)  # Add the button
            Animation(opacity=1, duration=.2).start(btn)  # Duration is < than clock duration
            self.counter += 1

    def check(self):
        if self.manager.check_if_winner():
            Factory.GamePopup().open()
            return
        self.manager.check_if_tie()

    def mark_me(self, widget):
        self.manager.sign = 'x' if self.manager.sign == 'o' else 'o'
        widget.text = self.manager.sign
        widget.disabled = True
        widget.disabled_color = (0, 0, 0, .65)


class WindowManager(ScreenManager):
    first_player = StringProperty("")
    second_player = StringProperty("")
    first_player_score = NumericProperty(0)
    second_player_score = NumericProperty(0)
    x_player = StringProperty("")
    o_player = StringProperty("")
    player_winner = StringProperty("")
    sign = StringProperty('o')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound_manager = SoundLoader()
        self.load_sound('sounds/enter_game.wav')

    def load_sound(self, song):
        sound = self.sound_manager.load(song)
        sound.play()
        sound.volume = 0.55

    def start(self):
        self.load_sound('sounds/enter_game.wav')

    def toss_me(self):
        self.first_player = self.ids["player1"].text
        self.second_player = self.ids["player2"].text
        winner = random.choice([self.first_player, self.second_player])
        self.x_player = winner
        if self.x_player == self.first_player:
            self.o_player = self.second_player
        else:
            self.o_player = self.first_player
        self.start()
        return winner

    def animate_it(self, widget, *args):
        animate = Animation(color=(0, 0, 1, 0), pos=(.1, .1), duration=.5)
        animate.start(widget)
        self.load_sound('sounds/Alien-takeoff.wav')

    def animate_me(self, widget, *args):
        animate = Animation(opacity=0, duration=.5)
        animate += Animation(size_hint=(.01, .01))
        animate.start(widget)
        self.load_sound('sounds/Alien-takeoff.wav')

    @staticmethod
    def check_values(*args):
        control_value = args[0]
        if all(arg == control_value for arg in args):
            return control_value

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
                return True
        return False

    def check_if_tie(self):
        buttons = [widget for widget in self.ids.keys() if widget.startswith('btn')]
        disabled = [1 if self.ids[btn].disabled else 0 for btn in buttons]
        if all(disabled) and not self.check_if_winner():
            self.load_sound('sounds/tie.wav')
            Factory.TiePopup().open()

    def reset_all(self):
        for name, widget in self.ids.items():
            if name.startswith('btn'):
                widget.disabled = False
                widget.text = ''
        self.ids["label1"].text = f"{self.x_player} is X and plays first"
        self.sign = 'o'
        if self.x_player == self.first_player:
            self.x_player = self.second_player
            self.o_player = self.first_player
            return
        self.o_player = self.second_player
        self.x_player = self.first_player

    def reset_score_players(self):
        self.first_player_score = 0
        self.first_player = ""
        self.second_player_score = 0
        self.second_player = ""


class TicTacToe(MDApp):
    def __init__(self, **kwargs):
        super(TicTacToe, self).__init__(**kwargs)
        self.theme_cls.primary_palette = 'Orange'


x = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen',
     'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
if __name__ == "__main__":
    TicTacToe().run()
