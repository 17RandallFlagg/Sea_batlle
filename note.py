def check_direction(x: int, y: int, x_step: int, y_step: int, ship_length: int) -> str:
    """
    Checks the availability of placing a ship in a specific direction.

    :param x: The starting x-coordinate.
    :param y: The starting y-coordinate.
    :param x_step: The step size for movement in the x-direction.
    :param y_step: The step size for movement in the y-direction.
    :param ship_length: The length of the ship to be placed.
    :return: str - A string indicating whether the ship can be placed ('can_be_placed')
           or not ('can_not_be_placed') in the specified direction.
    """
    for step in range(ship_length):
        # Calculate the coordinates for the current step
        cur_x = x + step * x_step
        cur_y = y + step * y_step

        # Check if the current position is within the bounds of the game board
        if not (0 <= cur_x < field_size and 0 <= cur_y < field_size):
            return 'can_not_be_placed'

        # Check the current position and its surrounding cells for the presence of a ship
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_x = cur_x + i
                new_y = cur_y + j
                # Exclude the current position from blocking placement, allow only adjacent cells within the field
                if ((0 <= new_x < field_size and 0 <= new_y < field_size) and battle_board[new_x][new_y] != 0
                        and (new_x != cur_x or new_y != cur_y)):
                    return 'can_not_be_placed'

    return 'can_be_placed'


def validate_ship_position(x: int, y: int, ship_length: int) -> tuple[str, ...]:
    """
    Validates the position for placing a ship in all four directions.

    :param x: The x-coordinate for the starting position.
    :param y: The y-coordinate for the starting position.
    :param ship_length: The length of the ship to be placed.
    :return: tuple[str, ...] - A tuple containing the results of the ship placement validation
                       in four directions: 'north', 'south', 'west', 'east'.
    """
    directions = {
        'north': check_direction(x, y, -1, 0, ship_length),
        'south': check_direction(x, y, 1, 0, ship_length),
        'west': check_direction(x, y, 0, -1, ship_length),
        'east': check_direction(x, y, 0, 1, ship_length)
    }

    return tuple(directions.values())


def place_ship(input_direction: str, x: int, y: int, ship_length) -> None:
    """
    Places a ship on the game board.

    :param input_direction: The direction of the ship ('N', 'S', 'W', 'E', or their full names).
    :param x: The X-coordinate on the game board.
    :param y: The Y-coordinate on the game board.
    :param ship_length: The length of the ship.
    :return: None
    """

    if input_direction == 'N' or input_direction == 'NORTH':
        for i in range(ship_length):
            battle_board[x - i][y] = ship_length * 10 + ship_length
    if input_direction == 'S' or input_direction == 'SOUTH':
        for i in range(ship_length):
            battle_board[x + i][y] = ship_length * 10 + ship_length
    if input_direction == 'W' or input_direction == 'WEST':
        for i in range(ship_length):
            battle_board[x][y - i] = ship_length * 10 + ship_length
    if input_direction == 'E' or input_direction == 'EAST':
        for i in range(ship_length):
            battle_board[x][y + i] = ship_length * 10 + ship_length

    print(f'По указанному направлению, успешно размещен {battle_ships_names[ship_length][0]} корабль.')
    display_game_board()