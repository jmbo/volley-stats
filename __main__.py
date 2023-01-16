'''Main.py to start processing matches.

'''
from volley.volley_match import VolleyGame, VolleyMatch
from volley.volley_player import VolleyRoster

import yaml

# print("____menu____")

### Define Players
roster = VolleyRoster()

with open('scores/fall-2022.yaml', 'r') as file:
    season = yaml.safe_load(file)

## add players to roster
for player in season['roster']['females']:
    roster.add_player(player['name'], 'f', player['status'], player['jersey'])
for player in season['roster']['males']:
    roster.add_player(player['name'], 'm', player['status'], player['jersey'])

# # # TODO: create a VolleySeason object to store matches ??
# # # TODO: how to correctly parse the holes ?? -- look at match 2

### Define Matches
games = []



# match1 = VolleyMatch(games)

# match1.calc_match_stats()
# match1.print_player_stats(roster)
