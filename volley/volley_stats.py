'''Volleyball Stats module'''
from typing import List, Dict, Union, Tuple

class PlayerStats():
    ''' Class representing Player Statistics kept throughout kept VolleyStats
    '''
    def __init__(self) -> None:
        self.rb_pm = self.rf_pm = self.cf_pm = [0, 0]
        self.lf_pm = self.lb_pm = self.cb_pm = [0, 0]

        self.front_row = self.back_row = self.pm_stats = [0, 0]

        self.total_serves  = 0
        self.served_scores = []
        self.serve_runs    = []

        self.total_serve_points = 0
        self.total_games_played = 0


class VolleyStats():
    ''' Class representing all Volleyball Statistics kept for games and/or matches.
    '''

    PLUS  = 0
    MINUS = 1
    ROTATION = ['RB', 'RF', 'CF', 'LF', 'LB', 'CB']
    HALF_GAME = 0.6

    GAME        = 0
    MATCH       = 1
    SEASON      = 2
    ALL_TIME    = 3

    def __init__(self, lineup : List[int] = None) -> None:
        self.back_row_stats  = {}
        self.front_row_stats = {}
        self.player_stats    = {}

        self.final_team_score = 0
        self.final_oppo_score = 0
        self.won = False

        self.stats_type = VolleyStats.GAME

        for num in lineup:
            # [RB, RF, CF, LF, LB, CB]
            self.player_stats[num] = {'RB': [0, 0], 'RF': [0, 0], 'CF': [0, 0],
                                      'LF': [0, 0], 'LB': [0, 0], 'CB': [0, 0],
                                      'front_row': [0, 0], 'back_row': [0, 0], 'pm_stats': [0, 0],
                                      'serve_runs': [], 'total_serves': 0, 'served_scores': [],
                                      'total_serve_points': 0, 'games': 0,}

    def __add__(self, other: "VolleyStats") -> "VolleyStats":
        obj = VolleyStats()

        # calculate type of result
        obj.stats_type = _calculate_new_stats_type(self, other)
        # calculate final team score
        obj.final_team_score, obj.final_oppo_score = _calculate_new_final_score(self, other)


        if obj.final_team_score > obj.final_oppo_score:
            obj.won = True



        return obj

    def add_final_score(self, team: int, oppo: int) -> None:
        ''' Add final game scores'''
        self.final_team_score = team
        self.final_oppo_score = oppo
        if team > oppo:
            self.won = True

    def add_score_run(self, rotation: List[int], scores: List[int], p_m: int, beg=False) -> None:
        '''Adds each player's corresponding position plus/minus points'''
        score = len(scores)

        if p_m == self.MINUS:
            score *= -1

        # TODO: process backrow/frontrow tuples

        # if processing positive (team) scores, every first point we gain on the return is part of
        # the old rotation, we then rotate and all points followed are from successful serves
        # the only exception is at the beginning of the game if the team starts by serving, then all
        # points gained before the return are from successful serves
        if p_m == self.PLUS and not beg:
            rotation = rotation[-1:] + rotation[:-1]
            for i, pos in enumerate(self.ROTATION):
                self.player_stats[rotation[i]][pos][p_m]        += 1
                self.player_stats[rotation[i]]['pm_stats'][p_m] += 1
            rotation = rotation[1:] + rotation[:1]
            scores.pop(0)
            score -= 1

        for i, pos in enumerate(self.ROTATION):
            self.player_stats[rotation[i]][pos][p_m]        += score
            self.player_stats[rotation[i]]['pm_stats'][p_m] += score

        # assign serving stats to server position when processing positive (team) scores
        if p_m == self.PLUS:
            self.player_stats[rotation[0]]['served_scores'].append(scores)
            self.player_stats[rotation[0]]['serve_runs'].append(score)
            self.player_stats[rotation[0]]['total_serves'] += 1


    def finish_game(self, full : bool) -> None:
        '''At the end of each game calculate remaining stats for each player after all points are
         attributed. '''
        for player in self.player_stats:
            player['total_serve_points'] = len(player['served_scores'])

            player['front_row'] = [x1 + x2 + x3 for (x1, x2, x3) in zip(player['RF'],
                                                                        player['CF'],
                                                                        player['LF'])]
            player['back_row'] = [x1 + x2 + x3 for (x1, x2, x3) in zip(player['RB'],
                                                                       player['CB'],
                                                                       player['LB'])]
            if full:
                player['games'] += 1
            else:
                player['games'] += self.HALF_GAME

def _calculate_new_stats_type(left : VolleyStats, right : VolleyStats) -> int:
    if (left.stats_type == left.GAME and right.stats_type == right.GAME) or \
       (left.stats_type == left.MATCH and right.stats_type == right.GAME) or \
       (left.stats_type == left.GAME and right.stats_type == right.MATCH):
        return VolleyStats.MATCH
    if (left.stats_type == left.MATCH and right.stats_type == right.MATCH):
        return VolleyStats.SEASON

def _calculate_new_final_score(left : VolleyStats, right : VolleyStats) -> Tuple[int, int, int]:
    team_score = 0
    oppo_score = 0

    if (left.stats_type == left.GAME and right.stats_type == right.GAME):
        if left.won:
            team_score += 1
        else:
            oppo_score += 1
        if right.won:
            team_score += 1
        else:
            oppo_score += 1
    if (left.stats_type == left.MATCH and right.stats_type == right.GAME):
        team_score = left.final_team_score
        oppo_score = left.final_oppo_score
        if right.won:
            team_score += 1
        else:
            oppo_score += 1
    if (left.stats_type == left.GAME and right.stats_type == right.MATCH):
        team_score = right.final_team_score
        oppo_score = right.final_oppo_score
        if left.won:
            team_score += 1
        else:
            oppo_score += 1
    if (left.stats_type == left.MATCH and right.stats_type == right.MATCH):
        team_score = left.final_team_score + right.final_team_score
        oppo_score = left.final_oppo_score + right.final_oppo_score

    return (team_score, oppo_score)



# array of backrow stats

# array of front row stats

# all stats per player per position

# game runs
  # player : [total run]


    def print_stats(self) -> None:
        '''prints the volley stats contained in this class'''
