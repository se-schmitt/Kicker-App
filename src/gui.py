# Gui class

# Import python packages
import PySimpleGUI as sg
from PIL import Image

class GUI():
    def __init__(self):
        
        but_player_1 = create_player_button(1)
        but_player_2 = create_player_button(2)
        but_player_3 = create_player_button(3)
        but_player_4 = create_player_button(4)
        
        layout_score = [[sg.Text('Test')],[sg.Text('Test')]]
        layout_team1 = [[sg.Text('Team weiß',justification='center')],
                        [but_player_1,but_player_2]]
        layout_team2 = [[sg.Text('Team schwarz',justification='center')],
                        [but_player_3,but_player_4]]
        
        layout = [[sg.Text('LTD Kicker App', font='Arial 24')],
                  [sg.Column(layout_team1),sg.Column(layout_score),sg.Column(layout_team2)]
                  ]

        self.mainWindow = sg.Window('LTD Kicker App', layout,
                                    grab_anywhere=True, no_titlebar=False, finalize=True)
        

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
                    enable_events=True)
    return out
