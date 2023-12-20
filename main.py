from game import Game
from player import Player, Human, Bot


if __name__ == '__main__':
    """Точка старта"""
    Choose_player1 = input('Choose the first player, Human or Bot = ')
    if Choose_player1 == 'Human':
        player1 = Human(input('How is your name? = '))
    else:
        player1 = Bot('')

    Choose_player2 = input('Choose the second player, Human or Bot = ')
    if Choose_player2 == 'Human':
        player2 = Human(input('How is your name? = '))
    else:
        player2 = Bot('')
    game = Game(player1, player2)
