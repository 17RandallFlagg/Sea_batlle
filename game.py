from player import Player, Human, Bot
from enums import ShootResult


class Game:
    """Game object"""

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.current_player = self.player1
        self.opponent_player = self.player2

        self.player1.place_ships()
        self.player2.place_ships()


    def __switch_players(self):
        self.current_player, self.opponent_player = self.opponent_player, self.current_player

    def start(self):
        """Основной игровой цикл"""
        while self.winner is None:
            # Спрашиваем текущего игрока куда стрелять
            row, column = self.current_player.shoot()
            # Спрашиваем противника о результате выстрела
            shoot_result = self.opponent_player.check_shoot(row, column)

            match shoot_result:
                case ShootResult.miss:
                    self.__switch_players()
                case ShootResult.hit:
                    pass
                case ShootResult.kill:
                    if self.opponent_player.is_killed_all():
                        self.winner = self.current_player

        if isinstance(self.winner, Human):
            print("Winner is", self.winner.name)
        else:
            if self.winner == self.player1:
                print("Winner is Bot 1")
            else:
                print("Winner is Bot 2")
