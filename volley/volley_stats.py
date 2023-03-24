'''Volleyball Stats module'''
from typing import List, Dict, Union, Tuple

from operator import add

PLUS  = 0
MINUS = 1

class PlayerStats():
    ''' Class representing Player Statistics kept throughout kept VolleyStats
    '''
    ROTATION = ['RB', 'RF', 'CF', 'LF', 'LB', 'CB']

    def __init__(self, num) -> None:
        self.jersey_num = num

        self.rb_pm = self.rf_pm = self.cf_pm = [0, 0]
        self.lf_pm = self.lb_pm = self.cb_pm = [0, 0]

        self.front_row_pm = self.back_row_pm = self.pm_stats = [0, 0]

        self.total_serves  = 0
        self.served_scores = []
        self.serve_runs    = []

        self.total_serve_points = 0
        self.total_games_played = 0

    def __add__(self, other: "PlayerStats") -> "PlayerStats":

        # TODO: might need to check if None values present

        if self.jersey_num != other.jersey_num:
            msg = f"players don't match: {self.jersey_num} vs. {other.jersey_num}"
            raise Exception(ValueError, msg)

        obj = PlayerStats(self.jersey_num)

        obj.rb_pm = list(map(add, self.rb_pm, other.rb_pm))
        obj.rf_pm = list(map(add, self.rf_pm, other.rf_pm))
        obj.cf_pm = list(map(add, self.cf_pm, other.cf_pm))
        obj.lf_pm = list(map(add, self.lf_pm, other.lf_pm))
        obj.lb_pm = list(map(add, self.lb_pm, other.lb_pm))
        obj.cb_pm = list(map(add, self.cb_pm, other.cb_pm))

        obj.front_row_pm = list(map(add, self.front_row_pm, other.front_row_pm))
        obj.back_row_pm = list(map(add, self.back_row_pm, other.back_row_pm))
        obj.pm_stats = list(map(add, self.pm_stats, other.pm_stats))

        obj.total_serves = self.total_serves + other.total_serves
        obj.total_serve_points  = self.total_serve_points + other.total_serve_points
        obj.total_games_played  = self.total_games_played + other.total_games_played

    def add_points_to_rotation(self, rotation : str, points : int) -> None:
        '''Function adds the number of points specified to the plus minus statistics of the given
        player's rotation.

        If points are positive, stats are assumed to be PLUS, else stats are assume to be MINUS.
        '''
        side = PLUS
        if points < 0:
            side = MINUS

        if rotation == self.ROTATION[0]:
            self.rb_pm[side]        += points
            self.back_row_pm[side]  += points
        if rotation == self.ROTATION[1]:
            self.rf_pm[side]        += points
            self.front_row_pm[side] += points
        if rotation == self.ROTATION[2]:
            self.cf_pm[side]        += points
            self.front_row_pm[side] += points
        if rotation == self.ROTATION[3]:
            self.lf_pm[side]        += points
            self.front_row_pm[side] += points
        if rotation == self.ROTATION[4]:
            self.lb_pm[side]        += points
            self.back_row_pm[side]  += points
        if rotation == self.ROTATION[5]:
            self.cb_pm[side]        += points
            self.back_row_pm[side]  += points

        self.pm_stats[side] += points


class VolleyStats():
    ''' Class representing all Volleyball Statistics kept for games and/or matches.
    '''

    HALF_GAME = 0.6

    GAME        = 0
    MATCH       = 1
    SEASON      = 2
    ALL_TIME    = 3

    def __init__(self, lineup : List[int] = None) -> None:
        self.back_row_stats  = {}
        self.front_row_stats = {}
        self.player_stats : Dict[int, PlayerStats]   = {}

        self.final_team_score = 0
        self.final_oppo_score = 0
        self.won = False

        self.stats_type = VolleyStats.GAME

        for num in lineup:
            # [RB, RF, CF, LF, LB, CB]
            # self.player_stats[num] = {'RB': [0, 0], 'RF': [0, 0], 'CF': [0, 0],
            #                           'LF': [0, 0], 'LB': [0, 0], 'CB': [0, 0],
            #                           'front_row': [0, 0], 'back_row': [0, 0], 'pm_stats': [0, 0],
            #                           'serve_runs': [], 'total_serves': 0, 'served_scores': [],
            #                           'total_serve_points': 0, 'games': 0,}
            self.player_stats[num] = PlayerStats(num)

    def __add__(self, other: "VolleyStats") -> "VolleyStats":
        obj = VolleyStats()

        # calculate type of result
        obj.stats_type = _calculate_new_stats_type(self, other)
        # calculate final team score
        obj.final_team_score, obj.final_oppo_score = _calculate_new_final_score(self, other)

        # ‼ Defining WINS equal to more WINS than LOSSES in games, matches, seasons
        if obj.final_team_score > obj.final_oppo_score:
            obj.won = True

        # combine the stats of players across multiple games
        for num in set(self.player_stats.keys() + other.player_stats.keys()):
            obj.player_stats[num] = self.player_stats.get(num) + other.player_stats.get(num)

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

        if p_m == MINUS:
            score *= -1

        # TODO: process backrow/frontrow tuples

        # if processing positive (team) scores, every first point we gain on the return is part of
        # the old rotation, we then rotate and all points followed are from successful serves
        # the only exception is at the beginning of the game if the team starts by serving, then all
        # points gained before the return are from successful serves
        if p_m == PLUS and not beg:
            rotation = rotation[-1:] + rotation[:-1]
            for i, _ in enumerate(PlayerStats.ROTATION):
                self.player_stats[rotation[i]].add_points_to_rotation(i, 1)
            rotation = rotation[1:] + rotation[:1]
            scores.pop(0)
            score -= 1

        for i, _ in enumerate(PlayerStats.ROTATION):
            self.player_stats[rotation[i]].add_points_to_rotation(i, score)

        # assign serving stats to server position when processing positive (team) scores
        if p_m == PLUS:
            self.player_stats[rotation[0]].served_scores.append(scores)
            self.player_stats[rotation[0]].serve_runs.append(score)
            self.player_stats[rotation[0]].total_serves += 1

    def finish_game(self, full : bool) -> None:
        '''At the end of each game calculate remaining stats for each player after all points are
         attributed. '''
        for player in self.player_stats.values():
            player.total_serve_points = len(player.served_scores)

            if full:
                player.total_games_played += 1
            else:
                player.total_games_played += self.HALF_GAME

def _calculate_new_stats_type(left : VolleyStats, right : VolleyStats) -> int:
    if (left.stats_type == left.GAME and right.stats_type == right.GAME) or \
       (left.stats_type == left.MATCH and right.stats_type == right.GAME) or \
       (left.stats_type == left.GAME and right.stats_type == right.MATCH):
        return VolleyStats.MATCH
    if (left.stats_type == left.MATCH and right.stats_type == right.MATCH):
        return VolleyStats.SEASON

    return VolleyStats.ALL_TIME

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


    # def print_stats(self) -> None:
    #     '''prints the volley stats contained in this class'''
