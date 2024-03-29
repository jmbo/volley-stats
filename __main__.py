'''Main.py to start processing matches.

'''
import yaml

from volley.volley_match import VolleyMatch, VolleySeason
from volley.volley_player import VolleyRoster
# from volley.volley_report import VolleyReportPDF, VolleyReportText
from volley.volley_report import VolleyReportText

# print("____menu____")
volley_seasons = []

#### *************** IMPORT COED FALL 2022 **************** ####
### Define Players
roster = VolleyRoster()

with open('scores/coed-fa22.yaml', 'r') as file:
    season = yaml.safe_load(file)

## add players to roster
for player in season['roster']['females']:
    roster.add_player(player['name'], 'f', player['status'], player['jersey'])
for player in season['roster']['males']:
    roster.add_player(player['name'], 'm', player['status'], player['jersey'])

## create VolleySeason object
volley_seasons.append(VolleySeason(season['league'], season['season'], season['year'], roster))

## add season matches/games
for match in season['matches']:
    if match:
        # create Volleyball Match and add game info
        volley_match = VolleyMatch(match[0]['opponent'], roster)
        for i in range(1, len(match)):
            volley_match.add_game(match[i])
        # add match to the volley season
        volley_seasons[-1].add_match(volley_match)

#### *************** IMPORT COED WINTER 2023 **************** ####
### Define Players
roster = VolleyRoster()

with open('scores/coed-wn23.yaml', 'r') as file:
    season = yaml.safe_load(file)

## add players to roster
for player in season['roster']['females']:
    roster.add_player(player['name'], 'f', player['status'], player['jersey'])
for player in season['roster']['males']:
    roster.add_player(player['name'], 'm', player['status'], player['jersey'])

## create VolleySeason object
volley_seasons.append(VolleySeason(season['league'], season['season'], season['year'], roster))

## add season matches/games
for match in season['matches']:
    if match:
        # create Volleyball Match and add game info
        volley_match = VolleyMatch(match[0]['opponent'], roster)
        for i in range(1, len(match)):
            volley_match.add_game(match[i])
        # add match to the volley season
        volley_seasons[-1].add_match(volley_match)

#### *************** IMPORT COED WINTER 2023 **************** ####
### Define Players
roster = VolleyRoster()

with open('scores/mens-wn23.yaml', 'r') as file:
    season = yaml.safe_load(file)

## add players to roster
for player in season['roster']['players']:
    roster.add_player(player['name'], 'x', player['status'], player['jersey'])

## create VolleySeason object
volley_seasons.append(VolleySeason(season['league'], season['season'], season['year'], roster))

## add season matches/games
for match in season['matches']:
    if match:
        # create Volleyball Match and add game info
        volley_match = VolleyMatch(match[0]['opponent'], roster)
        for i in range(1, len(match)):
            volley_match.add_game(match[i])
        # add match to the volley season
        volley_seasons[-1].add_match(volley_match)

#### *************** IMPORT FINISHED **************** ####

# volley_season.print_match(0)
# print(volley_seasons[0])
# print(volley_seasons[1])
# print(volley_seasons[2])

# report = VolleyReportPDF()
# report.add_match()

txt_report = VolleyReportText()
print(txt_report.add_match(volley_seasons[2].matches[0]))


# # # TODO: how to correctly parse the holes ?? -- look at match 2

### Define Matches
# games = []



# match1 = VolleyMatch(games)

# match1.calc_match_stats()
# match1.print_player_stats(roster)
