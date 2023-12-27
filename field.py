from enums import Direction, ShootResult


class Field:
    """Игровое поле для морского боя"""

    def __init__(self):
        """Создаем пустое поле 10х10"""
        self.__field: list[list[dict]] = []
        for row in range(10):
            self.__field.append([])
            for col in range(10):
                self.__field[row].append(
                    {
                        "cell_type": 0,
                        "ship_number": 0,
                        "is_live": True
                    }
                )

    def set_ship(self, row: int, column: int, direction: Direction, ship_size: int, ship_number: int) -> bool:
        """Устанавливаем корабль на поле"""

        for cell in range(ship_size):
            r = row + direction.value[0] * cell
            c = column + direction.value[1] * cell
            if not 0 <= r < 10 or not 0 <= c < 10:
                return False

            for row_1 in range(-1, 2):
                for column_1 in range(-1, 2):
                    row_new = r + row_1
                    column_new = c + column_1

                    if 0 <= row_new < 10 and 0 <= column_new < 10:
                        if self.__field[row_new][column_new]['ship_number'] != 0:
                            if self.__field[row_new][column_new]['ship_number'] != ship_number:
                                return False

        for cell in range(ship_size):
            r = row + direction.value[0] * cell
            c = column + direction.value[1] * cell
            self.__field[r][c]['cell_type'] = ship_size
            self.__field[r][c]['ship_number'] = ship_number
        return True

    def __set_cell(self, row: int, column: int, value):
        """Меняем значение ячейки"""

    def check_shoot(self, shoot_coord) -> ShootResult:
        """Проверяем результат выстрела"""
        self.__field[shoot_coord[0]][shoot_coord[1]]['is_live'] = False
        ship = self.__field[shoot_coord[0]][shoot_coord[1]]['ship_number']
        if self.__field[shoot_coord[0]][shoot_coord[1]]['ship_number'] != 0:
            deck_is_live = 0
            for check_row in self.__field:
                for check_column in check_row:
                    if check_column['ship_number'] == ship and check_column['is_live'] is True:
                        deck_is_live += 1
            if deck_is_live > 0:
                return ShootResult.hit

            else:
                return ShootResult.kill
        else:
            return ShootResult.miss

    def is_killed_all(self) -> bool:
        """Проверяем, что убиты все корабли"""
        is_live_deck = 0
        for row in self.__field:
            for ship in row:
                if ship['ship_number'] != 0 and ship['is_live'] is True:
                    is_live_deck += 1
        if is_live_deck > 0:
            return False
        else:
            return True
