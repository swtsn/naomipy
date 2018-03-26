import time

import Adafruit_CharLCD as LCD

from states import GameSelect


class MainMenu:
    def __init__(self, display):
        self.state = GameSelect(display)

    def on_button_press(self, button):
        self.state = self.state.on_button_press(button)

        # Rate limit all button presses at 250ms
        time.sleep(0.25)
