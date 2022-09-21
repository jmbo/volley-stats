'''Volleyball Match module'''

class VolleyGame(object):
    '''Class representing a volleyball game keeping stats and records.

    '''
    total_court_pos = 6

    def __init__(self, lineup, team_scores, oppo_scores, serve_start, full):
        self.lineup= lineup
        self.team_scores = team_scores
        self.oppo_scores = oppo_scores
        self.serve_start = serve_start
        self.full = full
        self.stats = None
        self.won = None

    def calc_pos_stats(self, lineup_index):
        '''Calculates the plus/minus stats for each position in a game for a starting position in
           the lineup.

            Params:
                lineup_index (int): index of the starting position in the lineup list
            Return:
                pos_stats   (list): +/- stats for each position the player was on as they rotated
                    around the court. Each item in the list is a 2 item list where the first item
                    contains the +points for that player at that position and the second item
                    contains the -points for that player at that position. The first item on the
                    list is indicates the RB (Server) position with each next item being the next
                    (counterclockwise [CCW]) position on the court.
        '''
        # #### NET #####
        # [LF, CF, RF]
        # [LB, CB, RB]

        # initializing pos stats starting with RB and ending with CB -- each item in the list
        # represents [points scored by the team, points lost by the team]
        pos_stats = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

        if self.serve_start:
            index = lineup_index
        else:
            index = (lineup_index + 1) % (self.total_court_pos - 1)

        for score in self.team_scores:
            if isinstance(score, int):
                pos_stats[index][0] += 1
            elif score in ('R', 'r'):
                index = (index + 1) % (self.total_court_pos - 1)
            else:
                raise Exception("unknown item passed in team_scores")

        if self.serve_start:
            index = lineup_index
        else:
            index = (lineup_index + 1) % (self.total_court_pos - 1)

        for score in self.oppo_scores:
            if isinstance(score, int):
                pos_stats[index][0] -= 1
            elif score in ('R', 'r'):
                index = (index + 1) % (self.total_court_pos - 1)
            else:
                raise Exception("unknown item passed in oppo_scores")

        return pos_stats

    def calc_game_stats(self):
        '''Calculates game stats for this game.
        '''
        # determine if game was Lost or Won
        if self.team_scores[-1] in ('R', 'r'):
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
        for score in self.team_scores:
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

class VolleyMatch(object):
    '''Class representing a volleyball match composed of multiple games.

    Methods:
        add_game(game) : adds a game to the class instance

    '''
    def __init__(self, games=None):
        self.games = []
        self.stats = None

        if games:
            for game in games:
                self.add_game(game['lineup'], game['team_scores'], game['oppo_scores'],
                         game['serve'], game['full'])

    def add_game(self, lineup, team_scores, oppo_scores, serve_start=True, full=True):
        '''add_game() adds a game to the class instance.

            Params:
                lineup      (list): list containing starting lineup
                team_scores (list): list containing all points scored by the team as well as when
                    the return to the opposing team was made
                oppo_scores (list): list containing all points score by opposing team as well as
                    when the return to the team was made
                serve_start (bool): indicates whether the team started the serve for this game
                full        (bool): indicates whether this game was played to the end of a reg set
        '''
        self.games.append(VolleyGame(lineup, team_scores, oppo_scores, serve_start, full))

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
