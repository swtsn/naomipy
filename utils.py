import bisect
import os

import yaml


ROM_DIR = os.path.join(os.path.expanduser('~'), 'ROMs')


def center_text(display_string, extra_padding=0):
    """
    TODO: Parameterize extra padding so that this can generically work
    for games and for subjects.
    """
    display_length = 16
    # This assumes padding is on top line only
    top_usable_area = display_length - extra_padding

    tokens = display_string.split()
    lengths = _calculate_lengths(tokens)

    # By default we want to divide on our optimal length
    group_idx = bisect.bisect_right(lengths, top_usable_area)
    top_line_tokens = tokens[:group_idx]
    # TODO: Recompute lengths for bottom line
    bottom_line_tokens = tokens[group_idx:]

    # Check if the first token was not ideal
    if extra_padding and not len(top_line_tokens):
        group_idx = bisect.bisect_right(lengths, display_length)

        top_line_tokens = tokens[:group_idx]
        bottom_line_tokens = tokens[group_idx:]

        if not top_line_tokens:
            raise RuntimeError("Name {} too long to fit on display".format(tokens[0]))

    top_line = " ".join(top_line_tokens)
    bottom_line = " ".join(bottom_line_tokens)

    if len(bottom_line) > display_length:
        raise RuntimeError("Bottom line too long: {}, {}".format(top_line, bottom_line))

    # Recombine string with spaces and left justify each line where necessary
    top_line_padding = display_length - len(top_line)
    top_line_pad_left = top_line_padding / 2
    top_line_pad_right = top_line_pad_left + (top_line_padding % 2)

    # For the bottom line we use the entire display length because we aren't going to display arrows
    bottom_line_padding = display_length - len(bottom_line)
    bottom_line_pad_left = bottom_line_padding / 2
    bottom_line_pad_right = bottom_line_pad_left + (bottom_line_padding % 2)

    top_display = "{}{}{}".format(
        ' '*top_line_pad_left,
        top_line,
        ' '*top_line_pad_right
    )

    if not bottom_line:
        return top_display

    bottom_display = "{}{}{}".format(
        ' '*bottom_line_pad_left,
        bottom_line,
        ' '*bottom_line_pad_right
    )

    return "{}\n{}".format(top_display, bottom_display)


def _calculate_lengths(tokens):
    lengths = []
    for i in xrange(len(tokens)):
        cur_length = len(tokens[i])

        if i != 0:
            # Cumulatively add lengths, add 1 to account for displaying a space between tokens
            cur_length += lengths[i - 1] + 1

        lengths.append(cur_length)

    return lengths


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
    path_to_game_list = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'game_list.yaml')
    game_to_filename_map = {}

    game_list = yaml.load(file(path_to_game_list, 'r'))

    for game in game_list:
        if os.path.isfile(os.path.join(ROM_DIR, game['filename'])):
            game_to_filename_map[game['display_name']] = game

    return game_to_filename_map


def get_bg_colors(lcd):
    """Get current bg colors.

    Background color pins are active low.
    This won't work for screens that support pwm.
    """
    return (lcd._gpio.is_low(lcd._red), lcd._gpio.is_low(lcd._green), lcd._gpio.is_low(lcd._blue))



def get_filepath_for_game(game):
    return os.path.join(ROM_DIR, game['filename'])
