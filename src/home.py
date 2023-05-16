# Import public modules
from nicegui import app, ui

# Import custom modules
from init import choose_player, players, columns, dat

def content() -> None:
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
