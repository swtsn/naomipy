import os
import time

import Adafruit_CharLCD as LCD

from games import GAME_TO_FILENAME_MAP
from triforce_tools import TriforceUploader

IP_ADDRESS = "192.168.88.90"
ROM_DIR = os.path.join('/', 'media', 'naomi')


def generate_game_list():
    """Generates dict of available games on the system

    Will look in ROM_DIR for all games whose filename matches a value in
    GAME_TO_FILENAME_MAP. Returns dictionary containing only available games.

    TODO: Some sort of error reporting if games exist in ROM_DIR without a
    display name.

    :returns: Mapping of display name to filename for available games
    :rtype: dict
    :raises: RuntimeError if directory has no games
    """
    games = {}

    for display_name in GAME_TO_FILENAME_MAP:
        filename = GAME_TO_FILENAME_MAP[display_name]
        if os.path.isfile(os.path.join(ROM_DIR, filename)):
            games[display_name] = filename

    return games


def debug_display(games, cur_idx, new_idx, button):
    print(f"Pressed {button}. Current: {cur_idx}, New: {new_idx}.")


def main():
    lcd = LCD.Adafruit_CharLCDPlate()
    lcd.set_color(1.0, 0.0, 1.0)
    # First pass, no menu
    # main_menu = ["Select Game", "Test NetDIMM"]
    
    games = generate_game_list()
    game_display = sorted(games.keys())
    
    pressed_button = None
    cur_idx = 0
    
    lcd.clear()
    lcd.message(game_display[cur_idx])

    uploader = TriforceUploader(IP_ADDRESS, lcd)
    
    while True:
        if lcd.is_pressed(LCD.DOWN):
            if pressed_button == LCD.DOWN:
                pass
    
            new_idx = (cur_idx + 1) % len(game_display)
            lcd.clear()
            lcd.message(game_display[new_idx])
    
            cur_idx = new_idx
            pressed_button = LCD.DOWN
            time.sleep(0.5)
    
        if lcd.is_pressed(LCD.UP):
            if pressed_button == LCD.UP:
                pass
    
            new_idx = (cur_idx - 1) % len(game_display)
            lcd.clear()
            lcd.message(game_display[new_idx])
    
            cur_idx = new_idx
            pressed_button = LCD.UP
            time.sleep(0.5)

        if lcd.is_pressed(LCD.SELECT):
            lcd.clear()
            lcd.message("Loading game")

            filename = games[game_display[cur_idx]]
            uploader.upload_game(os.path.join(ROM_DIR, filename))

            lcd.clear()
            lcd.message("Game uploaded")
            time.sleep(80)

            lcd.clear()
            lcd.message(game_display[cur_idx])

            pressed_button = LCD.SELECT

        pressed_button = None


main()
