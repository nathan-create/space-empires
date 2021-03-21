import math
import random
import sys
sys.path.append('logs')
from logger import *
random.seed(1)

class Game:
    def __init__(self, players, board_size=[7,7]):
        self.players = players
        self.set_player_numbers()
        self.combat_coords = {}
        self.log = Logger('/home/runner/space-empires/logs/level-0.3-logs.txt')
        self.log.clear_log()

        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2

        self.state = {
            'turn': 1,
            'board_size': board_size,
            'players': {
                1: {
                    'scout_coords': {
                        1: (mid_x, 1),
                        2: (mid_x, 1),
                        3: (mid_x, 1),
                    },
                    'home_colony_coords': (mid_x, 1)
                },
                2: {
                    'scout_coords': {
                        1: (mid_x, board_y),
                        2: (mid_x, board_y),
                        3: (mid_x, board_y),
                    },
                    'home_colony_coords': (mid_x, board_y)
                }
            },
            'winner': None
        }

    def set_player_numbers(self):
        for i,player in enumerate(self.players):
            player.set_player_number(i+1)

    def check_if_coords_are_in_bounds(self, coords):
        x, y = coords
        board_x, board_y = self.state['board_size']
        if 1 <= x and x <= board_x:
            if 1 <= y and y <= board_y:
                return True
        return False

    def check_if_translation_is_in_bounds(self, coords, translation):
        max_x, max_y = self.state['board_size']
        x, y = coords
        dx, dy = translation
        new_coords = (x+dx,y+dy)
        return self.check_if_coords_are_in_bounds(new_coords)

    def get_in_bounds_translations(self, coords):
        translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
        in_bounds_translations = []
        for translation in translations:
            if self.check_if_translation_is_in_bounds(coords, translation):
                in_bounds_translations.append(translation)
        return in_bounds_translations

    def move_phase(self):
        self.log.write('\nBEGINNING OF TURN ' + str(self.state['turn']) + ' MOVEMENT PHASE\n\n')
        for player_num in self.state['players']:
            player_scouts = self.state['players'][player_num]['scout_coords']
            opponent_scouts = self.state['players'][3-player_num]['scout_coords']
            dead_scouts = [coord for key in self.combat_coords for coord in self.combat_coords[key]]
            for scout_num in player_scouts:
                if (player_num, scout_num) in dead_scouts:
                    continue
                scout = player_scouts[scout_num]
                choices = self.get_in_bounds_translations(scout)
                player = self.players[player_num - 1]
                move = player.choose_translation(self.state, choices, scout_num)
                new_coords = (scout[0]+move[0], scout[1]+move[1])
                self.state['players'][player_num]['scout_coords'][scout_num] = new_coords
                self.log.write('\tPlayer ' + str(player_num) + ' Scout ' + str(scout_num) + ': ' + str(scout) + ' -> ' + str(new_coords) + '\n')

                for opp_scout in opponent_scouts:
                    if opponent_scouts[opp_scout]==new_coords and new_coords not in self.combat_coords:
                        self.combat_coords[new_coords] = [(3-player_num, opp_scout)]
                    elif opponent_scouts[opp_scout]==new_coords and new_coords in self.combat_coords:
                        if (3-player_num, opp_scout) not in self.combat_coords[new_coords]:
                            self.combat_coords[new_coords].append((3-player_num, opp_scout))
                if new_coords in self.combat_coords:
                    self.combat_coords[new_coords].append((player_num, scout_num))
        self.log.write('\nEND OF TURN ' + str(self.state['turn']) + ' MOVEMENT PHASE\n')

    def find_target(self, player_num, combat_order):
        for scout in combat_order:
            if scout[0] != player_num:
                return scout

    def list_all_equal(self, input_list):
        for i in range(len(input_list)):
            if i != 0:
                if input_list[i] != input_list[i-1]:
                    return False
        return True

    def combat_phase(self):
        if self.state['winner'] != None:
            return None
        self.log.write('\nBEGINNING OF TURN ' + str(self.state['turn']) + ' COMBAT PHASE\n')
        if len(self.combat_coords) != 0:
            self.log.write('\n\tCombat Locations:\n')
            for location in self.combat_coords:
                self.log.write('\n\t\t'+str(location)+'\n\n')
                for scout in self.combat_coords[location]:
                    self.log.write('\t\t\tPlayer '+str(scout[0])+' Scout '+str(scout[1])+'\n')

        to_delete_coords = []
        for coord in self.combat_coords:
            self.log.write('\n\tCombat at ' + str(coord) + '\n')
            all_scouts = self.combat_coords[coord]
            while not self.list_all_equal([scout[0] for scout in all_scouts]):
                for scout in all_scouts:
                    attacker = scout
                    defender = self.find_target(scout[0], self.combat_coords[coord])
                    if defender == None:
                        break
                    self.log.write('\n\t\tAttacker: Player '+str(attacker[0])+' Scout '+str(attacker[1]))
                    self.log.write('\n\t\tDefender: Player '+str(defender[0])+' Scout '+str(defender[1]))
                    if round(random.random()) == 0:
                        self.log.write('\n\t\t(Miss)\n')
                        continue
                    self.log.write('\n\t\tHit!')
                    all_scouts.remove(defender)
                    del self.state['players'][defender[0]]['scout_coords'][defender[1]]
                    self.log.write('\n\t\tPlayer '+str(defender[0])+' Scout '+str(defender[1])+' was destroyed\n')
            self.log.write('\n\tSurvivors:\n')
            self.log.write('\n\t\t'+str(coord)+'\n')
            for scout in self.combat_coords[coord]:
                self.log.write('\n\t\t\tPlayer '+str(scout[0])+' Scout '+str(scout[1]))
            to_delete_coords.append(coord)
            self.log.write('\n')
        for coord in to_delete_coords:
            del self.combat_coords[coord]
        self.log.write('\nEND OF TURN ' + str(self.state['turn']) + ' COMBAT PHASE\n')
        self.state['turn'] += 1
        self.state['winner'] = self.check_for_winner()

    def run_to_completion(self):
        while self.state['winner'] == None:
            self.move_phase()
            self.combat_phase()

    def check_for_winner(self):
        p1_scouts = self.state['players'][1]['scout_coords']
        p1_base = self.state['players'][1]['home_colony_coords']
        p2_scouts = self.state['players'][2]['scout_coords']
        p2_base = self.state['players'][2]['home_colony_coords']

        p1_coords = [p1_scouts[key] for key in p1_scouts]
        p2_coords = [p2_scouts[key] for key in p2_scouts]

        if not any(coord1==p2_base for coord1 in p1_coords) and not any(coord2==p1_base for coord2 in p2_coords):
            return None
        if any(coord1==p2_base for coord1 in p1_coords) and not any(coord2==p1_base for coord2 in p2_coords):
            self.log.write('\nWINNER: PLAYER 1')
            return 1
        if not any(coord1==p2_base for coord1 in p1_coords) and any(coord2==p1_base for coord2 in p2_coords):
            self.log.write('\nWINNER: PLAYER 2')
            return 2
        if any(coord1==p2_base for coord1 in p1_coords) and any(coord2==p1_base for coord2 in p2_coords):
            self.log.write('\nTIE GAME')
            return "Tie"