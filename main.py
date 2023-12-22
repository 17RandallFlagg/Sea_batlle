from game import Game
from player import Human, Bot


if __name__ == '__main__':
    """Точка старта"""
    Choose_player1 = input('Choose the first player, Human or Bot = '.lower())
    if Choose_player1 == 'human':
        player1 = Human(input('How is your name? = '))
    else:
        player1 = Bot()

    Choose_player2 = input('Choose the second player, Human or Bot = '.lower())
    if Choose_player2 == 'human':
        player2 = Human(input('How is your name? = '))
    else:
        player2 = Bot()
    game = Game(player1, player2)

    game.start()
