'''Main.py to start processing matches.

'''
from volley.volley_match import VolleyMatch
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

game1_1 = ['fs', 29, 93, 38, 23, 9, 25]
score1_1 = ['R', 1, 2, 'R', 3, 'R', 4, 'R', 5, 6, 7, 'R', 8, 9, 'R', 10, 'R', 11, 'R', 12, 13, 14, \
            'R']
game1_2 = ['fr', 3, 45, 25, 29, 0, 30]
score1_2 = [1, 2, 'R', 3, 'R', 4, 5, 6, 'R', 7, 8, 'R', 9, 'R', 10, 'R', 11, 12, 13, 'R', 14, 'R', \
            15, 16, 'R', 17, 'R']
game1_3 = ['hs', 45, 0, 9, 93, 38, 23]
score1_3 = ['R', 1, 'R', 2, 'R', 3, 'R', 4, 'R', 5, 'R']

games.append([game1_1, score1_1])
games.append([game1_2, score1_2])

match1 = VolleyMatch(games)
match1.add_game([game1_3, score1_3])

match1.calc_match_stats()
match1.print_player_stats(roster)
