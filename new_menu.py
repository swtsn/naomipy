import time

import Adafruit_CharLCD as LCD

from states import GameSelect


class MainMenu:
    def __init__(self, display):
        self.state = GameSelect(display, None)

    def on_button_press(self, button):
        self.state = self.state.on_button_press(button)

        # Rate limit all button presses at 250ms
        time.sleep(0.25)


class MenuContext:
    def __init__(self, display, idx, cur_btn):
        self.display = display
        self.idk = idx
        self.cur_btn = cur_btn
