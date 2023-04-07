# Gui class

class GUI():
    def __init__(self):
        layout = [[sg.Text('LTD Kicker App', font='Arial 24')],
                  [[PLAY_BUTTON(nr) for nr in [1,2]],---Ergebnis eingeben---,[PLAY_BUTTON(nr) for nr in [3,4]],
                  ]

        self.mainWindow = sg.Window('LTD Kicker App', layout,
                                    grab_anywhere=True, no_titlebar=False, finalize=True)
        

    def run(self):
        while True:
            event, values = self.mainWindow.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event in ['but_player_1' + nr for nr in range(1,5)]:
                # Open window to select player

# Auxiliary classes and function
# Class to define player buttons
class PLAY_BUTTON():
    def __init__(self, id):
        sg.Button(  button_text = 'Spieler auswählen',
                    key = 'but_player_' + id,
                    s = (10,10),
                    font = 'Arial 12')
            
            
