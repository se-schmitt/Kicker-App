# Import public modules
from nicegui import app, ui
import cv2, os.path

# Import custom modules
from init import df_players, player, clear_tmp

def content() -> None:
    with ui.tab_panel('Statistik').style('background-color: rgb(255,255,255)'):
        ui.button('Zeige alte Statisitk', on_click=lambda: show_old_statistic())

# Function to show old statistic
def show_old_statistics():
    