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
        for row in self.opponent_field:
            for ship in row:
                if (ship['ship_number'] != 0 and ship['is_life'] == True) > 0:
                    return False

class Human(Player):

    def __init__(self, name: str):
        super().__init__()
        self.name = "\033[32m{}".format(name)

    def place_ships(self):
        """Спрашиваем пользователя куда и ставим корабли"""

        print(self.name, "\033[0m{}".format('please put the ships on your field.'))
        ships = [[4, 1], [3, 2], [3, 3], [2, 4], [2, 5], [2, 6], [1, 7], [1, 8], [1, 9], [1, 10]]
        letters = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
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
        while not ShootResult.miss or self.is_killed_all():
            print('Select a coordinate for the shot')
            where_i_was_shooting = []
            letters = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
            shoot_coord = (int(letters[input('Write a letter from "A" to "J" = ').upper()]),
                           (int(input('Write a value from "1" to "10" = ')) - 1))
            if shoot_coord not in where_i_was_shooting:
                where_i_was_shooting.append(shoot_coord)
                if self.opponent_field.check_shoot(*shoot_coord):
                    break
                return shoot_coord
            else:
                print("It's been shot here before, select other coordinates.")



class Bot(Player):

    def __init__(self):
        super().__init__()
        random_names_for_bot = ['Bot_Galina', 'Bot_Sigizmund', 'Bot_Erjan']
        self.name = choice(random_names_for_bot)

    def place_ships(self):
        """Спрашиваем пользователя куда и ставим корабли"""

        ships = [[4, 1], [3, 2], [3, 3], [2, 4], [2, 5], [2, 6], [1, 7], [1, 8], [1, 9], [1, 10]]
        for ship in ships:
            while True:
                rand_row = randint(0, 9)
                rand_column = randint(0, 9)
                rand_dir = [Direction.horizontal, Direction.vertical]
                random_direction = choice(rand_dir)

                if self.own_field.set_ship(rand_row, rand_column, random_direction, ship[0], ship[1]):
                    break

