# Import public modules
from nicegui import app, ui
import pandas as pd
from os.path import isfile, isdir
from os import listdir, remove, mkdir
from shutil import copyfile
from pathlib import Path
homepath = str(Path.home())

# Create backup of database 'players' and 'games'
## Debugging: 
# 1. set path_backup to e.g. your local documents folder
# 2. copy the CURRENT database_players.csv and database_games.csv to your data/ folder

path_backup = homepath + '/kicker-app_backup'
# Check if backup folder exists
if not isdir(path_backup):
    mkdir(path_backup)

if not path_backup == '':
    copyfile('data/database_players.csv',path_backup + '/database_players_' + pd.to_datetime('today').strftime("%y-%m-%d_%H.%M") + '.csv')
    copyfile('data/database_games.csv',path_backup + '/database_games_' + pd.to_datetime('today').strftime("%y-%m-%d_%H.%M") + '.csv')


# Reading database 'players'
df_players = pd.read_csv('data/database_players.csv',sep=',')
df_players['WinRate'] = [a for a  in round(df_players['Wins'] / df_players['Games']*100,1)]
df_players['Image'] = ['media/image_' + a + '.png' for a in df_players['Name']]
for i,row in df_players.iterrows():
    if not isfile(row['Image']):
        df_players.at[i,'Image'] = 'media/dummy_player.png'
df_players.set_index('Name',inplace=True,drop=False)

# Create data and columns properties for table
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

# Remove all files from tmp folder
def clear_tmp():
    list = listdir('media/tmp/')
    for f in list:
        remove('media/tmp/' + f)
clear_tmp()

# Define class for player
class player:
    def __init__(self, name, image):
        self.name = name
        self.image = image

# Initialize players
players = [ player('Spieler 1','media/dummy_player.png'),
            player('Spieler 2','media/dummy_player.png'),
            player('Spieler 3','media/dummy_player.png'),
            player('Spieler 4','media/dummy_player.png')  ]
rematch_players = [ player('Spieler 1','media/dummy_player.png'),
            player('Spieler 2','media/dummy_player.png'),
            player('Spieler 3','media/dummy_player.png'),
            player('Spieler 4','media/dummy_player.png')  ]

def is_valid_players():
    for i in range(0,4):
        if players[i].name == 'Spieler ' + str(i+1):
            ui.notify(f'Bitte wähle Spieler {i+1} aus!', type='negative')
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
            ui.notify('Noch steht kein Sieger fest! Eine Mannschaft muss 6 Tore erreichen.', type='negative')
        elif self.score1 == self.score2:
            out = False
            ui.notify('Hier ist etwas schief gelaufen! Es darf keinen Gleichstand geben.', type='negative')
        return out

# Initialize scores
scores = score(0,0)

# Function to add a game
def add_game():
    # Check if it is valid to add game
    if is_valid_players() and scores.is_valid_result():
        datestr = pd.to_datetime('today').strftime("%y-%m-%d %H:%M")

        # Add game to database 'players'
        for i in range(4):
            id = players[i].name
            df_players.at[id,'Games'] += 1
            df_players.at[id,'LastGame_Date'] = datestr

            if i in [0,1]:
                if scores.score1 > scores.score2:
                    df_players.at[id,'Wins'] += 1
                    df_players.at[id,'WinSeries'] = max([1,df_players.at[id,'WinSeries'] + 1])
                else:
                    df_players.at[id,'WinSeries'] = min([-1,df_players.at[id,'WinSeries'] - 1])
                df_players.at[id,'Goals'] += scores.score1
                df_players.at[id,'GoalsAgainst'] += scores.score2
            else:
                if scores.score1 > scores.score2:
                    df_players.at[id,'WinSeries'] = min([-1,df_players.at[id,'WinSeries'] - 1])
                else:
                    df_players.at[id,'Wins'] += 1
                    df_players.at[id,'WinSeries'] = max([1,df_players.at[id,'WinSeries'] + 1])
                df_players.at[id,'Goals'] += scores.score2
                df_players.at[id,'GoalsAgainst'] += scores.score1

            # Update WinRate
            df_players.at[id,'WinRate'] = round(df_players.at[id,'Wins'] / df_players.at[id,'Games']*100,1)

        # Update ELO scores
        update_elo(df_players,[p.name for p in players],scores.score1,scores.score2)

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
            rematch_players[i].image = players[i_switch].image

        # Reset players
        for i in range(4):
            players[i].name = 'Spieler ' + str(i+1)
            players[i].image = 'media/dummy_player.png'

# Function to set up rematch
def set_rematch():
    for i in range(4):
        players[i].name = rematch_players[i].name
        players[i].image = rematch_players[i].image

# Function to calculate ELO scores for 2 vs 2
# https://towardsdatascience.com/developing-an-elo-based-data-driven-ranking-system-for-2v2-multiplayer-games-7689f7d42a53
def update_elo(df,ids,s1,s2):
    # Set parameter
    R_old = [df.at[id,'Elo'] for id in ids]
    K = []
    for id in ids:
        K.append(40)
    P = 1 + abs(s1-s2)/6

    # Calculate winning probability for each team
    Eps,Ets = calc_win_prob(R_old)

    # Calculate new ELO scores for each player
    for (i,id) in enumerate(ids):
        if id in [ids[0],ids[1]]:
            if s1 > s2:
                S = 1  
                df.at[id,'Elo'] += (1-(R_old[i]/(R_old[0]+R_old[1]))) *  K[i] * P * (S - Ets[0])
            else:
                S = 0
                df.at[id,'Elo'] += (R_old[i]/(R_old[0]+R_old[1])) *  K[i] * P * (S - Ets[0])
        else:
            if s2 > s1:
                S = 1  
                df.at[id,'Elo'] += (1-(R_old[i]/(R_old[2]+R_old[3]))) *  K[i] * P * (S - Ets[1])
            else:
                S = 0
                df.at[id,'Elo'] += (R_old[i]/(R_old[2]+R_old[3])) *  K[i] * P * (S - Ets[1])
        
        df.at[id,'Elo'] = round(df.at[id,'Elo'],1) 

    return 0

# Function to calculate Winning probability from ELO scores
def calc_win_prob(Rall):
    # Set parameter
    D = 500

    # Calculate winning probability for each player
    Rp1,Rp2,Rp3,Rp4 = Rall
    Ep1 = (1 / (1 + 10**((Rp3 - Rp1)/D)) + 1 / (1 + 10**((Rp4 - Rp1)/D))) / 2
    Ep2 = (1 / (1 + 10**((Rp3 - Rp2)/D)) + 1 / (1 + 10**((Rp4 - Rp2)/D))) / 2
    Ep3 = (1 / (1 + 10**((Rp1 - Rp3)/D)) + 1 / (1 + 10**((Rp2 - Rp3)/D))) / 2
    Ep4 = (1 / (1 + 10**((Rp1 - Rp4)/D)) + 1 / (1 + 10**((Rp2 - Rp4)/D))) / 2

    # Calculate winning probability for each team
    Et1 = (Ep1 + Ep2) / 2
    Et2 = (Ep3 + Ep4) / 2

    return (Ep1,Ep2,Ep3,Ep4),(Et1,Et2)

