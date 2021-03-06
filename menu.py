import os
import signal
import sys
import time

import Adafruit_CharLCD as LCD

from states import GameSelect


SUCCESS_CHAR_CODE = [0, 1, 3, 22, 28, 8, 0, 0]
FAILURE_CHAR_CODE = [0, 27, 14, 4, 14, 27, 0, 0]


class MainMenu:
    def __init__(self, display):
        self.state = GameSelect(display)

    def on_button_press(self, button):
        self.state = self.state.on_button_press(button)

        # Rate limit all button presses at 250ms
        time.sleep(0.25)


def handle_sigterm(signum=None, frame=None):
    """Handle sigterm

    Graciously shutdown when we receive a SIGTERM.

    * Turn off display
    * Turn off backlight
    * Exit script
    """
    lcd = LCD.Adafruit_CharLCDPlate()
    lcd.clear()
    lcd.enable_display(False)
    lcd.set_backlight(False)
    sys.exit(0)
signal.signal(signal.SIGTERM, handle_sigterm)


def main():
    lcd = LCD.Adafruit_CharLCDPlate()
    lcd.set_color(1.0, 0.0, 1.0)

    # Create check mark at \x01
    lcd.create_char(1, SUCCESS_CHAR_CODE)

    # Create X mark at \x02
    lcd.create_char(2, FAILURE_CHAR_CODE)

    menu = MainMenu(lcd)

    pressed_button = None

    while True:
        for button in (LCD.UP, LCD.DOWN, LCD.LEFT, LCD.RIGHT, LCD.SELECT):
            if lcd.is_pressed(button):
                if pressed_button == button:
                    pass

                menu.on_button_press(button)
                pressed_button = button

            pressed_button = None


main()
