# Import public modules
from nicegui import app, ui

# Import custom modules
from init import players, dat, df_players

# Define function to create lambda function
def make_lambda(i):
    return lambda: dialog_players.submit(i)

# Dialog to choose player
with ui.dialog() as dialog_players, ui.card().props('bordered horizontal').style('max-width:300vh'):
    with ui.grid(columns=9).style('width:100vh'):
        for i,row in df_players.iterrows():
            with ui.image(row['Image']).on('click',make_lambda(i)).style('width:100%'):
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
    players[i_player].image = dat[i_row]['Image']
    players[i_player].text = dat[i_row]['Name']
    ui.notify(f'You chose i_player: {i_player} and i_row: {i_row} -> {players[i_player].name}')