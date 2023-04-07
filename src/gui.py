# Gui class

class GUI():
    def __init__(self):
        layout = [[sg.Text('LTD Kicker App')],
                  ]

        self.mainWindow = sg.Window('LTD Kicker App', layout,
                                    grab_anywhere=True, no_titlebar=False, finalize=True)
        

    def run(self):
        while True:
            
            
