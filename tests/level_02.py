import sys
sys.path.append('level_02')
from game_class import *
from player_class import *

num_wins = {1: 0, 2: 0}
scouts_remaining = {1: 0, 2: 0}
for _ in range(200):
    players = [CustomPlayer(), CustomPlayer()]
    game = Game(players)
    game.run_to_completion()
    winner = game.state['winner']
    scouts_remaining[winner] += len(game.state['players'][winner]['scout_coords'])

    num_wins[winner] += 1
avg_scouts_remaining = {k:v/200 for k,v in scouts_remaining.items()}

assert abs(num_wins[1] - num_wins[2]) <= 40
assert abs(avg_scouts_remaining[1] - avg_scouts_remaining[2]) <= 0.5
print("Passed")