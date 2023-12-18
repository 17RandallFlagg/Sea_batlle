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
        if not ((direction.horizontal and 10 <= row + ship_size - 1)
                or (direction.vertical and 10 <= column + ship_size - 1)):
            return False

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

            self.__field[r][c]['cell_type'] = ship_size
            self.__field[r][c]['ship_number'] = ship_number



        return True

    def __set_cell(self, row: int, column: int, value):
        """Меняем значение ячейки"""

    def __check_cell(self, row: int, column: int):
        """Можно ли туда ставить палубу корабля"""

    def check_shoot(self, row: int, column: int) -> ShootResult:
        """Проверяем результат выстрела"""