# Import public modules
from nicegui import app, ui
import pandas as pd
from os.path import isfile

# Reading database 'players'
df_players = pd.read_csv('data/database_players.csv',sep=',')
df_players['WinRate'] = [a for a  in round(df_players['Wins'] / df_players['Games']*100,1)]
df_players['Image'] = ['media/image_' + a + '.png' for a in df_players['Name']]
for i,row in df_players.iterrows():
    if not isfile(row['Image']):
        df_players.at[i,'Image'] = 'media/dummy_player.png'

# Create data and columns properties for table
dat = df_players.to_dict('records')
columns = [
    {'name': 'name',        'label': 'Name',            'field': 'Name',            'sortable': True,   'align': 'left'},
    {'name': 'image',       'label': 'Bild',            'field': 'Image',           'sortable': False,  'align': 'center'},
    {'name': 'games',       'label': 'Spiele',          'field': 'Games',           'sortable': True,   'align': 'center'},
    {'name': 'wins',        'label': 'Siege',           'field': 'Wins',            'sortable': True,   'align': 'center'},
    {'name': 'winrate',     'label': 'Quote / %',       'field': 'WinRate',         'sortable': True,   'align': 'center'},
    {'name': 'elo',         'label': 'Elo Rating',      'field': 'Elo',             'sortable': True,   'align': 'center'},
    {'name': 'series',      'label': 'Siegesserie',     'field': 'WinSeries',       'sortable': True,   'align': 'center'},
    {'name': 'goals',       'label': 'Tore',            'field': 'Goals',           'sortable': True,   'align': 'center'},
    {'name': 'goals_a',     'label': 'Gegentore',       'field': 'GoalsAgainst',    'sortable': True,   'align': 'center'},
    {'name': 'last_game',   'label': 'zuletzt gespielt','field': 'LastGame_Date',   'sortable': True,   'align': 'center'},
]

# Reading database 'games'
df_games = pd.read_csv('data/database_games.csv',sep=',')

# Set colors
ui.colors(primary='rgb(0,60,90)',secondary='rgb(240,240,240)',accent='rgb(255,0,0)')

# Define class for player
class player:
    def __init__(self, name, id, image):
        self.name = name
        self.id = id
        self.image = image

# Initialize players
players = [ player('Spieler 1',1,'media/dummy_player.png'),
            player('Spieler 2',2,'media/dummy_player.png'),
            player('Spieler 3',3,'media/dummy_player.png'),
            player('Spieler 4',4,'media/dummy_player.png')  ]
rematch_players = [ player('Spieler 1',1,'media/dummy_player.png'),
            player('Spieler 2',2,'media/dummy_player.png'),
            player('Spieler 3',3,'media/dummy_player.png'),
            player('Spieler 4',4,'media/dummy_player.png')  ]

def is_valid_players():
    for i in range(0,4):
        if players[i].name == 'Spieler ' + str(i+1):
            ui.notify(f'Bitte wähle Spieler {i+1} aus!')
            return False
    return True

# Define scores
class score:
    def __init__(self, score1, score2):
        self.score1 = 0
        self.score2 = 0

    def is_valid_result(self):
        out = True
        if not self.score1 == 6 and not self.score2 == 6:
            out = False
            ui.notify('Noch steht kein Sieger fest! Eine Mannschaft muss 6 Tore erreichen.')
        elif self.score1 == self.score2:
            out = False
            ui.notify('Hier ist etwas schief gelaufen! Es darf keinen Gleichstand geben.')
        return out

# Initialize scores
scores = score(0,0)

# Function to add a game
def add_game():
    # Check if it is valid to add game
    if is_valid_players() and scores.is_valid_result():
        # DEBUGGING
        print(f"Aktueller Spielstand im Spiel {players[0].name} + {players[1].name} vs. {players[2].name} + {players[3].name}:\n{scores.score1} : {scores.score2}")

        datestr = pd.to_datetime('today').strftime("%y-%m-%d %H:%M")
        
        # Add game to database 'players'
        for i in range(4):
            irow = df_players['ID'] == players[i].id
            df_players.at[df_players[irow].index[0],'Games'] += 1
            df_players.at[df_players[irow].index[0],'LastGame_Date'] = datestr
            if i in [1,2]:
                if scores.score1 > scores.score2:
                    df_players.at[df_players[irow].index[0],'Wins'] += 1
                    df_players.at[df_players[irow].index[0],'WinSeries'] += 1
                else:
                    df_players.at[df_players[irow].index[0],'WinSeries'] = min([0,df_players.at[df_players[irow].index[0],'WinSeries'] - 1])
                df_players.at[df_players[irow].index[0],'Goals'] += scores.score1
                df_players.at[df_players[irow].index[0],'GoalsAgainst'] += scores.score2
            else:
                if scores.score1 > scores.score2:
                    df_players.at[df_players[irow].index[0],'WinSeries'] = min([0,df_players.at[df_players[irow].index[0],'WinSeries'] - 1])
                else:
                    df_players.at[df_players[irow].index[0],'Wins'] += 1
                    df_players.at[df_players[irow].index[0],'WinSeries'] += 1
                df_players.at[df_players[irow].index[0],'Goals'] += scores.score2
                df_players.at[df_players[irow].index[0],'GoalsAgainst'] += scores.score1

        # Save database 'players'
        df_players.to_csv('data/database_players.csv',sep=',',index=False)
        
        # Update table
        from app import table
        table.rows[:] = df_players.to_dict('records')
        table.update()

        # Add game to database 'games'
        df_games.loc[len(df_games)] = [datestr, players[0].name, players[1].name, players[2].name, players[3].name, 'white', 'black', scores.score1, scores.score2]

        # Save database 'games'
        df_games.to_csv('data/database_games.csv',sep=',',index=False)

        # Reset scores
        scores.score1 = 0
        scores.score2 = 0

        # Set rematch players
        for i in range(4):
            if i in [0,1]:
                i_switch = i+2
            elif i in [2,3]:
                i_switch = i-2
            rematch_players[i].name = players[i_switch].name
            rematch_players[i].id = players[i_switch].id
            rematch_players[i].image = players[i_switch].image

        # Reset players
        for i in range(4):
            players[i].name = 'Spieler ' + str(i+1)
            players[i].id = i+1
            players[i].image = 'media/dummy_player.png'

# Function to set up rematch
def set_rematch():
    print('Rematch players: ' + str(rematch_players[1].name) + ' + ' + str(rematch_players[2].name) + ' vs. ' + str(rematch_players[3].name) + ' + ' + str(rematch_players[0].name))
    for i in range(4):
        players[i].name = rematch_players[i].name
        players[i].id = rematch_players[i].id
        players[i].image = rematch_players[i].image