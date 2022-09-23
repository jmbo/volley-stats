'''Main.py to start processing matches.

'''
from volley.volley_match import VolleyGame, VolleyMatch
from volley.volley_player import VolleyRoster

# print("____menu____")

### Define Players
roster = VolleyRoster()

# female players
roster.add_player('Holly'  , 'f', 'full', 00)
roster.add_player('Madysen', 'f', 'full', 25)
roster.add_player('Reba'   , 'f', 'full', 23)
roster.add_player('Rasheda', 'f', 'full', 3)
roster.add_player('Pooja'  , 'f', 'full', 93)

# male players
roster.add_player('Lee'    , 'm', 'full', 29)
roster.add_player('Markus' , 'm', 'full', 38)
roster.add_player('Jose'   , 'm', 'full', 30)
roster.add_player('Ian'    , 'm', 'full', 9)
roster.add_player('Jacob'  , 'm', 'full', 11)
roster.add_player('Reid'   , 'm', 'full', 45)

# subs
roster.add_player('Natalie', 'f', 'sub', 5)
roster.add_player('Paul'   , 'm', 'sub', 44)

### Define Matches
games = []

## Match 1 Games
games.append(VolleyGame({'match': 1,
    'game': 1,
    'full': True,
    'serve': True,
    'lineup': [29, 93, 38, 23, 9, 25],
    'team_scores': ['R', 1, 2, 'R', 3, 'R', 4, 'R', 5, 6, 7, 'R', 8, 9, 'R', 10, 'R', 11, 'R', 12, 13, 14, 'R'], #pylint: disable=line-too-long
    'oppo_scores': [1, 'R', 2, 3, 'R', 4, 5, 6, 7, 8, 'R', 9, 10, 11, 12, 13, 'R', 14, 15, 16, 'R', 17, 18, 19, 'R', 20, 21, 22, 'R', 23, 24, 'R', 25, 'X'] #pylint: disable=line-too-long
}))
games.append(VolleyGame({
    'match': 1,
    'game': 2,
    'full': True,
    'serve': False,
    'lineup': [3, 45, 25, 29, 0, 30],
    'team_scores': [1, 2, 'R', 3, 'R', 4, 5, 6, 'R', 7, 8, 'R', 9, 'R', 10, 'R', 11, 12, 13, 'R', 14, 'R', 15, 16, 'R', 17, 'R'], #pylint: disable=line-too-long
    'oppo_scores': [1, 2, 3, 4, 'R', 5, 'R', 6, 7, 8, 9, 10, 'R', 11, 12, 13, 'R', 14, 'R', 15, 'R', 16, 17, 18, 19, 20, 'R', 21, 'R', 22, 23, 'R', 24, 'R', 25, 'X'] #pylint: disable=line-too-long
}))
games.append(VolleyGame({
    'match': 1,
    'game': 3,
    'full': False,
    'serve': True,
    'lineup': [45, 0, 9, 93, 38, 23],
    'team_scores': ['R', 1, 'R', 2, 'R', 3, 'R', 4, 'R', 5, 'R'], #pylint: disable=line-too-long
    'oppo_scores': [1, 2, 3, 4, 'R', 5, 'R', 6, 'R', 7, 'R', 8, 9, 10, 11, 12, 13, 'R', 14, 15, 'X'] #pylint: disable=line-too-long
}))

## Match 2 Games
# TODO: create a VolleySeason object to store matches ??
# TODO: how to correctly parse the holes ??
games.append(VolleyGame({
    'match': 2,
    'game': 2,
    'full': True,
    'serve': True,
    'lineup': [25, 38, 3, 9, 93, 29],
    'team_scores': [1, 2, 3, 'R', 4, 5, 'R', 6, 7, 8, 'R', 9, 10, 11, 'R', 12, 13, 'R', 14, 15, 16, 17, 18, 19, 'R', 20, 21, 'R', 22, 23, 24, 25, 'X'], #pylint: disable=line-too-long
    'oppo_scores': [1, 'R', 2, 'R', 3, 'R', 4, 5, 6, 'R', 7, 'R', 8, 'R', 9, 10, 'R'] #pylint: disable=line-too-long ## point 8 was a HOLE
}))
games.append(VolleyGame({
    'match': 2,
    'game': 3,
    'full': True,
    'serve': True,
    'lineup': [0, 29, 23, 30, 3, 45],
    'team_scores': [1, 2, 3, 4, 5, 'R', 6, 'R', 7, 8, 9, 'R', 10, 'R', 11, 12, 'R', 13, 'R', 14, 'R', 15, 16, 17, 'R', 18, 'R', 19, 'R', 20, 21, 22, 'R', 23, 24, 25, 'X'], #pylint: disable=line-too-long
    'oppo_scores': ['R', 1, 2, 'R', 3, 'R', 4, 5, 6, 'R', 7, 8, 9, 'R', 10, 'R', 11, 'R', 12, 'R', 13, 'R', 14, 'R', 15, 'R', 16, 'R'] #pylint: disable=line-too-long ## point 10, 16 were a HOLE
}))

match1 = VolleyMatch(games)

match1.calc_match_stats()
match1.print_player_stats(roster)
