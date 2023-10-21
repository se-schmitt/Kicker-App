# Import public modules
from nicegui import app, ui

# Import custom modules
from init import players, df_players

# Define function to create lambda function
def make_lambda(i):
    return lambda: dialog_players.submit(i)

# Dialog to choose player
with ui.dialog() as dialog_players, ui.card().props('bordered horizontal').style('max-width:350vh'):
    with ui.grid(columns=8).style('width:150vh'):
        for i,row in df_players.iterrows():
            with ui.image(row['Image']).on('click',make_lambda(i)).style('width:100%; display: block; margin-left: auto; margin-right: auto; clip-path: circle(50% at center)'):
                ui.label(row['Name']).classes('absolute-bottom text-subtitle2 text-center').style('line-height:0%; text-align: center')
dialog_players.open()
dialog_players.set_visibility(False)

# Choose player function
async def choose_player_1():
    dialog_players.set_visibility(True)
    out = await dialog_players
    choose_player(0,out)

async def choose_player_2():
    dialog_players.set_visibility(True)
    out = await dialog_players
    choose_player(1,out)

async def choose_player_3():
    dialog_players.set_visibility(True)
    out = await dialog_players
    choose_player(2,out)

async def choose_player_4():
    dialog_players.set_visibility(True)
    out = await dialog_players
    choose_player(3,out)

def choose_player(i_player, id_name):
    # Open and hide dialog for next choice
    dialog_players.open()
    dialog_players.set_visibility(False)

    # Set player
    if id_name is not None:
        players[i_player].name = df_players.at[id_name,'Name']
        players[i_player].image = df_players.at[id_name,'Image']
        ui.notify(f'You chose i_player: {i_player} and i_row: {id_name} -> {players[i_player].name}')