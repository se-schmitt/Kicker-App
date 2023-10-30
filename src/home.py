# Import public modules
from nicegui import app, ui

# Import custom modules
from init import players, columns, df_players, scores, add_game, set_rematch
from dialog import choose_player_1, choose_player_2, choose_player_3, choose_player_4

def content() -> None:
    with ui.tab_panel('Home').style('background-color: rgb(255,255,255)'):
        with ui.column().classes('justify-center items-around'):
            # Spielstand
            with ui.row().classes('w-full justify-center items-around').style('height: 21vh'):
                with ui.column().classes('justify-center'):
                    with ui.card().style('background-color: rgb(255,255,255)'):
                        ui.label('Team weiß').classes('w-full').style('text-align:center;font-size:24px')
                        with ui.row().classes('w-full justify-center'):
                            with ui.image('/media/dummy_player.png').style('width:150px').on('click',choose_player_1).bind_source(players[0],target_name='image'):
                                ui.label('Spieler 1').classes('absolute-bottom text-subtitle2 text-center').bind_text(players[0],'name')
                            with ui.image('/media/dummy_player.png').style('width:150px').on('click',choose_player_2).bind_source(players[1],target_name='image'):
                                ui.label('Spieler 2').classes('absolute-bottom text-subtitle2 text-center').bind_text(players[1],'name')

                with ui.column().classes('justify-center items-around').props('vertical-bottom'):
                    with ui.card().style('background-color: rgb(220,220,220)'):
                        with ui.row().classes('justify-center items-around text-center').style('font-size:40px'):
                            ui.select([0,1,2,3,4,5,6], value=0).props(add='no-icon-animation').style('font-size:40px; color:rgb(0,60,90);').bind_value(scores,'score1')
                            ui.label(':')
                            ui.select([0,1,2,3,4,5,6], value=0).style('font-size:40px').bind_value(scores,'score2')
                        ui.button('Hinzufügen',on_click=lambda: add_game()).style('width:100%')
                        ui.button('Rematch', on_click=lambda: set_rematch()).style('width: 100%')


                with ui.column().classes('justify-center'):
                    with ui.card().style('background-color: rgb(50,50,50)'):
                        ui.label('Team schwarz').classes('w-full').style('text-align:center; font-size:24px; color:rgb(255,255,255)')
                        with ui.row().classes('w-full justify-center'):
                            with ui.image('/media/dummy_player.png').style('width:150px').on('click',choose_player_3).bind_source(players[2],target_name='image'):
                                ui.label('Spieler 3').classes('absolute-bottom text-subtitle2 text-center').bind_text(players[2],'name')
                            with ui.image('/media/dummy_player.png').style('width:150px').on('click',choose_player_4).bind_source(players[3],target_name='image'):
                                ui.label('Spieler 4').classes('absolute-bottom text-subtitle2 text-center').bind_text(players[3],'name')
            
            # Table
            with ui.row().classes('w-full justify-center items-around').style('color:rgb(0,60,90)'):
                table = ui.table(columns=columns, rows=df_players.to_dict('records'), row_key='Name').style('height: 62vh; width: 1200px; color:rgb(0,60,90); font-size: 28px; background-color: rgb(240,240,240)')
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
                <q-tr :props="props" style="position: sticky; top: 0; background-color: rgb(240,240,240); z-index: 1; font-size:20px;">
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

    # Return table
    return table


