import time

import Adafruit_CharLCD as LCD

import utils

from triforce_tools import TriforceUploader, IP_ADDRESSES


class State(object):
    def __init__(self, lcd):
        self.lcd = lcd

        self.lcd.clear()
        self.lcd.message("{}".format(self))

    def __str__(self):
        pass

    def on_button_press(self, button):
        pass


class GameSelect(State):
    def __init__(self, lcd, game_idx=0):
        """
        :param lcd: Handle to an LCD
        :param int game_idx: Optional param for idx at which to start game list

        TODO: Add dict formats
        :ivar list game_list: Full list of games with all details
        :ivar list games: List of game display names
        """
        super(GameSelect, self).__init__(lcd)
        self.game_list = utils.generate_game_list()
        self.game_names = sorted(self.game_list.keys())
        self.game_idx = game_idx

    def __str__(self):
        return "Game Select"

    def on_button_press(self, button):
        if button in (LCD.LEFT, LCD.RIGHT):
            pass

        if button == LCD.UP:
            new_idx = (self.game_idx - 1) % len(self.game_names)
            self.lcd.clear()
            self.lcd.message(utils.center_text(self.game_names[new_idx]))
            self.game_idx = new_idx

        if button == LCD.DOWN:
            new_idx = (self.game_idx + 1) % len(self.game_names)
            self.lcd.clear()
            self.lcd.message(utils.center_text(self.game_names[new_idx]))
            self.game_idx = new_idx

        if button == LCD.SELECT:
            return DIMMSelect(self.lcd, self.game_list[self.game_names[self.game_idx]])

        return self


class DIMMSelect(State):
    class __DIMMSelect:
        def __init__(self, lcd, selected_game):
            self.lcd = lcd
            self.targets = IP_ADDRESSES
            self.selected_game = selected_game
            self.cur_idx = 0

            # TODO: Consider state machine
            self.menu_flag = False

        def __str__(self):
            return repr(self) + self.cur_idx

    instance = None

    def __init__(self, lcd, selected_game):
        """
        :param lcd: An lcd handle. This is not generalized.
        :param dict selected_game: A dict describing the game to be loaded.
        """
        super(DIMMSelect, self).__init__(lcd)

        if not DIMMSelect.instance:
            DIMMSelect.instance = DIMMSelect.__DIMMSelect(lcd, selected_game)
        else:
            DIMMSelect.instance.lcd = lcd
            DIMMSelect.instance.selected_game = selected_game

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self):
        # TODO: Add in up/down arrows
        return "Choose target\ndevice: \x03/x04"

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
                # Might be nice to ping at start and issue warnings. Especially while I don't have
                # UI support for adding targets.
                try:
                    installer = TriforceUploader(self.targets[self.cur_idx], self.lcd)
                except RuntimeError:
                    self.lcd.clear()
                    # TODO: Colorize
                    self.lcd.message("Cannot connect!\nUse other DIMM")
                    return self

                installer.upload_game(utils.get_filepath_for_game(self.selected_game))
                return GameSelect(self.lcd)

        return self
