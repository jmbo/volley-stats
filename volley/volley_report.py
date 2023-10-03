"""
Module to Generate Volleyball PDF Reports of Game/Match/Season Stats
"""
from typing import List, Dict, Tuple, TypedDict, Optional
import tabulate

# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import landscape, letter
# from reportlab.lib.units import mm, inch

from .volley_match import VolleyMatch, VolleyGame
from .volley_player import VolleyRoster

# class VolleyReportPDF():
#     """Class Generates a PDF Report of Desired Stats"""

#     # pdfmetrics.registerFont( TTFont('consolas', 'Consola.ttf'))

#     def __init__(self):
#         file_name = "volleyball_output.pdf"

#         self.pdf = canvas.Canvas(file_name, pagesize=letter)
#         self.pdf.setFont('Courier-Bold', 16)

#         self.pdf.showPage()

#     def add_match(self) -> None:
#         """Prints Match Statistics to PDF Report"""
#         width, height = letter
#         # create new page
#         self.pdf.setPageSize(letter)
#         self.pdf.setFont('Courier', 12)

#         self.pdf.line(0.5*inch, 10.5*inch, 8*inch, 10.5*inch)

#         self.pdf.line(0.5*inch, 9.5*inch, 8*inch, 9.5*inch)

#         self.pdf.showPage()

#         self.pdf.save()

class VolleyReportText():
    """Class Generates a Text Report of Desired Stats"""

    WIDTH  = 90
    HEIGHT = 56
    NAME_W = 7

    def __init__(self) -> None:
        file_name = "volleyball_output.pdf"

    def add_match(self, match : VolleyMatch) -> str:
        """Creates Match Stats Message."""
        match_num = match.match_num
        match_opp = match.opponent['name']

        msg = []
        msg.append('*' * self.WIDTH)
        msg.append(f'MATCH {match_num} STATS -- OPPONENT: {match_opp}'.center(self.WIDTH))
        msg.append('*' * self.WIDTH)

        lineups = []
        for game in match.games:
            lineups.append(game.lineup)

        msg += self._create_game_lineups(lineups, match.roster)
        msg.append('')
        msg += self._create_game_scores(match.games)
        msg.append('')

        msg += self._create_stats1(match)
        msg.append('')
        msg += self._create_stats2(match)
        msg.append('')
        msg += self._create_stats3(match)
        msg.append('')

        return '\n'.join(msg)

    def _create_game_lineups(self, lineups : List[List[int]], roster : VolleyRoster) -> List[str]:
        msg = []
        msg.append(('   '  + '-'*10 + ' NET ' + '-'*10 + '  ') * 3)
        msg.append(('   _' + ' '*23 + '_  ') * 3)

        line = ''
        for lineup in lineups:
            line += '  | '
            line += f'{roster.get_player_name(lineup[1])[:self.NAME_W].center(self.NAME_W)} '
            line += f'{roster.get_player_name(lineup[2])[:self.NAME_W].center(self.NAME_W)} '
            line += f'{roster.get_player_name(lineup[3])[:self.NAME_W].center(self.NAME_W)} | '
        msg.append(line)

        msg.append(('  | ' + ' '*23 + ' | ') * 3)

        line = ''
        for lineup in lineups:
            line += '  |_'
            line += f'{roster.get_player_name(lineup[4])[:self.NAME_W].center(self.NAME_W)} '
            line += f'{roster.get_player_name(lineup[5])[:self.NAME_W].center(self.NAME_W)} '
            line += f'{roster.get_player_name(lineup[0])[:self.NAME_W].center(self.NAME_W)}_| '
        msg.append(line)

        return msg

    def _create_game_scores(self, games : List[VolleyGame]) -> List[str]:
        msg = []

        msg_str =  'GAME 1'.center(int(self.WIDTH / 3))
        msg_str += 'GAME 2'.center(int(self.WIDTH / 3))
        msg_str += 'GAME 3'.center(int(self.WIDTH / 3))
        msg.append(msg_str)

        msg_str = ''
        for game in games:
            stats = game.game_stats
            if stats.won:
                score_str = f'W: {stats.final_team_score} - {stats.final_oppo_score}'
                msg_str += score_str.center(int(self.WIDTH / 3))
            else:
                score_str = f'L: {stats.final_team_score} - {stats.final_oppo_score}'
                msg_str += score_str.center(int(self.WIDTH / 3))
        msg.append(msg_str)

        return msg

    def _create_game_serve_runs(self, games : List[VolleyGame]) -> List[str]:
        msg = ['Serve Runs:']
        return msg

    def _create_stats1(self, match : VolleyMatch) -> List[str]:
        msg = []

        tabulate.MIN_PADDING = 0
        headers = ['Name', 'Total Games', 'T Det Games', 'Serve Rots.', 'Miss Serve', 'Out Balls',
                   'Into Net', 'Bad Pass', 'Net T (Tot.)', 'Errors (Tot.)']
        widths = [14, 5, 5, 5, 5, 5, 4, 4, 6, 6]
        align  = ["left"] + ["right"] * 9
        data   = []

        for player, stats in match.match_stats.player_stats.items():
            fmt = [f'({str(player).rjust(2)}) {match.roster.get_player_name(player)}']
            fmt.append(stats.total_games_played)
            fmt.append(stats.total_detailed_games)
            fmt.append(stats.total_serves)
            fmt.append(stats.missed_serves)
            fmt.append(stats.out_balls)
            fmt.append(stats.into_net)
            fmt.append(stats.bad_pass)
            fmt.append(stats.net_touches)
            fmt.append(stats.errors)

            data.append(fmt)

        # "pretty"
        # "fancy_grid"
        msg = tabulate.tabulate(data, headers=headers, tablefmt="fancy_grid",
                       maxcolwidths=widths, maxheadercolwidths=widths, colalign=align
                       ).split('\n')

        return msg

    def _create_stats2(self, match : VolleyMatch) -> List[str]:
        msg = []

        tabulate.MIN_PADDING = 0
        headers = ['Name', 'Total Games', 'Serve Rots.', 'Unret Serv', 'Recov', 'Pts/ Serve',
                   'Pts/ Game', '+/- Stats']
        widths = [14, 5, 5, 5, 5, 5, 4, 7]
        align  = ["left"] + ["right"] * 6 + ["center"]
        data   = []

        for player, stats in match.match_stats.player_stats.items():
            fmt = [f'({str(player).rjust(2)}) {match.roster.get_player_name(player)}']
            fmt.append(stats.total_games_played)
            # fmt.append(stats.total_detailed_games)
            fmt.append(stats.total_serves)
            fmt.append(stats.unreturned_serves)
            fmt.append(stats.recoveries)
            fmt.append(stats.points_per_serve)
            fmt.append(stats.points_per_game)
            fmt.append(f'+{stats.pm_stats[0]:2}/{stats.pm_stats[1]:2}')

            data.append(fmt)

        # "pretty"
        # "fancy_grid"
        # "presto"
        msg = tabulate.tabulate(data, headers=headers, tablefmt="presto",
                       maxcolwidths=widths, maxheadercolwidths=widths, colalign=align,
                       floatfmt='.2f'
                       ).split('\n')
        return msg

    def _create_stats3(self, match : VolleyMatch) -> List[str]:
        msg = []

        tabulate.MIN_PADDING = 0
        headers = ['Name', '% (Normalized)\n   RB      RF      CF      LF      LB      CB    ',
                   '% (Normalized)\n    BR   |    FR   ']
        align  = ["left"] + ["center"] * 2
        data   = []

        for player, stats in match.match_stats.player_stats.items():
            fmt = [f'({str(player).rjust(2)}) {match.roster.get_player_name(player)}']
            fmt.append(stats.rb_pm)
            fmt.append(stats.front_row_pm)

            data.append(fmt)

        # "pretty"
        # "fancy_grid"
        msg = tabulate.tabulate(data, headers, tablefmt="presto", colalign=align).split('\n')

        return msg
