from nicegui import app, ui
import pandas as pd
from os.path import isfile
import copy

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

global id_player
id_player = 0

players = [ player('Spieler 1',1,'media/dummy_player.png'),
            player('Spieler 2',2,'media/dummy_player.png'),
            player('Spieler 3',3,'media/dummy_player.png'),
            player('Spieler 4',4,'media/dummy_player.png')  ]

def create_get_name(n):
    def get_name():
        print(dialog_players.value)
        # print(df.at[id_player-1,'image'])
        # players[id_player - 1] = player(n, id_player, df.at[id_player-1,'image'])
        dialog_players.close()
    return get_name

# Dialog to choose player
with ui.dialog() as dialog_players, ui.card().props('bordered horizontal').style('max-width:300vh'):
    with ui.grid(columns=9).style('width:100vh'):
        for i,row in df.iterrows():
            with ui.image(row['image']).on('click',create_get_name(i)).style('width:100%'):
                ui.label(row['Name']).classes('absolute-bottom text-subtitle2 text-center')
    # for i,row in df.iterrows():
    #     ui.image(row['image']).on('click',lambda: print(row['name'])).style('width:20%')


def choose_player(i):
    dialog_players.set_value(i)
    dialog_players.open()
    ui.notify(f'You chose {i}')

# columns = [
#     {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
#     {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
# ]
# dat = [
#     {'name': 'Alice', 'age': 18},
#     {'name': 'Bob', 'age': 21},
#     {'name': 'Carol'},
# ]

# General settings
app.add_static_files('/media', 'media')

# Tabs definition
with ui.header().classes('w-full justify-between  items-center').style('color:rgb(0,60,90);background:rgb(200,200,200);height:7%'):
    ui.label('LTD Kicker App').classes('font-bold').style('font-size: 20px')
    tabs = ui.tabs().props('inline-label').classes('inline-label')
    imag = ui.image('https://mv.rptu.de/fileadmin/_processed_/4/d/csm_LTD_LOGO_DE_0_95_140_5f0ada1f40.png').style('width:150px;text-align:right;') #.classes('col self-end')
with tabs:
    ui.tab('Home', icon='home')
    ui.tab('Statistik', icon='leaderboard')
    ui.tab('Turnier', icon='emoji_events')
    ui.tab('Einstellungen', icon='settings')

# Tabs content
tab_panels = ui.tab_panels(tabs, value='Home').props('horizontal').classes('w-full justify-center')
with tab_panels:
    # Tab 'Home'
    with ui.tab_panel('Home'):
        # Spielstand
        with ui.card():
            with ui.row().classes('w-full justify-center items-around').style('height: 21vh'):
                with ui.column().classes('justify-center'):
                    with ui.card():
                        ui.label('Team 1').classes('w-full').style('text-align:center;font-size:24px')
                        with ui.row().classes('w-full justify-center'):
                            with ui.image('/media/dummy_player.png').style('width:150px').on('click',lambda: choose_player(1)):
                                ui.label('Spieler 1').classes('absolute-bottom text-subtitle2 text-center')
                            with ui.image('/media/dummy_player.png').style('width:150px').on('click',lambda: choose_player(2)):
                                ui.label('Spieler 2').classes('absolute-bottom text-subtitle2 text-center')

                with ui.column().classes('justify-center items-around').props('vertical-bottom'):
                    with ui.card():
                        with ui.row().classes('justify-center items-around text-center').style('font-size:40px'):
                            ui.select([0,1,2,3,4,5,6], value=0).props(add='no-icon-animation').style('font-size:40px; color:rgb(0,60,90);')
                            ui.label(':')
                            ui.select([0,1,2,3,4,5,6], value=0).style('font-size:40px')
                        ui.button('Hinzufügen').style('width:100%')
                        ui.button('Rematch').style('width: 100%')


                with ui.column().classes('justify-center'):
                    with ui.card():
                        ui.label('Team 2').classes('w-full').style('text-align:center;font-size:24px')
                        with ui.row().classes('w-full justify-center'):
                            # image_pl3 = ui.image('/media/dummy_player.png').style('width:150px').on(type='click',handler=print(3))
                            with ui.image('/media/dummy_player.png').style('width:150px').on('click',lambda: choose_player(3)):
                                ui.label('Spieler 3').classes('absolute-bottom text-subtitle2 text-center')
                            with ui.image('/media/dummy_player.png').style('width:150px').on('click',lambda: choose_player(4)):
                                ui.label('Spieler 4').classes('absolute-bottom text-subtitle2 text-center').bind_text_from(players[3])
        
        # Table
        with ui.card():
            with ui.row().classes('w-full justify-center items-around').style('color:rgb(0,60,90)'):
                table = ui.table(columns=columns, rows=dat).style('height: 62vh; width: 1000px; color:rgb(0,60,90); font-size: 20px; background-color: rgb(240,240,240)')
                table.add_slot('body',
                r'''
                <q-tr :props="props">
                    <q-td
                        v-for="col in props.cols"
                        :key="col.name"
                        :props="props"
                    >
                        <span v-if="col.name != 'image'">{{ col.value }}</span>
                        <q-avatar v-if="col.name === 'image'" size="40px" class="shadow-4">
                            <img :src="col.value">
                        </q-avatar>
                    </q-td>
                </q-tr>
                ''')
                table.add_slot('header',
                r'''
                <q-tr :props="props" style="position: sticky; top: 0; background-color: rgb(220,220,220); z-index: 1; font-size:20px;">
                    <q-th
                        v-for="col in props.cols"
                        :key="col.name"
                        :props="props"
                        style="padding: 5px;"
                    >
                        {{ col.label }}
                    </q-th>
                </q-tr>
                ''')

    # Tab 'Statistik'
    with ui.tab_panel('Statistik'):
        ui.label('This is the second tab')

    # Tab 'Turnier'
    with ui.tab_panel('Turnier'):
        ui.label('This is the third tab')

    # Tab 'Einstellungen'
    with ui.tab_panel('Einstellungen'):
        ui.label('This is the fourth tab')



ui.run(title='LTD Kicker App',dark=False)
# ui.run(native=True, window_size=(400, 300), fullscreen=False)
