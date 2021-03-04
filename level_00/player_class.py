from random import random
import math

def dist(start_point, end_point):
    x = end_point[0] - start_point[0]
    y = end_point[1] - start_point[1]
    return (x ** 2 + y ** 2) ** 0.5

class RandomPlayer():
    def __init__(self):
        self.player_number = None

    def set_player_number(self, n):
        self.player_number = n

    def choose_translation(self, game_state, choices):
        # `choices` is a list of possible translations,
        # e.g. [(0,0), (-1,0), (0,1)] if the player's
        # scout is in the bottom-right corner of the board

        random_idx = math.floor(len(choices) * random())
        return choices[random_idx]

class CustomPlayer():
    def __init__(self):
        self.player_number = None

    def set_player_number(self, n):
        self.player_number = n

    def get_opponent_player_number(self):
        if self.player_number == None:
            return None

        elif self.player_number == 1:
            return 2

        elif self.player_number == 2:
            return 1

    def choose_translation(self, game_state, choices):
        myself = game_state['players'][self.player_number]
        opponent_player_number = self.get_opponent_player_number()
        opponent = game_state['players'][opponent_player_number]

        my_scout_coords = myself['scout_coords']
        opponent_home_colony_coords = opponent['home_colony_coords']

        closest_choice = choices[0]
        smallest_dist_coords = (my_scout_coords[0] + closest_choice[0], my_scout_coords[1] + closest_choice[1])
        smallest_dist = dist(smallest_dist_coords, opponent_home_colony_coords)

        for choice in choices:
            updated_coords = (my_scout_coords[0] + choice[0], my_scout_coords[1] + choice[1])
            if dist(updated_coords, opponent_home_colony_coords) < smallest_dist:
                closest_choice = choice
                smallest_dist = dist(updated_coords, opponent_home_colony_coords)

        return closest_choice