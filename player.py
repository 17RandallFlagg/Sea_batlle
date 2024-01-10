from field import Field
from enums import Direction, ShootResult
from random import randint, choice


class Player:
    """Абстрактный игрок"""

    def __init__(self):
        self.own_field = Field()
        self.opponent_field = Field()
        self.where_i_was_shooting = []
        self.bot_hit_a_ship = []
        self.not_kill_nowhere_shoot = True

    def place_ships(self):
        """ Расставляем корабли на поле
            Пример абстрактного метода. Требует реализации в потомке
        """
        raise NotImplementedError

    def shoot(self):
        """Производим выстрел. Возвращаем row и column"""
        raise NotImplementedError

    def check_is_not_shoot_early(self, shoot_coord) -> bool:
        """Проверяем ячейку в которую произвели выстрел"""
        if shoot_coord not in self.where_i_was_shooting:
            self.where_i_was_shooting.append(shoot_coord)
            return True
        else:
            return False

    def random_coordinate(self):
        """Рандомизируем координату выстрела для бота"""
        rand_r = randint(0, 9)
        rand_c = randint(0, 9)
        shoot_coord = (rand_r, rand_c)
        while True:
            if shoot_coord in self.where_i_was_shooting:
                rand_row = randint(0, 9)
                rand_column = randint(0, 9)
                shoot_coord = (rand_row, rand_column)
            return shoot_coord


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

    def shoot(self):
        """Спрашиваем у игрока куда стрелять"""

        while not self.opponent_field.is_killed_all():
            print(self.name, "\033[0m{}".format('Select a coordinate for the shot'))
            letters = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
            shoot_coord = (int(letters[input('Write a letter from "A" to "J" = ').upper()]),
                           int(input('Write a value from "1" to "10" = ')) - 1)

            if self.check_is_not_shoot_early(shoot_coord) is True:
                shoot_result = self.opponent_field.check_shoot(shoot_coord)
                if shoot_result == ShootResult.hit:
                    print("\033[31m{}".format('Hit! Get another shot.'))
                    return ShootResult.hit
                if shoot_result == ShootResult.kill:
                    return ShootResult.kill
                if shoot_result == ShootResult.miss:
                    print("\033[36m{}".format("You are miss!"))
                    return ShootResult.miss
            else:
                print("\033[34m{}".format("It's been shot here before, select other coordinates."))
                break


class Bot(Player):

    def __init__(self):
        super().__init__()
        random_names_for_bot = ['Bot_Galina', 'Bot_Sigizmund', 'Bot_Erjan', 'Bot_Edelstan', 'Bot_Ragnar', 'Bot_Waider',
                                'Bot_DeathGun', 'Bot_Freeman', 'Bot_LoveYourMom']
        self.name = "\033[32m{}".format(choice(random_names_for_bot))

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

    def shoot(self):
        """Спрашиваем у игрока куда стрелять"""
        letters = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}
        print(self.name, "\033[0m{}".format('select a coordinate for the shot'))
        self.not_kill_nowhere_shoot = True
        if len(self.bot_hit_a_ship) == 0:
            # Если ранее бот не попал в корабль:
            shoot_coord = self.random_coordinate()
            shoot_result = self.opponent_field.check_shoot(shoot_coord)
            print((letters[shoot_coord[0]]), shoot_coord[1] + 1)
            if shoot_result == ShootResult.hit:
                print("\033[31m{}".format('Hit! Get another shot.'))
                self.where_i_was_shooting.append(shoot_coord)
                for x in range(-1, 2, 2):
                    for y in range(-1, 2, 2):
                        if (0 <= shoot_coord[0] + x < 10 and 0 <= shoot_coord[1] + y < 10
                                and shoot_coord not in self.where_i_was_shooting):
                            rand_row_not_ship = shoot_coord[0] + x
                            rand_column_not_ship = shoot_coord[1] + y
                            not_ship = (rand_row_not_ship, rand_column_not_ship)
                            if not_ship not in self.where_i_was_shooting:
                                self.where_i_was_shooting.append(not_ship)
                self.bot_hit_a_ship.append(shoot_coord)
                return ShootResult.hit
            if shoot_result == ShootResult.miss:
                print("\033[36m{}".format("Bot is miss!"))
                self.where_i_was_shooting.append(shoot_coord)
                return ShootResult.miss
            if shoot_result == ShootResult.kill:
                print("\033[31m{}".format('The ship is destroyed!'))
                self.where_i_was_shooting.append(shoot_coord)
                return ShootResult.kill
        else:
            # Если ранее бот попал в корабль, но не убил:
            rand_row = 0
            rand_column = 0
            if len(self.bot_hit_a_ship) >= 1:
                rand_row = self.bot_hit_a_ship[-1][0]
                rand_column = self.bot_hit_a_ship[-1][1]
            cell_around = ((rand_row, rand_column - 1), (rand_row, rand_column + 1),
                           (rand_row - 1, rand_column), (rand_row + 1, rand_column))
            for cell in cell_around:
                if 0 <= cell[0] < 10 and 0 <= cell[1] < 10 and cell not in self.where_i_was_shooting:
                    shoot_result = self.opponent_field.check_shoot(cell)
                    print((letters[cell[0]]), cell[1] + 1)
                    if shoot_result == ShootResult.miss:
                        print("\033[36m{}".format("Bot is miss!"))
                        self.not_kill_nowhere_shoot = False
                        self.where_i_was_shooting.append(cell)
                        return ShootResult.miss
                    if shoot_result == ShootResult.kill:
                        print("\033[31m{}".format('The ship is destroyed!'))
                        self.not_kill_nowhere_shoot = False
                        self.where_i_was_shooting.append(cell)
                        for x in range(-1, 2):
                            for y in range(-1, 2):
                                if (0 <= cell[0] + x < 10 and 0 <= cell[1] + y < 10
                                        and cell not in self.where_i_was_shooting):
                                    rand_row_not_ship = cell[0] + x
                                    rand_column_not_ship = cell[1] + y
                                    not_ship = (rand_row_not_ship, rand_column_not_ship)
                                    if not_ship not in self.where_i_was_shooting:
                                        self.where_i_was_shooting.append(not_ship)
                        self.bot_hit_a_ship.clear()
                        return ShootResult.kill
                    if shoot_result == ShootResult.hit:
                        self.where_i_was_shooting.append(cell)
                        for x in range(-1, 2, 2):
                            for y in range(-1, 2, 2):
                                if (0 <= cell[0] + x < 10 and 0 <= cell[1] + y < 10
                                        and cell not in self.where_i_was_shooting):
                                    rand_row_not_ship = cell[0] + x
                                    rand_column_not_ship = cell[1] + y
                                    not_ship = (rand_row_not_ship, rand_column_not_ship)
                                    if not_ship not in self.where_i_was_shooting:
                                        self.where_i_was_shooting.append(not_ship)
                        self.bot_hit_a_ship.append(cell)
                        self.not_kill_nowhere_shoot = False
                        print("\033[31m{}".format('Hit! Get another shot.'))
                        return ShootResult.hit
                else:
                    continue
                break

            if self.not_kill_nowhere_shoot is True:
                rand_row = self.bot_hit_a_ship[0][0]
                rand_column = self.bot_hit_a_ship[0][1]
                cell_around = ((rand_row, rand_column - 1), (rand_row, rand_column + 1),
                               (rand_row - 1, rand_column), (rand_row + 1, rand_column))
                for cell in cell_around:
                    if (0 <= cell[0] < 10 and 0 <= cell[1] < 10) and (cell not in self.where_i_was_shooting):
                        shoot_result = self.opponent_field.check_shoot(cell)
                        print((letters[cell[0]]), cell[1] + 1)
                        if shoot_result == ShootResult.miss:
                            print("\033[36m{}".format("Bot is miss!"))
                            self.where_i_was_shooting.append(cell)
                            return ShootResult.miss
                        if shoot_result == ShootResult.kill:
                            print("\033[31m{}".format('The ship is destroyed!'))
                            self.where_i_was_shooting.append(cell)
                            self.bot_hit_a_ship.clear()
                            for x in range(-1, 2, 2):
                                for y in range(-1, 2, 2):
                                    if (0 <= cell[0] + x < 10 and 0 <= cell[1] + y < 10
                                            and cell not in self.where_i_was_shooting):
                                        rand_row_not_ship = cell[0] + x
                                        rand_column_not_ship = cell[1] + y
                                        not_ship = (rand_row_not_ship, rand_column_not_ship)
                                        if not_ship not in self.where_i_was_shooting:
                                            self.where_i_was_shooting.append(not_ship)
                            return ShootResult.kill
                        if shoot_result == ShootResult.hit:
                            print("\033[31m{}".format('Hit! Get another shot.'))
                            self.where_i_was_shooting.append(cell)
                            for x in range(-1, 2, 2):
                                for y in range(-1, 2, 2):
                                    if (0 <= cell[0] + x < 10 and 0 <= cell[1] + y < 10
                                            and cell not in self.where_i_was_shooting):
                                        rand_row_not_ship = cell[0] + x
                                        rand_column_not_ship = cell[1] + y
                                        not_ship = (rand_row_not_ship, rand_column_not_ship)
                                        if not_ship not in self.where_i_was_shooting:
                                            self.where_i_was_shooting.append(not_ship)
                            self.bot_hit_a_ship.append(cell)
                            return ShootResult.hit
                    else:
                        continue
