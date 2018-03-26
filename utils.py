import os

from functools import lru_cache

from games import GAME_TO_FILENAME_MAP


ROM_DIR = os.path.join('/', 'media', 'naomi')


@lru_cache()
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


def get_bg_colors(lcd):
    """Get current bg colors.

    Background color pins are active low.
    This won't work for screens that support pwm.
    """
    return (lcd._gpio.is_low(lcd._red), lcd._gpio.is_low(lcd._green), lcd._gpio.is_low(lcd._blue))



def get_gilepath_for_game(game_name):
    return os.path.join(ROM_DIR, GAME_TO_FILENAME_MAP[game_name])
