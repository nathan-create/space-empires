import sys
sys.path.append('level_03')
from game_class import *
from player_classes import *

players = [CustomPlayer(), CustomPlayer()]
game = Game(players)
game.run_to_completion()