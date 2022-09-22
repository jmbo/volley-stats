'''Volleyball Roster module'''

class VolleyRoster(object):
    '''Class representing the volleyball roster.

    '''
    def __init__(self) -> "VolleyRoster":
        self.players = []

    def add_player(self, name : str, gender : str, status : str, number : str) -> None:
        '''Adds a volleyball player to the roster.
        '''
        self.players.append(VolleyPlayer(name, gender, status, number))

    def get_player_name(self, number : int) -> str:
        '''Finds a player's name from their jersey number.
        '''
        for player in self.players:
            if player.number == number:
                return player.name

        return None


class VolleyPlayer(object):
    '''Class representing a volleyball player keeping stats and records.

    '''

    def __init__(self, name : str, gender : str, status : str, number : str) -> None:
        self.name = name
        self.gender = gender
        self.status = status
        self.number = number
