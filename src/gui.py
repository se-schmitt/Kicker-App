# Gui class

class GUI():
    def __init__(self):
        layout = [[sg.Text('LTD Kicker App')],
                  ]

        self.mainWindow = sg.Window('LTD Kicker App', layout,
                                    grab_anywhere=True, no_titlebar=False, finalize=True)
        

    def run(self):
        while True:

# Auxiliary classes and function
# Class to define player buttons
class PLAY_BUTTON():
    def __init__(self,text):
        sg.Button(  button_text = text,
                    s = (10,10))
            
            
