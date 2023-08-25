"""
Module to Generate Volleyball PDF Reports of Game/Match/Season Stats
"""
from typing import List, Dict, Tuple, TypedDict, Optional

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

        msg_str = '----- Name -----'
        msg_str += '| Total | T Det || Serve | Miss  |  Out  | Into | Bad  | Net T  | Errors |'
        msg.append(msg_str)
        msg_str = ' ' * 16
        msg_str += '| Games | Games || Rots. | Serve | Balls | Net  | Pass | (Tot.) | (Tot.) |'
        msg.append(msg_str)
        msg_str = '================'
        msg_str += '+=======+=======++=======+=======+=======+======+======+========+========+'
        msg.append(msg_str)

        for player, stats in match.match_stats.player_stats.items():
            msg_str = f'({str(player).rjust(2)}) {match.roster.get_player_name(player)}'.ljust(16)
            msg_str += '| '  + str(stats.total_games_played).rjust(5) + ' '
            msg_str += '| '  + str(stats.total_detailed_games).rjust(5) + ' '
            msg_str += '|| ' + str(stats.total_serves).rjust(5) + ' '
            msg_str += '| '  + str(stats.missed_serves).rjust(5) + ' '
            msg_str += '| '  + str(stats.out_balls).rjust(5) + ' '
            msg_str += '| '  + str(stats.into_net).rjust(4) + ' '
            msg_str += '| '  + str(stats.bad_pass).rjust(4) + ' '
            msg_str += '| '  + str(stats.net_touches).rjust(6) + ' '
            msg_str += '| '  + str(stats.errors).rjust(6) + ' |'

            msg.append(msg_str)



        return msg
