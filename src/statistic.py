# Import public modules
from nicegui import app, ui
import cv2, os.path
import pandas as pd

path_old = '/home/sebastian/Downloads/log.txt'

# Import custom modules
from init import df_players, player, clear_tmp

def content() -> None:
    with ui.tab_panel('Statistik').style('background-color: rgb(255,255,255)'):
        ui.button('Zeige alte Statisitk', on_click=lambda: show_old_statistics())

# Function to show old statistic
def show_old_statistics():
    # Read old data
    df_old = pd.read_table(path_old)

    # Define columns
    # Create data and columns properties for table
    columns_old = [
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