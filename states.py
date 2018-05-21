from utils import generate_game_list

import Adafruit_CharLCD as LCD

from triforce_tools import TriforceUploader


def _display_success(lcd):
    lcd.set_color(0.0, 1.0, 0.0)
    lcd.clear()
    lcd.message("Success! \x01")
    time.sleep(2)
    lcd.clear()
    lcd.message("Success! \x01\nPress Select")

    # Wait until user presses SELECT
    while True:
        if lcd.is_pressed(LCD.SELECT):
            return


class State:
    def __init__(self, lcd):
        self.lcd = lcd

        self.lcd.clear()
        self.lcd.message("{}".format(self))

    def __str__(self):
        pass

    def on_button_press(self, button):
        pass


class GameSelect(State):
    def __init__(self, lcd, installer=None):
        super().__init__(lcd)
        self.games = sorted(generate_game_list().keys())
        self.cur_idx = 0

        self.installer = installer

        # TODO: Consider state machine
        self.menu_flag = False

    def __str__(self):
        return "Game Select"

    def on_button_press(self, button):
        if button in (LCD.LEFT, LCD.RIGHT):
            return DIMMSelect(self.lcd)

        if not self.menu_flag:
            if button == LCD.SELECT:
                self.menu_flag = True
                self.lcd.clear()
                self.lcd.message(self.games[self.cur_idx])

        else:
            if button == LCD.UP:
                new_idx = (self.cur_idx - 1) % len(self.games)
                self.lcd.clear()
                self.lcd.message(self.games[new_idx])
                self.cur_idx = new_idx

            if button == LCD.DOWN:
                new_idx = (self.cur_idx + 1) % len(self.games)
                self.lcd.clear()
                self.lcd.message(self.games[new_idx])
                self.cur_idx = new_idx

            if button == LCD.SELECT:
                self.lcd.clear()
                self.lcd.message("Loading game...")
                # Do JIT check of installer
                self.installer.upload_game(get_filepath_for_game(self.games[self.cur_idx]))
                current_bg = get_bg_colors(self.lcd)
                _display_success(self.lcd)
                self.lcd.set_color(*current_bg)
                self.lcd.clear()
                self.lcd.message(self.games[self.cur_idx])


        return self


class DIMMSelect(State):
    # On first create, ping the DIMM
    def __DIMMSelect:
        def __init__(self, lcd):
            super().__init__(lcd)
            self.lcd = lcd
            self.targets = IP_ADDRESSES
            self.cur_idx = 0

            # TODO: Consider state machine
            self.menu_flag = False

        def __str__(self):
            return repr(self) + self.cur_idx

    instance = None

    def __init__(self, lcd):
        if not DIMMSelect.instance:
            DIMMSelect.instance = __DIMMSelect(lcd)
        else:
            DIMMSelect.instance.lcd = lcd

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self):
        return "DIMM Select"

    def on_button_press(self, button):
        if button in (LCD.LEFT, LCD.RIGHT):
            # There's a workflow bug here:
            # t0 - Set idx 1
            # t1 - Go to game
            # t2 - Come back to DIMMSelect
            # t3 - Go to gameselect
            # t4 - idx resets to 0
            return GameSelect(self.lcd)

        if not self.menu_flag:
            if button == LCD.SELECT:
                self.menu_flag = True
                self.lcd.clear()
                self.lcd.message(self.targets[self.cur_idx])

        else:
            if button == LCD.UP:
                new_idx = (self.cur_idx - 1) % len(self.targets)
                self.lcd.clear()
                self.lcd.message(self.targets[new_idx])
                self.cur_idx = new_idx

            if button == LCD.DOWN:
                new_idx = (self.cur_idx + 1) % len(self.targets)
                self.lcd.clear()
                self.lcd.message(self.targets[new_idx])
                self.cur_idx = new_idx

            if button == LCD.SELECT:
                # Ping installer here but later consider moving. This will help with JIT pinging.
                installer = TriforceUploader(self.targets[self.cur_idx], lcd)
                return GameSelect(self.lcd, installer)

        return self
