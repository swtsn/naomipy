import bisect
import os

from games import GAME_TO_FILENAME_MAP


ROM_DIR = os.path.join('/', 'media', 'naomi')


def center_text(test_str):
    display_length = 16

    # Display length of 16, arrows on each end
    display_space = display_length - 2

    # Leave room for spaces so it doesn't look weird
    padded_space = display_space - 2

    tokens = test_str.split()
    lengths = _calculate_lengths(tokens)

    # By default we want to divide on our optimal length
    group_idx = bisect.bisect_right(lengths, padded_space)
    top_line_tokens = tokens[:group_idx]
    # TODO: Recompute lengths for bottom line
    bottom_line_tokens = tokens[group_idx:]

    # Check if the first token was not ideal
    if not len(top_line_tokens):
        group_idx = bisect.bisect_right(lengths, display_space)

        top_line_tokens = tokens[:group_idx]
        bottom_line_tokens = tokens[group_idx:]

        if not top_line_tokens:
            raise RuntimeError("Category {} too long to fit on display".format(tokens[0]))

    top_line = " ".join(top_line_tokens)
    bottom_line = " ".join(bottom_line_tokens)

    # Recombine string with spaces and left justify each line where necessary
    top_line_space = display_space - len(top_line)
    top_line_pad_left = top_line_space / 2
    top_line_pad_right = top_line_pad_left + (top_line_space % 2)

    # For the bottom line we use the entire display length because we aren't going to display arrows
    bottom_line_space = display_length - len(bottom_line)
    bottom_line_pad_left = bottom_line_space / 2
    bottom_line_pad_right = bottom_line_pad_left + (bottom_line_space % 2)

    return "<{}{}{}>|\n|{}{}{}".format(
        ' '*top_line_pad_left,
        top_line,
        ' '*top_line_pad_right,
        ' '*bottom_line_pad_left,
        bottom_line,
        ' '*bottom_line_pad_right
    )


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



def get_filepath_for_game(game_name):
    return os.path.join(ROM_DIR, GAME_TO_FILENAME_MAP[game_name])
