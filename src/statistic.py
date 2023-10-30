# Import public modules
from nicegui import app, ui
import cv2, os.path
import pandas as pd

path_old = 'C:/Users/LTD/log.txt'

# Import custom modules
from init import df_players, player, clear_tmp

def content() -> None:
    with ui.tab_panel('Statistik').style('background-color: rgb(255,255,255)'):
        ui.button('Zeige alte Statisitk', on_click=lambda: show_old_statistics())

# Function to show old statistic
def show_old_statistics():
    # Read old data
    df_old = pd.read_table(path_old)
    df_old['WinRate'] = [a for a  in round(df_old['Wins'] / df_old['Games']*100,1)]

    # Define columns
    # Create data and columns properties for table
    columns_old = [
        {'name': 'name',        'label': 'Name',            'field': 'Name',            'sortable': True,   'align': 'left'},
        {'name': 'games',       'label': 'Spiele',          'field': 'Games',           'sortable': True,   'align': 'center'},
        {'name': 'wins',        'label': 'Siege',           'field': 'Wins',            'sortable': True,   'align': 'center'},
        {'name': 'winrate',     'label': 'Quote / %',       'field': 'WinRate',         'sortable': True,   'align': 'center'},
        {'name': 'goals',       'label': 'Tore',            'field': 'Tore',            'sortable': True,   'align': 'center'},
        {'name': 'goals_a',     'label': 'Gegentore',       'field': 'ggTore',          'sortable': True,   'align': 'center'},
        {'name': 'last_game',   'label': 'zuletzt gespielt','field': 'zuletztGespielt', 'sortable': True,   'align': 'center'},
    ]

    # Create table
    with ui.dialog() as dialog, ui.card().props('bordered horizontal').style('max-width:350vh'):
        table = ui.table(columns=columns_old, rows=df_old.to_dict('records'), row_key='Name').style('height: 62vh; width: 1200px; color:rgb(0,60,90); font-size: 28px; background-color: rgb(240,240,240)')
        ui.button('Schließen', on_click=dialog.close).style('font-weight: bold; background-color: rgb(255,0,0);')

    dialog.open()