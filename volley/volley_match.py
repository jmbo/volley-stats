'''Volleyball Match module'''
# TODO: add game validation logic
## validate score swip-swap, score order, win by 2,
## check if half or full game from scores reported
## determine include based on validation
## no need to require 'X' at end of scores
## record final scored recorded and detect discrepancies

from typing import List, TypedDict, Union

from .volley_player import VolleyRoster
from .volley_stats import VolleyStats, PLUS, MINUS

class VolleyGameType(TypedDict):
    "Typing class for Dictionary structure received from parsing the Volleyball YAML info sheet"
    lineup          : List[int]
    team_scores     : List[Union[str, int]]
    opponent_scores : List[Union[str, int]]
    serve           : bool
    include         : bool
    full            : bool
    game            : int

class VolleyGame():
    '''Class representing a volleyball game keeping stats and records.

    '''
    total_court_pos = 6

    def __init__(self, game : VolleyGameType) -> None:
        self.lineup      = game['lineup']
        self.team_scores = game['team_scores']
        self.oppo_scores = game['opponent_scores']
        self.serve_start = game['serve']
        self.include     = game['include']
        self.full        = game['full']
        self.game        = game['game']
        self.game_stats  = VolleyStats(self.lineup)

        # calculate stats if games is to be included in stats
        if self.include:
            self._calc_game_stats()

    def _calc_game_stats(self) -> None:
        '''Calculates game stats for this game.
        '''
        # calculate game final scores
        self.game_stats.add_final_score(max([x for x in self.team_scores if str(x).isdigit()]),
                                        max([x for x in self.oppo_scores if str(x).isdigit()]))

        ### PROCESS Team Scored Points Against Opponent
        # initialize team rotation
        rotation = self.lineup.copy()
        if not self.serve_start:
            # rotate the rotation back 1 if we start receiving
            rotation = rotation[-1:] + rotation[:-1]
            assert int(self.team_scores[0])

        # team_scores: ['R', 1, 2, 'R', 3, 'R', 4, 'R', 5, 6, 7, 'R', 8, 9, 'R', 10, 'R', 11, 'R', 12, 13, 14, 'R']                     serve_start = true
        # team_scores: [1, 2, 'R', 3, 'R', 4, 5, 6, 'R', 7, 8, 'R', 9, 'R', 10, 'R', 11, 12, 13, 'R', 14, 'R', 15, 16, 'R', 17, 'R']    serve_start = true  || false

        sco : List[int] = []
        start = self.serve_start
        for score in self.team_scores:
            if score in ('R', 'r', 'X', 'x'):
                self.game_stats.add_score_run(rotation, sco, PLUS, beg=start)
                rotation = rotation[1:] + rotation[:1]
                start = False
                sco = []
            else:
                sco.append(int(score))

        ### PROCESS Opponent Scored Points Against Team
        # initialize team rotation
        rotation = self.lineup.copy()
        if not self.serve_start:
            # rotate the rotation back 1 if we start receiving
            rotation = rotation[-1:] + rotation[:-1]

        sco = []
        for score in self.oppo_scores:
            if score in ('R', 'r', 'X', 'x'):
                self.game_stats.add_score_run(rotation, sco, MINUS)
                rotation = rotation[1:] + rotation[:1]
                sco = []
            else:
                sco.append(int(score))

        ### FINALIZE Game Stats
        self.game_stats.finish_game(self.full)


        # for item in self.player_stats.items():
        #     player = item[1]

        #     # calculate the +/- stats for each player in this game
        #     # positive should be the total points scored by the team, negative should be the
        #     # score of the opposite team
        #     pos_sum = neg_sum = 0
        #     for i in player['pos_stats']:
        #         pos_sum += i[0]
        #         neg_sum += i[1]
        #     player['pm_stats'].append(pos_sum)
        #     player['pm_stats'].append(neg_sum)

        #     # calculate number of points player "scored" in the SERVE (RB) position
        #     if sum(player['run']) != len(player['scores']):
        #         raise Exception("Player's scores and point runs do not match")

        #     player['points'] = len(player['scores'])

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
    def __init__(self, oppo: str) -> None:
        self.opponent                = oppo
        self.games: List[VolleyGame] = []
        self.match_stats             = VolleyStats()

    def add_game(self, game : VolleyGameType)  -> None:
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
        self.games.append(VolleyGame(game))
        # add last added game's stats to match stats
        self.match_stats += self.games[-1].game_stats

class VolleySeason(object):
    '''Class representing a volleyball season composed of multiple matches.

        Attributes:
            games       (list)
            stats       ()

    '''
    def __init__(self, league: str, season: str, year: int, roster: VolleyRoster) -> None:
        self.matches: List[VolleyMatch] = []
        self.roster = roster
        self.league = str.upper(league) + ' ' + str.capitalize(season) + ' ' + str(year)

        self.season_stats  = VolleyStats()

    def __str__(self) -> str:
        return str(self.season_stats)

    def add_match(self, match: VolleyMatch) -> None:
        '''Adds a match info to the volleyball season.
        '''
        self.matches.append(match)
        # add last added match's stats to season stats
        self.season_stats += self.matches[-1].match_stats

    def print_match(self, match : int) -> None:
        """Function prints the provided Volleyball's Match Game information and Statistics."""

        self.matches[match].print_stats(self.roster)
