# Import public modules
from nicegui import app, ui
import pandas as pd

# Import custom modules
import home, settings, statistic

# General settings
app.add_static_files('/media', 'media')

# Tabs definition
with ui.header().classes('w-full justify-between  items-center').style('color:rgb(0,60,90);background:rgb(160,160,160);height:7%'):
    ui.label('LTD Kicker App').classes('font-bold').style('font-size: 20px')
    tabs = ui.tabs().props('inline-label').classes('inline-label')
    imag = ui.image('media/LTD_Logo_DE.png').style('width:200px;text-align:right;') #.classes('col self-end')
with tabs:
    ui.tab('Home', icon='home')
    ui.tab('Statistik', icon='leaderboard')
    ui.tab('Turnier', icon='emoji_events')
    ui.tab('Einstellungen', icon='settings')

# Tabs content
tab_panels = ui.tab_panels(tabs, value='Home').props('horizontal').classes('w-full justify-center')
with tab_panels:
    # Tab 'Home'
    table = home.content()

    # Tab 'Statistik'
    statistic.content()

    # Tab 'Turnier'
    with ui.tab_panel('Turnier'):
        ui.label('This is the third tab')

    # Tab 'Einstellungen'
    settings.content()

# Run App
ui.run(title='LTD Kicker App',dark=False)
# ui.run(native=True, window_size=(400, 300), fullscreen=False)
