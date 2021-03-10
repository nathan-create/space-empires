from random import random
import math

def calc_dist(start_point, end_point):
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    return math.sqrt(dx**2 + dy**2)

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
        opponent_num = self.get_opponent_player_number()
        opponent = game_state['players'][opponent_num]

        my_scout_coords = myself['scout_coords']
        opponent_home_coords = opponent['home_colony_coords']

        closest_choice = choices[0]
        smallest_dist_coords = (my_scout_coords[0] + closest_choice[0], my_scout_coords[1] + closest_choice[1])
        smallest_dist = calc_dist(smallest_dist_coords, opponent_home_coords)


        for choice in choices:
            updated_coords = (my_scout_coords[0] + choice[0], my_scout_coords[1] + choice[1])

            if calc_dist(updated_coords, opponent_home_coords) < smallest_dist:
                closest_choice = choice
                smallest_dist = calc_dist(updated_coords, opponent_home_coords)

        return closest_choice