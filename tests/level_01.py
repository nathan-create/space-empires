import sys
sys.path.append('level_01')
from game_class import *
from player_class import *

# test A
players = [CustomPlayer(), CustomPlayer()]
game = Game(players)

game.move_phase()
game.combat_phase()
game.move_phase()
game.combat_phase()
game.move_phase()
game.combat_phase()
print(game.state['players'])

# test B
num_wins = {1: 0, 2: 0}
for _ in range(200):
    players = [CustomPlayer(), CustomPlayer()]
    game = Game(players)
    game.run_to_completion()
    winner = game.state['winner']
    num_wins[winner] += 1
print(num_wins)
