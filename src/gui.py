# Gui class

# Import python packages
import PySimpleGUI as sg
import pandas as pd
from PIL import Image

class GUI():
    def __init__(self):
        # Read data
        self.data_list = pd.read_csv('data/database_kicker_app.csv')
        table = sg.Table(   values=self.data_list.values.tolist(), 
                            headings=self.data_list.columns.tolist(),
                            justification='left',
                            expand_x=True,
                            expand_y=True
        )
        
        # Layout
        but_player_1 = create_player_button(1)
        but_player_2 = create_player_button(2)
        but_player_3 = create_player_button(3)
        but_player_4 = create_player_button(4)
        
        but_p_1 = create_score_button('+',1)
        but_p_2 = create_score_button('+',2)
        but_m_1 = create_score_button('-',1)
        but_m_2 = create_score_button('-',2)
        
        txt_score = sg.Text('0:0', key='but_score', font='Arial 24', expand_x=True, justification='center')
        
        layout_score = [[sg.Text('', font='Arial 16', expand_x=False, justification='center')],
                        [but_p_1,but_p_2],
                        [txt_score],
                        [but_m_1,but_m_2]]
        layout_team1 = [[sg.Text('Team weiß', font='Arial 16', expand_x=False, justification='center')],
                        [but_player_1,but_player_2]]
        layout_team2 = [[sg.Text('Team schwarz', font='Arial 16', expand_x=False, justification='center')],
                        [but_player_3,but_player_4]]
        
        layout = [[sg.Text('LTD Kicker App', font='Arial 24', expand_x=True, justification='center')],
                  [sg.Column(layout_team1, element_justification='center', justification='right', expand_x=True),sg.Column(layout_score, expand_x=False, expand_y=True),sg.Column(layout_team2, element_justification='center', justification='left', expand_x=True)],
                  [table]]

        self.mainWindow = sg.Window('LTD Kicker App', layout,
                                    grab_anywhere=True, 
                                    no_titlebar=False, 
                                    finalize=True,
                                    resizable=True)
        

    def run(self):
        while True:
            event, values = self.mainWindow.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event in ['but_player_1' + nr for nr in range(1,5)]:
                break
                # Open window to select player

# Auxiliary classes and function
# Function to create image buttons
def create_player_button(id):
    target_sz = 100                     # pixels
    src = 'media/dummy_player.png'
    img = Image.open(src)
    if img.width != img.height:
        print("File '" + src + "' not quadratic!")
    
    if img.width != target_sz or img.height != target_sz:
        img = img.resize((target_sz,target_sz))  
        img.save(src)  
        
    img.close()
        
    out = sg.Image( source=src, 
                    key='player_but_'+str(id), 
                    size=(target_sz,target_sz),
                    enable_events=True,)
    return out

# Create button for '+' and '-'
def create_score_button(sign,team):
    if sign == '+':
        key_txt = 'p_' + str(team)
        just = 'left'
    else:
        key_txt = 'm_' + str(team)
        just = 'right'
    
    return sg.Button(sign,key='key_but_' + key_txt, expand_x=False, size=(4,1))