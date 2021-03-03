import sys
sys.path.append('level_00')
from game_class import *
from player_class import *

players = [RandomPlayer(), CustomPlayer()]
game = Game(players)

assert game.state == {
    'turn': 1,
    'board_size': [7,7],
    'players': {
        1: {
            'scout_coords': (4, 1),
            'home_colony_coords': (4, 1)
        },
        2: {
            'scout_coords': (4, 7),
            'home_colony_coords': (4, 7)
        }
    },
    'winner': None
}

game.complete_turn()
print(game.state)

game.run_to_completion()
print(game.state)