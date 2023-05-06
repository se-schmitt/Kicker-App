from nicegui import app, ui
import pandas as pd
from os.path import isfile

# Loading
df = pd.read_csv('data/data-kicker-app.txt',sep='\t')
df['Quote'] = [str(a) + ' %' for a  in round(df['Wins'] / df['Games']*100,1)]
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
    {'name': 'quote',       'label': 'Quote',           'field': 'Quote',           'sortable': True,   'align': 'center'},
    {'name': 'goals',       'label': 'Tore',            'field': 'Tore',            'sortable': True,   'align': 'center'},
    {'name': 'goals_a',     'label': 'Gegentore',       'field': 'ggTore',          'sortable': True,   'align': 'center'},
    {'name': 'last_game',   'label': 'zuletzt gespielt','field': 'zuletztGespielt', 'sortable': True,   'align': 'center'},
]

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
with ui.header().classes('w-full justify-between  items-center').style('color:rgb(0,60,90);background:rgb(200,200,200)') as row:
    ui.label('LTD Kicker App').classes('font-bold')
    tabs = ui.tabs().props('inline-label').classes('inline-label')
    imag = ui.image('https://mv.rptu.de/fileadmin/_processed_/4/d/csm_LTD_LOGO_DE_0_95_140_5f0ada1f40.png').style('width:150px;text-align:right;') #.classes('col self-end')
with tabs:
    ui.tab('Home', icon='home')
    ui.tab('Statistik', icon='leaderboard')
    ui.tab('Turnier', icon='emoji_events')
    ui.tab('Einstellungen', icon='settings')

# Tabs content
tab_panels = ui.tab_panels(tabs, value='Home').props('horizontal').classes('w-full justify-center').style('color:rgb(0,60,90);font-size:16px')
with tab_panels:
    # Tab 'Home'
    with ui.tab_panel('Home'):
        # Spielstand
        with ui.row().classes('w-full justify-center items-around'):
            with ui.column().classes('justify-center'):
                ui.label('Team 1').classes('w-full').style('text-align:center;font-size:24px')
                with ui.row().classes('w-full justify-center'):
                    with ui.image('/media/dummy_player.png').style('width:150px'):
                        ui.label('Spieler 1').classes('absolute-bottom text-subtitle2 text-center')
                    with ui.image('/media/dummy_player.png').style('width:150px'):
                        ui.label('Spieler 2').classes('absolute-bottom text-subtitle2 text-center')
            with ui.column().classes('justify-center'):
                with ui.grid(rows=3,columns=3).classes('justify-end items-around text-center').style('font-size:40px'):
                    ui.button('+').style('font-size:20px; width:50px; height:50px')
                    ui.label('')
                    ui.button('+').style('font-size:20px; width:50px; height:50px')

                    ui.label('0')
                    ui.label(':')
                    ui.label('0')

                    ui.button('-').style('font-size:20px; width:50px; height:50px')
                    ui.label('')
                    ui.button('-').style('font-size:20px; width:50px; height:50px')
                ui.button('Hinzufügen').style('width:100%')
                ui.button('Rematch').style('width:100%')

            with ui.column().classes('justify-center'):
                ui.label('Team 2').classes('w-full').style('text-align:center;font-size:24px')
                with ui.row().classes('w-full justify-center'):
                    with ui.image('/media/dummy_player.png').style('width:150px'):
                        ui.label('Spieler 3').classes('absolute-bottom text-subtitle2 text-center')
                    with ui.image('/media/dummy_player.png').style('width:150px'):
                        ui.label('Spieler 4').classes('absolute-bottom text-subtitle2 text-center')
        
        # Table
        with ui.row().classes('w-full justify-center items-around').style('color:rgb(0,60,90);font-size:16px'):
            table = ui.table(columns=columns, rows=dat).style('height: 400px; width: 1000px; color:rgb(0,60,90);font-size:20px; background-color: rgb(240,240,240)')
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
               <q-tr :props="props" style="position: sticky; top: 0; background-color: rgb(230,230,230); z-index: 1; font-size:20px;">
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
