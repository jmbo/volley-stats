'''Volleyball Stats module'''
from typing import List, Dict, Union, Tuple

from operator import add

PLUS  = 0
MINUS = 1

# array of backrow stats

# array of front row stats

# all stats per player per position

class PlayerStats():
    ''' Class representing Player Statistics kept throughout kept VolleyStats
    '''
    ROTATION = ['RB', 'RF', 'CF', 'LF', 'LB', 'CB']

    def __init__(self, num : int) -> None:
        self.jersey_num = num

        self.rb_pm = [0, 0]
        self.rf_pm = [0, 0]
        self.cf_pm = [0, 0]
        self.lf_pm = [0, 0]
        self.lb_pm = [0, 0]
        self.cb_pm = [0, 0]
        self._rotation_pm = [self.rb_pm, self.rf_pm, self.cf_pm, self.lf_pm, self.lb_pm, self.cb_pm]

        self.front_row_pm = [0, 0]
        self.back_row_pm  = [0, 0]
        self.pm_stats     = [0, 0]

        self.total_serves  = 0
        self.served_scores : List[int]  = []
        self.serve_runs    : List[int]  = []

        self.total_serve_points : int   = 0
        self.total_games_played : float = 0

        self.points_per_game  : float   = 0
        self.points_per_serve : float   = 0

    def __add__(self, other: "PlayerStats") -> "PlayerStats":

        if self.jersey_num != other.jersey_num:
            msg = f"players don't match: {self.jersey_num} vs. {other.jersey_num}"
            raise Exception(ValueError, msg)

        obj = PlayerStats(self.jersey_num)

        # TODO: try sum instead of add....
        obj.rb_pm = list(map(add, self.rb_pm, other.rb_pm))
        obj.rf_pm = list(map(add, self.rf_pm, other.rf_pm))
        obj.cf_pm = list(map(add, self.cf_pm, other.cf_pm))
        obj.lf_pm = list(map(add, self.lf_pm, other.lf_pm))
        obj.lb_pm = list(map(add, self.lb_pm, other.lb_pm))
        obj.cb_pm = list(map(add, self.cb_pm, other.cb_pm))
        obj._rotation_pm = [obj.rb_pm, obj.rf_pm, obj.cf_pm, obj.lf_pm, obj.lb_pm, obj.cb_pm]

        obj.front_row_pm = list(map(add, self.front_row_pm, other.front_row_pm))
        obj.back_row_pm = list(map(add, self.back_row_pm, other.back_row_pm))
        obj.pm_stats = list(map(add, self.pm_stats, other.pm_stats))

        obj.total_serves = self.total_serves + other.total_serves
        obj.total_serve_points  = self.total_serve_points + other.total_serve_points
        obj.total_games_played  = self.total_games_played + other.total_games_played

        try:
            obj.points_per_game = obj.total_serve_points / obj.total_games_played
            obj.points_per_serve = obj.total_serve_points / obj.total_serves
        except ZeroDivisionError as exc:
            if obj.total_serve_points == 0:
                if obj.total_games_played == 0:
                    obj.points_per_game = 0
                if obj.total_serves == 0:
                    obj.points_per_serve = 0
            else:
                raise exc

        return obj

    def _print_pos_stats(self) -> str:
        ret = ""
        for pm_stat in self._rotation_pm:
            stat = self._normalize(pm_stat)
            ret += f"+{stat[0]:>2}/-{abs(stat[1]):<2} "
        return ret[:-1]

    def _normalize(self, sta: List[int]) -> List[int]:
        return [round((sta[0] / self.pm_stats[0]) * 100), round((sta[1] / self.pm_stats[1]) * 100)]

    def add_points_to_rotation(self, rotation : str, points : int) -> None:
        '''Function adds the number of points specified to the plus minus statistics of the given
        player's rotation.

        If points are positive, stats are assumed to be PLUS, else stats are assume to be MINUS.
        '''
        side = PLUS
        if points < 0:
            side = MINUS

        self._rotation_pm[self.ROTATION.index(rotation)][side] += points

        if rotation in (self.ROTATION[0], self.ROTATION[4], self.ROTATION[5]):
            self.back_row_pm[side]  += points

        if rotation in (self.ROTATION[1], self.ROTATION[2], self.ROTATION[3]):
            self.front_row_pm[side] += points

        self.pm_stats[side] += points


class VolleyStats():
    ''' Class representing all Volleyball Statistics kept for games and/or matches.
    '''

    HALF_GAME = 0.6

    GAME        = 0
    MATCH       = 1
    SEASON      = 2
    ALL_TIME    = 3

    def __init__(self, lineup : Union[List[int], None] = None) -> None:
        self.back_row_stats  : Dict[Tuple[int, int, int], List[int]] = {}
        self.front_row_stats : Dict[Tuple[int, int, int], List[int]] = {}
        self.player_stats : Dict[int, PlayerStats]   = {}

        self.final_team_score = 0
        self.final_oppo_score = 0
        self.won = False

        self.stats_type = VolleyStats.GAME
        self.valid      = False

        if lineup:
            for num in lineup:
                self.player_stats[num] = PlayerStats(num)

    def __add__(self, other: "VolleyStats") -> "VolleyStats":
        obj = VolleyStats()

        # if both VolleyStats objects are NULL, return a NULL object
        if not self.valid and not other.valid:
            return obj

        # calculate type of result
        obj.stats_type = _calculate_new_stats_type(self, other)
        # calculate final team score
        obj.final_team_score, obj.final_oppo_score = _calculate_new_final_score(self, other)

        # ‼ Defining WINS equal to more WINS than LOSSES in games, matches, seasons
        if obj.final_team_score > obj.final_oppo_score:
            obj.won = True

        # combine the stats of players across multiple games
        for num in set(list(self.player_stats.keys()) + list(other.player_stats.keys())):
            obj.player_stats[num] = self.player_stats.get(num, PlayerStats(num)) \
                                  + other.player_stats.get(num, PlayerStats(num))

        obj.valid = True

        return obj

    # def __iadd__(self, other: "VolleyStats") -> "VolleyStats":
    #     return self.__add__(other)

    def __str__(self) -> str:
        return _print_stats(self)

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
            for i, jersey_num in enumerate(rotation):
                self.player_stats[jersey_num].add_points_to_rotation(PlayerStats.ROTATION[i], 1)
            rotation = rotation[1:] + rotation[:1]
            scores.pop(0)
            score -= 1

        for i, jersey_num in enumerate(rotation):
            self.player_stats[jersey_num].add_points_to_rotation(PlayerStats.ROTATION[i], score)

        # assign serving stats to server position when processing positive (team) scores
        if p_m == PLUS:
            self.player_stats[rotation[0]].served_scores += scores
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

            try:
                player.points_per_game = player.total_serve_points / player.total_games_played
                player.points_per_serve = player.total_serve_points / player.total_serves
            except ZeroDivisionError as exc:
                if player.total_serve_points == 0:
                    if player.total_games_played == 0:
                        player.points_per_game = 0
                    if player.total_serves == 0:
                        player.points_per_serve = 0
                else:
                    raise exc
        # validate these stats
        self.valid = True

    def print_stats(self) -> None:
        """Function prints the provided Match's Statistics."""
        print(_print_stats(self))

def _calculate_new_stats_type(left : VolleyStats, right : VolleyStats) -> int:
    if (left.stats_type == left.GAME and right.stats_type == right.GAME) or \
       (left.stats_type == left.MATCH and right.stats_type == right.GAME) or \
       (left.stats_type == left.GAME and right.stats_type == right.MATCH):
        return VolleyStats.MATCH
    if (left.stats_type == left.MATCH and right.stats_type == right.MATCH):
        return VolleyStats.SEASON

    return VolleyStats.ALL_TIME

def _calculate_new_final_score(left : VolleyStats, right : VolleyStats) -> Tuple[int, int]:
    team_score = 0
    oppo_score = 0

    # TODO: BUG: if one of the games is the "NULL" stats, it will add a count to the oppo score
    # since won is false by default
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

def _print_stats(self: VolleyStats) -> str:
            # game = self.games[0]
        # for key in game.stats.keys():
        #     name = roster.get_player_name(key)
        #     print(f'({key:02d}) {name} {" "*(8-len(name))} => ', game.stats[key])

    msg = ''
    msg += " Name ".center(16, '-')     + " =>"  # 16
    msg += " Total Games "                + "|"   # 11
    msg += " Serve Rotations "            + "|"   # 15
    msg += " +/- Stats "                  + "|"   # 9
    msg += " % (Normalized) ".center(49)  + "|"   # 48
    msg += " % (Normalized) ".center(19)  + "|"   # 9
      #    "BR".center(8),         "|",  # 9
    msg += " Pts/Serve "                  + "|"   # 9
    msg += " Pts/Game "                   + "|\n" # 8

    msg += f"{' ':>17}  {' ':>13}|{' ':>17}|{' ':>11}|"
    msg += "   RB      RF      CF      LF      LB      CB    |"
    msg += "BR".center(9) + "|" +  "FR".center(9) + "|"
    msg += f"{' ':>11}|{' ':10}|\n"

    # sort dictionary by ppg
    # stats = dict(sorted(self.match_stats.items(), key=lambda x:x[1]['ppg'], reverse=True))
    stats = dict(sorted(self.player_stats.items(), key=lambda x:x[1].points_per_game, reverse=True))

    for item in stats.items():
        num = item[0]
        player = item[1]
        # name = roster.get_player_name(num)
        name = ''

        msg += f"({num:02d}) {name}".ljust(16, ' ')                                     + " => "
        msg += f"{player.total_games_played:11.1f}"                                     + " | "
        msg += f"{player.total_serves:>15}"                                             + " | "
        msg += f"+{player.pm_stats[0]:>3}/-{abs(player.pm_stats[1]):<3}"                + " | "
        #   f"{player['pos_stats']}",                                             "|",
        msg += f"{player._print_pos_stats()}"                                           + " | "
        stat = player._normalize(player.back_row_pm)
        msg += f"+{stat[0]:>2}/-{abs(stat[1]):<2}"                                      + " | "
        stat = player._normalize(player.front_row_pm)
        msg += f"+{stat[0]:>2}/-{abs(stat[1]):<2}"                                      + " | "
        msg += f"{player.points_per_serve:9.2f}"                                        + " | "
        msg += f"{player.points_per_game:8.2f}"                                         + " | "
        msg += "\n"

    return msg