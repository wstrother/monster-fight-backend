
# This module hard codes some data / procedures for new character creation

DV_MAX = 5      # available stat points for new character creation

MOVE_POOLS = [
    ["RED", "YELLOW", "BLACK"],     # JOLLYGATOR
    ["BLUE", "PURPLE", "BLACK"],    # QUAILEAF
    ["GREEN", "BROWN", "BLACK"]     # BLAZEBRA
]


def get_move_list(move_cont, color_cont, colors, index):
    return [
        move_cont.get_move_by_color_index(
            color_cont.get_color_id(c), index
        ) for c in colors
    ]


def get_move_pool(move_cont, color_cont, species_id):
    colors = MOVE_POOLS[species_id - 1]
    first = get_move_list(move_cont, color_cont, colors, 0)
    second = get_move_list(move_cont, color_cont, colors, 1)

    return first, second
