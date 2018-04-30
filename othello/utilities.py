def is_valid_move(move, board_state, color_number):
    if move == None:
        return False
    if not is_empty_position(board_state, move):
        # Stone is already placed
        return False
    if can_take_stones_vertically_up(move, board_state, color_number):
        return True
    if can_take_stones_vertically_down(move, board_state, color_number):
        return True
    if can_take_stones_horizontally_left(move, board_state, color_number):
        return True
    if can_take_stones_horizontally_right(move, board_state, color_number):
        return True
    if can_take_stones_diagonally_up_left(move, board_state, color_number):
        return True
    if can_take_stones_diagonally_up_right(move, board_state, color_number):
        return True
    if can_take_stones_diagonally_down_left(move, board_state, color_number):
        return True
    if can_take_stones_diagonally_down_right(move, board_state, color_number):
        return True
    return False


def can_take_stones_vertically_up(move, board_state, color_number):
    def accumulator(x, y, step):
        return (x, y + step)
    return can_take_stone_in_accumulator_direction(move, board_state, color_number, accumulator)


def can_take_stones_vertically_down(move, board_state, color_number):
    def accumulator(x, y, step):
        return (x, y - step)
    return can_take_stone_in_accumulator_direction(move, board_state, color_number, accumulator)


def can_take_stones_horizontally_left(move, board_state, color_number):
    def accumulator(x, y, step):
        return (x - step, y)
    return can_take_stone_in_accumulator_direction(move, board_state, color_number, accumulator)


def can_take_stones_horizontally_right(move, board_state, color_number):
    def accumulator(x, y, step):
        return (x + step, y)
    return can_take_stone_in_accumulator_direction(move, board_state, color_number, accumulator)


def can_take_stones_diagonally_up_left(move, board_state, color_number):
    def accumulator(x, y, step):
        return (x - step, y + step)
    return can_take_stone_in_accumulator_direction(move, board_state, color_number, accumulator)


def can_take_stones_diagonally_up_right(move, board_state, color_number):
    def accumulator(x, y, step):
        return (x + step, y + step)
    return can_take_stone_in_accumulator_direction(move, board_state, color_number, accumulator)


def can_take_stones_diagonally_down_left(move, board_state, color_number):
    def accumulator(x, y, step):
        return (x - step, y - step)
    return can_take_stone_in_accumulator_direction(move, board_state, color_number, accumulator)


def can_take_stones_diagonally_down_right(move, board_state, color_number):
    def accumulator(x, y, step):
        return (x + step, y - step)
    return can_take_stone_in_accumulator_direction(move, board_state, color_number, accumulator)


def can_take_stone_in_accumulator_direction(move, board_state, color_number, accumulator):
    (x, y) = move
    (rows, columns) = board_state.shape
    for i in range(1, max(rows, columns), 1):
        position = accumulator(x, y, i)
        if is_out_of_board(board_state, position) or is_empty_position(board_state, position):
            break
        if (board_state[position] == color_number):
            if i != 1:
                return True
            else:
                return False
    return False


def has_valid_move(board_state, color_number):
    return len(list_all_valid_moves(board_state, color_number)) != 0

def color_string_to_number(color_string):
    return (-1 if (color_string == 'black') else 1)


def is_out_of_board(board_state, position):
    (x, y) = position
    (rows, columns) = board_state.shape
    return (x < 0 or y < 0 or rows <= x or columns <= y)


def is_empty_position(board_state, position):
    return board_state[position] == 0


def list_all_valid_moves(board_state, color_number):
    empty_positions = list_all_empty_positions(board_state)
    valid_moves = []
    for move in empty_positions:
        if is_valid_move(move, board_state, color_number):
            valid_moves.append(move)
    return valid_moves


def list_all_empty_positions(board_state):
    positions = []
    (rows, columns) = board_state.shape
    for x in range(rows):
        for y in range(columns):
            position = (x, y)
            if is_empty_position(board_state, position):
                positions.append(position)
    return positions
