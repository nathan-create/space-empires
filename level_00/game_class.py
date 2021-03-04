class Game:
    def __init__(self, players, board_size=[7,7]):
        self.players = players
        self.set_player_numbers()

        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2

        self.game_state = {
            'turn': 1,
            'board_size': board_size,
            'players': {
                1: {
                    'scout_coords': (mid_x, 1),
                    'home_colony_coords': (mid_x, 1)
                },
                2: {
                    'scout_coords': (mid_x, board_y),
                    'home_colony_coords': (mid_x, board_y)
                }
            },
            'winner': None
        }

    def set_player_numbers(self):
        for i, player in enumerate(self.players):
            player.set_player_number(i+1)

    def check_if_coords_are_in_bounds(self, coords):
        x, y = coords
        board_x, board_y = self.game_state['board_size']
        if 1 <= x and x <= board_x:
            if 1 <= y and y <= board_y:
                return True
        return False

    def check_if_translation_is_in_bounds(self, coords, translation):
        max_x, max_y = self.game_state['board_size']
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

    def complete_turn(self):
        for player in self.game_state['players']:
            init_coords = self.game_state['players'][player]['scout_coords']
            choices = self.get_in_bounds_translations(init_coords)

            for p in self.players:
                if p.player_number == player:
                    move = p.choose_translation(self.game_state, choices)

            self.game_state['players'][player]['scout_coords'] = (init_coords[0] + move[0], init_coords[1] + move[1])
        self.game_state['turn'] += 1
        p1 = self.game_state['players'][1]
        p2 = self.game_state['players'][2]

        if p1['scout_coords'] != p2['home_colony_coords'] and p2['scout_coords'] != p1['home_colony_coords']:
            self.game_state['winner'] = None
        elif p1['scout_coords'] == p2['home_colony_coords'] and p2['scout_coords'] != p1['home_colony_coords']:
            self.game_state['winner'] =  1
        elif p1['scout_coords'] != p2['home_colony_coords'] and p2['scout_coords']== p1['home_colony_coords']:
            self.game_state['winner'] =  2
        elif p1['scout_coords'] == p2['home_colony_coords'] and p2['scout_coords'] == p1['home_colony_coords']:
            self.game_state['winner'] =  "Tie"

    def run_to_completion(self):
        while self.game_state['winner'] == None:
            self.complete_turn()