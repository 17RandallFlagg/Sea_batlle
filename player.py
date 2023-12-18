from field import Field
from enums import Direction, ShootResult
from random import randint, choice


class Player:
    """Абстрактный игрок"""

    def __init__(self):
        self.own_field = Field()
        self.opponent_field = Field()

    def place_ships(self):
        """ Расставляем корабли на поле
            Пример абстрактного метода. Требует реализации в потомке
        """
        raise NotImplementedError

    def shoot(self) -> tuple[int, int]:
        """Производим выстрел. Возвращаем row и column"""
        raise NotImplementedError

    def check_shoot(self, row: int, column: int) -> ShootResult:
        """Проверяем ячейку в которую произвели выстрел"""
        return self.own_field.check_shoot(row, column)

    def is_killed_all(self) -> bool:
        """Проверяем, что убиты все корабли"""
        return False

class Human(Player):

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def place_ships(self):
        """Спрашиваем пользователя куда и ставим корабли"""

        ships = [[4, 1], [3, 2], [3, 3], [2, 4], [2, 5], [2, 6], [1, 7], [1, 8], [1, 9], [1, 10]]
        letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10}
        for ship in ships:
            while True:
                print(f'Set up {ship[0]}-deck ship number {ship[1]}')
                coordinate_row = letters[input('Write a letter from "A" to "J" = ').upper()]
                coordinates_col = int(input('Write a value from "1" to "10" = ')) - 1
                direction = input('Write direction: "hor" or "ver" = ')
                if direction == 'hor':
                    direction = Direction.horizontal
                if direction == 'ver':
                    direction = Direction.vertical

                if self.own_field.set_ship(coordinate_row, coordinates_col, direction, ship[0], ship[1]):
                    break
                else:
                    print("Can't post here, choose another coordinate.")

    def shoot(self) -> tuple[int, int]:
        """Спрашиваем у игрока куда стрелять"""


class Bot(Player):

    def place_ships(self):
        """Рандомно расставляем корабли"""
        self.own_field.set_ship(1, 2, Direction.vertical)

    def shoot(self) -> tuple[int, int]:
        """Решаем куда выстрелить"""
