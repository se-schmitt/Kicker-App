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

def create_get_name(n):
    def get_name():
        print(dialog_players.value)
        dialog_players.close()
    return get_name

# Dialog to choose player
with ui.dialog() as dialog_players, ui.card().props('bordered horizontal').style('max-width:300vh'):
    with ui.grid(columns=9).style('width:100vh'):
        for i,row in df.iterrows():
            with ui.image(row['image']).on('click',create_get_name(i)).style('width:100%'):
                ui.label(row['Name']).classes('absolute-bottom text-subtitle2 text-center')

def choose_player(i):
    dialog_players.set_value(i)
    dialog_players.open()
    ui.notify(f'You chose {i}')