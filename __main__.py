'''Main.py to start processing matches.

'''
import yaml

from volley.volley_match import VolleyMatch, VolleySeason
from volley.volley_player import VolleyRoster

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

## create VolleySeason object
volley_season = VolleySeason(season['league'], season['season'], season['year'], roster)

## add season matches/games
for match in season['matches']:
    if match:
        # create Volleyball Match and add game info
        volley_match = VolleyMatch(match[0]['opponent'])
        for i in range(1, len(match)):
            volley_match.add_game(match[i])
        # add match to the volley season
        volley_season.add_match(volley_match)

volley_season.print_match(0)

# # # TODO: how to correctly parse the holes ?? -- look at match 2

### Define Matches
# games = []



# match1 = VolleyMatch(games)

# match1.calc_match_stats()
# match1.print_player_stats(roster)
