import json

def create_file():
    file_path = 'players.json'
    list_players = [
                {'nickname':'player1', 'points':'--', 'level':'--'},
                {'nickname':'player2', 'points':'--', 'level':'--'},
                {'nickname':'player3', 'points':'--', 'level':'--'},
                {'nickname':'player4', 'points':'--', 'level':'--'},
                {'nickname':'player5', 'points':'--', 'level':'--'},
                ]

    with open(file_path, 'w') as f:
        players = json.dump(list_players, f)