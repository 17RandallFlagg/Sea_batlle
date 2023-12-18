from game import Game
from player import Player, Human, Bot


if __name__ == '__main__':
    """Точка старта"""
    player1 = Human("Федор")
    player2 = Bot()
    game = Game(player1, player2)
