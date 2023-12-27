from field import Field
from enums import Direction, ShootResult
from random import randint, choice


class Player:
    """Абстрактный игрок"""

    def __init__(self):
        self.own_field = Field()
        self.opponent_field = Field()
        self.where_i_was_shooting = []


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


class Human(Player):

    def __init__(self, name: str):
        super().__init__()
        self.name = "\033[32m{}".format(name)

    def place_ships(self):
        """Спрашиваем пользователя куда и ставим корабли"""
        print(self.name, "\033[0m{}".format('please put the ships on your field.'))
        ships = [[4, 1]]
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

                    if self.opponent_field.is_killed_all():
                        return ShootResult.kill
                    else:
                        print("\033[31m{}".format('The ship is destroyed! Get another shot.'))
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
        random_names_for_bot = ['Bot_Galina', 'Bot_Sigizmund', 'Bot_Erjan', 'Bot_Edelstan', 'Bot_Ragnar']
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
        while not self.opponent_field.is_killed_all():
            print(self.name, "\033[0m{}".format('Select a coordinate for the shot'))
            rand_row = randint(0, 9)
            rand_column = randint(0, 9)
            shoot_coord = (rand_row, rand_column)
            while shoot_coord in self.where_i_was_shooting:
                rand_row = randint(0, 9)
                rand_column = randint(0, 9)
                shoot_coord = (rand_row, rand_column)
            if self.check_is_not_shoot_early(shoot_coord) is True:
                shoot_result = self.opponent_field.check_shoot(shoot_coord)
                if shoot_result == ShootResult.hit:
                    print("\033[31m{}".format('Hit! Get another shot.'))
                    return ShootResult.hit
                if shoot_result == ShootResult.kill:

                    if self.opponent_field.is_killed_all():
                        return ShootResult.kill
                    else:
                        print("\033[31m{}".format('The ship is destroyed! Get another shot.'))
                    return ShootResult.kill
                if shoot_result == ShootResult.miss:
                    print("\033[36m{}".format("You are miss!"))
                    return ShootResult.miss



                # if self.opponent_field.check_shoot(*shoot_coord) == ShootResult.hit:
                #     while not ShootResult.kill:
                #         for _ in self.opponent_field[0:-1]:
                #             for x in range(-1, 2):
                #                 for y in range(-1, 2):
                #                     if not rand_row + x >= 10 or rand_column + y >= 10:
                #                         new_rand_row = rand_row + x
                #                         new_rand_column = rand_column + y
                #                         shoot_coord = (new_rand_row, new_rand_column)
                #                         if shoot_coord not in where_i_was_shooting:
                #                             where_i_was_shooting.append(shoot_coord)
                #                             self.opponent_field.check_shoot(*shoot_coord)

