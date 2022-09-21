'''Volleyball Match module'''

class VolleyMatch(object):
    '''Class representing a volleyball match composed of multiple games.

    Methods:
        add_game(game) : adds a game to the class instance

    '''
    def __init__(self, games=None):
        self.games = []
        self.stats = None

        if games:
            start = False
            full = False

            for game in games:
                lineup = game[0]
                scores = game[1]
                game = lineup.pop(0)

                if game[0].lower() == 'f':
                    full = True
                if game[1].lower() == 's':
                    start = True

                self.games.append(VolleyGame(lineup, scores, start, full))

    def add_game(self, game):
        '''add_game() adds a game to the class instance.

            Params:
                game : list containing two lists. First list contains the game
                       status in form a string followed by the numbered lineup.
                       The second lists contains the game score.'''
        start = False
        full = False

        lineup = game[0]
        scores = game[1]
        game = lineup.pop(0)

        if game[0].lower() == 'f':
            full = True
        if game[1].lower() == 's':
            start = True

        self.games.append(VolleyGame(lineup, scores, start, full))

    def calc_match_stats(self):
        '''Calculates match stats.
        '''
        players = {}

        for game in self.games:
            # initialize players
            lineup = game.get_game_lineup()
            for num in lineup:
                if num not in players.keys():
                    players[num] = {'total_match_points': 0, 'total_match_serves': 0, 'games': 0}

            # populate player stats from each game
            game_stats = game.get_game_stats()
            for key in game_stats.keys():
                players[key]['total_match_points'] += game_stats[key]['points']
                players[key]['total_match_serves'] += game_stats[key]['serves']
                if game.full:
                    players[key]['games'] += 1
                else:
                    players[key]['games'] += 0.5

        for player in players.items():
            player[1]['ppg'] = player[1]['total_match_points'] / player[1]['games']
            player[1]['pps'] = player[1]['total_match_points'] / player[1]['total_match_serves']

        self.stats = players

    def print_player_stats(self, roster):
        '''Prints a player's stats.

            Params:
                roster : VolleyRoster containing all player's info and status.
        '''
        # game = self.games[0]
        # for key in game.stats.keys():
        #     name = roster.get_player_name(key)
        #     print(f'({key:02d}) {name} {" "*(8-len(name))} => ', game.stats[key])
        print("---- Name----- =>  Total Games  |  Total Serves  |  Pts/Serve  |  Pts/Game  |")
        # sort dictionary by ppg
        stats = dict(sorted(self.stats.items(), key=lambda x:x[1]['ppg'], reverse=True))

        for item in stats.items():
            num = item[0]
            player = item[1]
            name = roster.get_player_name(num)
            print(f"({num:02d}) {name} {' '*(8-len(name))} => ", \
                  f"{player['games']:12.1f} | {player['total_match_serves']:>14} | " \
                  f"{player['pps']:11.2f} | {player['ppg']:10.2f} |")


class VolleyGame(object):
    '''Class representing a volleyball game keeping stats and records.

    '''
    total_court_pos = 6

    def __init__(self, lineup, game_scores, serve_start=True, full=True):
        self.lineup= lineup
        self.game_scores = game_scores
        self.serve_start = serve_start
        self.full = full
        self.stats = None
        self.won = None

    def calc_game_stats(self):
        '''Calculates game stats for this game.
        '''
        # determine if game was Lost or Won
        if self.game_scores[-1] in ('R', 'r'):
            self.won = False
        else:
            self.won = True

        # initialize players
        players = {}
        for num in self.lineup:
            players[num] = {'run': [], 'serves': 0, 'scores': [], 'points': 0}

        # process game scores
        pos = 0
        sco = 0
        run = 0
        for score in self.game_scores:
            if score in ('R', 'r'):
                players[self.lineup[pos % self.total_court_pos]]['run'].append(run)
                players[self.lineup[pos % self.total_court_pos]]['serves'] += 1
                pos += 1
                run = 0
            else:
                sco += 1
                run += 1
                if sco != score:
                    raise Exception("Scoring unmatched or incomplete")
                players[self.lineup[pos % self.total_court_pos]]['scores'].append(score)

        for item in players.items():
            player = item[1]
            if sum(player['run']) != len(player['scores']):
                raise Exception("Player's scores and point runs do not match")

            player['points'] = len(player['scores'])

        self.stats = players

    def get_game_stats(self):
        '''Gets game stats for this game.

            Returns:
                self.stats -> dict()
                    keys  : each player's jersey number
                    values:
                    'run' = indicates number of successful points for each serve run in this game
                    'serves' = indicates total number of serve runs in this game
                    'scores' = indicates which score points the player served in
                    'points' = indicates total points player served on this game
        '''
        self.calc_game_stats()
        return self.stats

    def get_game_lineup(self):
        '''Gets the game lineup.

            Returns:
                self.lineup -> list()
                    list of all jersey numbers seen in this game
        '''
        return self.lineup
