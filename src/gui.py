# Gui class

# Import python packages
import PySimpleGUI as sg
import pandas as pd
import operator
from PIL import Image

class GUI():
    def __init__(self):
        # Settings
        self.font = 'Carlito'
        
        # Read data
        self.data_list = pd.read_csv('data/database_kicker_app.csv')
        table = sg.Table(   values=self.data_list.values.tolist(), 
                            headings=self.data_list.columns.tolist(),
                            justification='center',
                            num_rows=15,
                            expand_x=True,
                            expand_y=True,
                            enable_click_events=True,
                            key='-TABLE-',
                            font=self.font+' 12',
                            text_color='#002435',
                            background_color='white',
                            header_font=(self.font,'14','bold'),
                            sbar_width=20
        )
        
        # Layout
        but_player_1 = create_player_button(1)
        but_player_2 = create_player_button(2)
        but_player_3 = create_player_button(3)
        but_player_4 = create_player_button(4)
        
        but_p_1 = create_score_button('+',1,self.font)
        but_p_2 = create_score_button('+',2,self.font)
        but_m_1 = create_score_button('-',1,self.font)
        but_m_2 = create_score_button('-',2,self.font)
        
        txt_score = sg.Text('0:0', key='but_score', font=(self.font,'30','bold'), expand_x=True, justification='center')
        
        layout_score = [[sg.Text(' ', font=(self.font,'20','bold'), expand_x=False, justification='center')],
                        [but_p_1,but_p_2],
                        [txt_score],
                        [but_m_1,but_m_2]]
        layout_team1 = [[sg.Text('Team weiß', font=(self.font,'20','bold'), expand_x=False, justification='center')],
                        [but_player_1,but_player_2]]
        layout_team2 = [[sg.Text('Team schwarz', font=(self.font,'20','bold'), expand_x=False, justification='center')],
                        [but_player_3,but_player_4]]
        layout_add_rm = [[sg.Button('Hinzufügen',key='-ADD-',font=(self.font,'16','bold'),expand_x=True,size=(20,1)),sg.Button('Rematch',key='-REMATCH-',font=(self.font,'16','bold'),expand_x=True,size=(20,1))]]
        
        layout = [[sg.Text('LTD Kicker App', font=(self.font,'36','bold'), expand_x=True, justification='center')],
                  [sg.Text('',expand_x=True),sg.Column(layout_team1, element_justification='center', justification='right', expand_x=False),sg.Column(layout_score, expand_x=False, expand_y=True),sg.Column(layout_team2, element_justification='center', justification='left', expand_x=False),sg.Text('',expand_x=True)],
                  [sg.Column(layout_add_rm,element_justification='center',justification='center')],
                  [table]]

        self.mainWindow = sg.Window('LTD Kicker App', layout,
                                    grab_anywhere=True, 
                                    no_titlebar=False, 
                                    finalize=True,
                                    resizable=True)
        

    def run(self):
            
        # currently sorted columns
        i_col_sorted = 0
        sort_descending = False
        table_wid = self.mainWindow['-TABLE-'].Widget
        
        while True:
            event, values = self.mainWindow.read()

            if event == sg.WINDOW_CLOSED:
                break
            # elif event in ['but_player_1' + nr for nr in range(1,5)]:
            #     break
            #     # Open window to select player
            elif isinstance(event, tuple):
                if event[0] == '-TABLE-':
                    if event[2][0] == -1 and event[2][1] != -1:
                        i_col_clicked = event[2][1]
                        headers = self.data_list.columns.tolist()
                        if i_col_clicked == i_col_sorted and not sort_descending:
                            sort_descending = True
                            headers[i_col_clicked] += ' \u2193'
                        else:
                            sort_descending = False
                            headers[i_col_clicked] += ' \u2191'
                            
                        sorted_table = sort_table(self.data_list.values.tolist(), i_col_clicked, descending=sort_descending)
                        self.mainWindow['-TABLE-'].update(sorted_table)
                        update_title(table_wid, self.data_list.columns.tolist(), headers)
                        
                        i_col_sorted = i_col_clicked

# Auxiliary classes and function
# Function to create image buttons
def create_player_button(id):
    target_sz = 160                     # pixels
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
def create_score_button(sign,team,font):
    if sign == '+':
        key_txt = 'p_' + str(team)
        just = 'left'
    else:
        key_txt = 'm_' + str(team)
        just = 'right'
    
    return sg.Button(sign,key='key_but_' + key_txt, expand_x=False, size=(4,1),font=(font,'16','bold'))

# Sort table
def sort_table(table, i_col_clicked, descending=False):
    table = sorted(table, key=operator.itemgetter(i_col_clicked))
    if descending:
        table.reverse()
    return table

# Update table headings
def update_title(table, headings, new_headings):
    for cid, text in zip(headings, new_headings):
        table.heading(cid, text=text)