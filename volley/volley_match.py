'''Volleyball Match module'''
from typing import List, Dict, Union

from .volley_player import VolleyRoster

class VolleyGame(object):
    '''Class representing a volleyball game keeping stats and records.

    '''
    total_court_pos = 6

    def __init__(self, game : Dict[str, Union[int, bool, List[int], List[Union[str, int]]]]) \
                                                                                -> "VolleyGame":
        self.lineup= game['lineup']
        self.team_scores = game['team_scores']
        self.oppo_scores = game['oppo_scores']
        self.serve_start = game['serve']
        self.full = game['full']
        self.match = game['match']
        self.game = game['game']
        self.stats = None
        self.won = None

    def calc_pos_stats(self, lineup_index: int) -> List[List[int]]:
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
            index = self.lineup.index(lineup_index)
        else:
            index = (self.lineup.index(lineup_index) + 1) % (self.total_court_pos - 1)

        for score in self.team_scores:
            if isinstance(score, int):
                pos_stats[index][0] += 1
            elif score in ('R', 'r'):
                index = (index + 1) % (self.total_court_pos - 1)
            else:
                raise Exception("unknown item passed in team_scores")

        if self.serve_start:
            index = self.lineup.index(lineup_index)
        else:
            index = (self.lineup.index(lineup_index) + 1) % (self.total_court_pos - 1)

        for score in self.oppo_scores:
            if isinstance(score, int):
                pos_stats[index][1] -= 1
            elif score in ('R', 'r'):
                index = (index + 1) % (self.total_court_pos - 1)
            else:
                raise Exception("unknown item passed in oppo_scores")

        return pos_stats

    def calc_game_stats(self) -> None:
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
            players[num] = {'run': [], 'serves': 0, 'scores': [], 'points': 0,
                            'pos_stats': self.calc_pos_stats(num)}

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

    def get_game_stats(self) -> Dict[str, int]:
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

    def get_game_lineup(self) -> List[int]:
        '''Gets the game lineup.

            Returns:
                self.lineup -> list()
                    list of all jersey numbers seen in this game
        '''
        return self.lineup

class VolleyMatch(object):
    '''Class representing a volleyball match composed of multiple games.

        Attributes:
            games       (list)
            stats       ()

    '''
    def __init__(self, games : List[VolleyGame]) -> "VolleyMatch":
        self.games = games
        self.stats = None

    def add_game(self, game : VolleyGame) -> None:
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
        self.games.append(game)

    def calc_match_stats(self) -> None:
        '''Calculates match stats.
        '''
        players = {}

        for game in self.games:
            # initialize player's plus/minus stats
            lineup = game.get_game_lineup()
            for num in lineup:
                if num not in players:
                    players[num] = {'total_match_points': 0,
                                    'total_match_serves': 0,
                                    'games': 0,
                                    'pos_stats': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]}

            # populate player stats from each game
            game_stats = game.get_game_stats()
            for key in game_stats.keys():
                players[key]['total_match_points'] += game_stats[key]['points']
                players[key]['total_match_serves'] += game_stats[key]['serves']
                players[key]['pos_stats'] = [list(map(sum, zip(*n)))
                            for n in zip(players[key]['pos_stats'], game_stats[key]['pos_stats'])]
                if game.full:
                    players[key]['games'] += 1
                else:
                    players[key]['games'] += 0.5

        for player in players.items():
            player[1]['ppg'] = player[1]['total_match_points'] / player[1]['games']
            player[1]['pps'] = player[1]['total_match_points'] / player[1]['total_match_serves']

        self.stats = players

    def print_player_stats(self, roster : VolleyRoster) -> None:
        '''Prints a player's stats.

            Params:
                roster : VolleyRoster containing all player's info and status.
        '''
        # game = self.games[0]
        # for key in game.stats.keys():
        #     name = roster.get_player_name(key)
        #     print(f'({key:02d}) {name} {" "*(8-len(name))} => ', game.stats[key])
        print(" Name ".center(16, '-'), "=>",  # 16
               "Total Games",          "|",  # 11
               "Serve Rotations",      "|",  # 15
               "RB CB LB LF CF RF +/- Stats", "|",  #27
               "Pts/Serve",            "|",  # 9
               "Pts/Game",             "|")  # 8
        # sort dictionary by ppg
        stats = dict(sorted(self.stats.items(), key=lambda x:x[1]['ppg'], reverse=True))

        for item in stats.items():
            num = item[0]
            player = item[1]
            name = roster.get_player_name(num)
            print(f"({num:02d}) {name}".ljust(16, ' '), '=>',\
                  f"{player['games']:11.1f}",            "|",
                  f"{player['total_match_serves']:>15}", "|",
                  f"{player['pos_stats']}",              "|",
                  f"{player['pps']:9.2f}",               "|",
                  f"{player['ppg']:8.2f}",               "|")
