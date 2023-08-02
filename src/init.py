# Import public modules
from nicegui import app, ui
import pandas as pd
from os.path import isfile

# Loading
df = pd.read_csv('data/data-kicker-app.txt',sep='\t')
df['Quote'] = [a for a  in round(df['Wins'] / df['Games']*100,1)]
df['image'] = ['media/image_' + a + '.png' for a in df['Name']]
for i,row in df.iterrows():
    if not isfile(row['image']):
        df.at[i,'image'] = 'media/dummy_player.png'

dat = df.to_dict('records')
columns = [
    {'name': 'name',        'label': 'Name',            'field': 'Name',            'sortable': True,   'align': 'left'},
    {'name': 'image',       'label': 'Bild',            'field': 'image',           'sortable': False,  'align': 'center'},
    {'name': 'games',       'label': 'Spiele',          'field': 'Games',           'sortable': True,   'align': 'center'},
    {'name': 'wins',        'label': 'Siege',           'field': 'Wins',            'sortable': True,   'align': 'center'},
    {'name': 'quote',       'label': 'Quote / %',       'field': 'Quote',           'sortable': True,   'align': 'center'},
    {'name': 'goals',       'label': 'Tore',            'field': 'Tore',            'sortable': True,   'align': 'center'},
    {'name': 'goals_a',     'label': 'Gegentore',       'field': 'ggTore',          'sortable': True,   'align': 'center'},
    {'name': 'last_game',   'label': 'zuletzt gespielt','field': 'zuletztGespielt', 'sortable': True,   'align': 'center'},
]

ui.colors(primary='rgb(0,60,90)',secondary='rgb(240,240,240)',accent='rgb(255,0,0)')

class player:
    def __init__(self, name, id, image):
        self.name = name
        self.id = id
        self.image = image
        self.text = name

players = [ player('Spieler 1',1,'media/dummy_player.png'),
            player('Spieler 2',2,'media/dummy_player.png'),
            player('Spieler 3',3,'media/dummy_player.png'),
            player('Spieler 4',4,'media/dummy_player.png')  ]

# Dialog > move to new file

# Define function to create lambda function
def make_lambda(i):
    return lambda: dialog_players.submit(i)

# Dialog to choose player
with ui.dialog() as dialog_players, ui.card().props('bordered horizontal').style('max-width:300vh'):
    with ui.grid(columns=9).style('width:100vh'):
        for i,row in df.iterrows():
            with ui.image(row['image']).on('click',make_lambda(i)).style('width:100%'):
                ui.label(row['Name']).classes('absolute-bottom text-subtitle2 text-center no-margin')

# Choose player function
async def choose_player_1():
    out = await dialog_players
    choose_player(0,out)

async def choose_player_2():
    out = await dialog_players
    choose_player(1,out)

async def choose_player_3():
    out = await dialog_players
    choose_player(2,out)

async def choose_player_4():
    out = await dialog_players
    choose_player(3,out)

def choose_player(i_player, i_row):
    players[i_player].name = dat[int(i_row)]['Name']
    players[i_player].id = dat[int(i_row)]['ID']
    players[i_player].image = dat[i_row]['image']
    players[i_player].text = dat[i_row]['Name']
    ui.notify(f'You chose i_player: {i_player} and i_row: {i_row} -> {players[i_player].name}')