from player import Player, Human, Bot
from enums import ShootResult
from random import choice


class Game:
    """Game object"""

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        rand = [self.player1, self.player2]
        self.current_player = choice(rand)
        if self.current_player == self.player1:
            self.opponent_player = self.player2
        else:
            self.opponent_player = self.player1

        self.current_player.place_ships()
        self.opponent_player.place_ships()

    def __switch_players(self):
        self.current_player, self.opponent_player = self.opponent_player, self.current_player

    def start(self):
        """Основной игровой цикл"""
        while self.winner is None:
            # Спрашиваем противника о результате выстрела
            self.current_player.opponent_field = self.opponent_player.own_field
            shoot_result = self.current_player.shoot()

            match shoot_result:
                case ShootResult.miss:
                    self.__switch_players()
                case ShootResult.hit:
                    pass
                case ShootResult.kill:
                    if self.current_player.opponent_field.is_killed_all():
                        self.winner = self.current_player
                    else:
                        print("\033[31m{}".format('Get another shot.'))

        if isinstance(self.winner, Human):
            print("\033[35m{}".format('All ship is destroyed!'))
            print("\033[33m{}".format(f"Game over! Congratulations, the winner is player {self.winner.name}"))
        else:
            if isinstance(self.winner, Bot):
                if self.winner == self.player1:
                    print("\033[35m{}".format('All ship is destroyed!'))
                    print("\033[33m{}".format(f"Game over! Congratulations, the winner is player {self.winner.name}"))
                else:
                    print("\033[35m{}".format('All ship is destroyed!'))
                    print("\033[33m{}".format(f"Game over! Congratulations, the winner is player {self.winner.name}"))

