# Import public modules
from nicegui import app, ui
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from init import players, columns, df_players, scores, add_game, set_rematch
from dialog import choose_player_1, choose_player_2, choose_player_3, choose_player_4

path_old = 'C:/Users/LTD/Documents/log.txt'
path_data = 'data/database_games.csv'
path_player = 'data/database_players.csv'

# Import custom modules
from init import df_players, player, clear_tmp

def content() -> None:
    with ui.tab_panel('Statistik').style('background-color: rgb(255,255,255)'):
        # create vertical split -> (value=9) -> 9% of site is the dropdown menu
        with ui.splitter(value=9).classes('w-full h-full') as splitter: 
            with splitter.before:
                with ui.tabs().props('vertical').classes('w-256') as tabs:
                    plot = ui.tab('Show Elo Plot', icon='query_stats')
                    h2h = ui.tab('Show Head-to-Head', icon='group')
                    stat = ui.tab('Zeige alte Statistik', icon='folder')
            with splitter.after: 
                with ui.tab_panels(tabs, value=plot) \
                        .props('vertical').classes('w-256 h-full'):
                    # create first page
                    with ui.tab_panel(plot):
                        ui.label('Show Elo Plot').classes('text-h4')
                        show_elo_plot()
                    # create second page
                    with ui.tab_panel(h2h):
                        with ui.row().classes('justify-center'):
                            with ui.card().style('background-color: rgb(255,255,255)'):
                                ui.label('Team weiß').classes('w-full').style('text-align:center;font-size:24px')
                                with ui.row().classes('w-full justify-center'):
                                    with ui.image('/media/dummy_player.png').style('width:150px; clip-path: circle(50% at center)').on('click',choose_player_1).bind_source(players[0],target_name='image'):
                                        ui.label('Spieler 1').classes('absolute-bottom text-subtitle2 text-center').bind_text(players[0],'name')
                                    with ui.image('/media/dummy_player.png').style('width:150px; clip-path: circle(50% at center)').on('click',choose_player_2).bind_source(players[1],target_name='image'):
                                        ui.label('Spieler 2').classes('absolute-bottom text-subtitle2 text-center').bind_text(players[1],'name')
                            with ui.card().style('background-color: rgb(50,50,50)'):
                                ui.label('Team schwarz').classes('w-full').style('text-align:center; font-size:24px; color:rgb(255,255,255)')
                                with ui.row().classes('w-full justify-center'):
                                    with ui.image('/media/dummy_player.png').style('width:150px; clip-path: circle(50% at center)').on('click',choose_player_3).bind_source(players[2],target_name='image'):
                                        ui.label('Spieler 3').classes('absolute-bottom text-subtitle2 text-center').bind_text(players[2],'name')
                                    with ui.image('/media/dummy_player.png').style('width:150px; clip-path: circle(50% at center)').on('click',choose_player_4).bind_source(players[3],target_name='image'):
                                        ui.label('Spieler 4').classes('absolute-bottom text-subtitle2 text-center').bind_text(players[3],'name')
                                            
                    columns = [
                        {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
                        {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
                    ]
                    rows = [
                        {'name': 'Alice', 'age': 18},
                        {'name': 'Bob', 'age': 21},
                        {'name': 'Carol'},
                    ]
                    ui.table(columns=columns, rows=rows, row_key='name')
                    # create third page
                    with ui.tab_panel(stat):
                        ui.label('Zeige alte Statistik').classes('text-h4')
                        show_old_statistics
        #with ui.column():
         #   with ui.row():
          #      ui.button('Zeige alte Statistik', on_click=lambda: show_old_statistics())
           #     ui.button('Show Elo Plot', on_click=lambda: show_elo_plot())
            #    ui.button('Show Head-to-Head', on_click=lambda: show_H2H())
            
        
        



# Function to show old statistic
def show_old_statistics():
    # Read old data
    df_old = pd.read_table(path_old)
    df_old['WinRate'] = [a for a  in round(df_old['Wins'] / df_old['Games']*100,1)]

    # Define columns
    # Create data and columns properties for table
    columns_old = [
        {'name': 'name',        'label': 'Name',            'field': 'Name',            'sortable': True,   'align': 'left'},
        {'name': 'games',       'label': 'Spiele',          'field': 'Games',           'sortable': True,   'align': 'center'},
        {'name': 'wins',        'label': 'Siege',           'field': 'Wins',            'sortable': True,   'align': 'center'},
        {'name': 'winrate',     'label': 'Quote / %',       'field': 'WinRate',         'sortable': True,   'align': 'center'},
        {'name': 'goals',       'label': 'Tore',            'field': 'Tore',            'sortable': True,   'align': 'center'},
        {'name': 'goals_a',     'label': 'Gegentore',       'field': 'ggTore',          'sortable': True,   'align': 'center'},
        {'name': 'last_game',   'label': 'zuletzt gespielt','field': 'zuletztGespielt', 'sortable': True,   'align': 'center'},
    ]

    # Create table
    with ui.dialog() as dialog, ui.card().props('bordered horizontal').style('max-width:350vh'):
        table = ui.table(columns=columns_old, rows=df_old.to_dict('records'), row_key='Name').style('height: 62vh; width: 1200px; color:rgb(0,60,90); font-size: 28px; background-color: rgb(240,240,240)')
        ui.button('Schließen', on_click=dialog.close).style('font-weight: bold; background-color: rgb(255,0,0);')

    dialog.open()

# Function to show elo plots
def show_elo_plot():
    
    # Read data
    d = {}
    dp = pd.read_csv(path_player)
    dp_names = [a for a  in dp['Name']]
    df_elo = 1000*np.ones(len(dp_names))
    df_games = np.zeros(len(dp_names))

    df = pd.read_csv(path_data)
    df_time = [a for a  in df['DateTime']]
    df_date = []
    for (i,id) in (enumerate(df_time)):
        df_date.append(df_time[i].partition(" ")[0])
    df_p1 = [a for a  in df['Player1']]
    df_p2 = [a for a  in df['Player2']]
    df_p3 = [a for a  in df['Player3']]
    df_p4 = [a for a  in df['Player4']]
    df_c1 = [a for a  in df['Color1']]
    df_c2 = [a for a  in df['Color2']]
    df_s1 = [a for a  in df['Score1']]
    df_s2 = [a for a  in df['Score2']]

    plot = []
    plot_date = []
    for (i,id) in (enumerate(df_p1)):
        update_elo(df_elo, df_games,(df_p1[i], df_p2[i], df_p3[i], df_p4[i]),dp_names,df_s1[i],df_s2[i])
        if i < len(df_date)-1:
            if df_date[i] != df_date[i+1]:
                curr_elo = []
                plot_date.append(df_date[i])
                for (j,jd) in (enumerate(dp_names)):
                    curr_elo.append(df_elo[j])
                plot.append(curr_elo)
    plot = np.array(plot)

    class ToggleButton(ui.button):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self._state = False
            self.on('click', self.toggle)
        
        def toggle(self) -> None:
            """Toggle the button state."""
            self._state = not self._state
            self.update()

        def update(self) -> None:
            self.props(f'color={"green" if self._state else "red"}')
            super().update()

    with ui.row():
        for (i,id) in enumerate(dp_names):
            d["_{0}".format(i)] = ToggleButton(dp_names[i])
    
    ui.button('Plot ELO for selected Players!', on_click=lambda: Graph())
    
    #TODO: Once pushed to console -> recalculate elo and edit database_players.xlsx
    #for (i,id) in enumerate(dp_names):
    #    ui.label(plot[-1,i])

    main_plot = ui.pyplot(close=False, figsize=(16, 6))

    def Graph():
        with main_plot:
            plt.clf()
            #x = np.linspace(0.0, 5.0)
            #y = np.cos(2 * np.pi * x) * np.exp(-x)#
            for (i,id) in enumerate(dp_names):
                if d["_{0}".format(i)]._state != False:
                    d["__{0}".format(i)] = plt.plot( plot[:,i], '-', label=dp_names[i])
            plt.title("Elo Plot")
            plt.xlabel("Documented days since start of ELO system / d")
            plt.ylabel("ELO / -")
            plt.legend(loc="upper left")
        

    return

# Function to show head to head data
def show_H2H():
    # Read old data
    df_old = pd.read_table(path_old)
    df_old['WinRate'] = [a for a  in round(df_old['Wins'] / df_old['Games']*100,1)]

    # Define columns
    # Create data and columns properties for table
    columns_old = [
        {'name': 'name',        'label': 'Name',            'field': 'Name',            'sortable': True,   'align': 'left'},
        {'name': 'games',       'label': 'Spiele',          'field': 'Games',           'sortable': True,   'align': 'center'},
        {'name': 'wins',        'label': 'Siege',           'field': 'Wins',            'sortable': True,   'align': 'center'},
        {'name': 'winrate',     'label': 'Quote / %',       'field': 'WinRate',         'sortable': True,   'align': 'center'},
        {'name': 'goals',       'label': 'Tore',            'field': 'Tore',            'sortable': True,   'align': 'center'},
        {'name': 'goals_a',     'label': 'Gegentore',       'field': 'ggTore',          'sortable': True,   'align': 'center'},
        {'name': 'last_game',   'label': 'zuletzt gespielt','field': 'zuletztGespielt', 'sortable': True,   'align': 'center'},
    ]

    # Create table
    with ui.dialog() as dialog, ui.card().props('bordered horizontal').style('max-width:350vh'):
        table = ui.table(columns=columns_old, rows=df_old.to_dict('records'), row_key='Name').style('height: 62vh; width: 1200px; color:rgb(0,60,90); font-size: 28px; background-color: rgb(240,240,240)')
        ui.button('Schließen', on_click=dialog.close).style('font-weight: bold; background-color: rgb(255,0,0);')

    dialog.open()

def update_elo(df,games,ids,dp_names,s1,s2):
    # Read position of current players in the full array
    df_update = []
    for (j,jd) in enumerate(ids):
        for (i,id) in enumerate(dp_names):
            if id == jd:
                df_update.append(i)
    # Pre-allocate K and R, set parameters depending on original elo and games count for each player
    K = []
    R_old = []
    for (i,id) in enumerate(ids):
        #K.append(50 / (1 + df.at[id,'Games'] / 200)) # original calc
        K.append(40)
        R_old.append(df[df_update[i]])
    P = 1 + abs(s1-s2)/6
    
    # Calculate winning probability for each team
    Eps,Ets = calc_win_prob(R_old)
    
    # Calculate new ELO scores for each player
    # in Version 0 ELO was NOT strictly conserved, in fact, 222.9 ELO is "lost"
    # Winning probabilities of any player are scaled with how many games the played, which results in deviations from convervation (lol)
    # Solution: 
    # a) Dont weight the amount of games played
    # b) Additionally, change from "calculate ELO from per player win probabilities" to "calculate ELO from team win propabilities" and then use
    # c) a simple rescaling depending on the initial per-player Elo's
    # Example: Team A (Player 1 ELO: 1100, Player 2 ELO: 900) wins over Team B (Player 3 ELO: 1000, Player 4 ELO: 1200) by 6:3. 
    #          Expected win probability Team A: 38.69%, Team B: 61.31%
    #          The Team-ELO gain then gets split depending on their percentage of the total team ELO
    #          Player 1: +16.55
    #          Player 2: +20.23
    #          Player 3: -16.72
    #          Player 4: -20.07
        
    
    for (i,id) in enumerate(ids):
        if id in [ids[0],ids[1]]:
            if s1 > s2:
                S = 1  
                df[df_update[i]] += (1-(R_old[i]/(R_old[0]+R_old[1]))) *  K[i] * P * (S - Ets[0])
            else:
                S = 0
                df[df_update[i]] += (R_old[i]/(R_old[0]+R_old[1])) *  K[i] * P * (S - Ets[0])
        else:
            if s2 > s1:
                S = 1  
                df[df_update[i]] += (1-(R_old[i]/(R_old[2]+R_old[3]))) *  K[i] * P * (S - Ets[1])
            else:
                S = 0
                df[df_update[i]] += (R_old[i]/(R_old[2]+R_old[3])) *  K[i] * P * (S - Ets[1])
        
        df[df_update[i]] = round(df[df_update[i]],1)
        games[df_update[i]] += 1
            
    return 0

# Function to calculate Winning probability from ELO scores
def calc_win_prob(Rall):
    # Set parameter
    # TODO: With the new calculation D might needs to be lower (e.g. 250)
    D = 500
    #ui.label(Rall).classes('text-h4').style('text-align:center;font-size:12px')
    # Calculate winning probability for each player
    Rp1,Rp2,Rp3,Rp4 = Rall
    Ep1 = (1 / (1 + 10**((Rp3 - Rp1)/D)) + 1 / (1 + 10**((Rp4 - Rp1)/D))) / 2
    Ep2 = (1 / (1 + 10**((Rp3 - Rp2)/D)) + 1 / (1 + 10**((Rp4 - Rp2)/D))) / 2
    Ep3 = (1 / (1 + 10**((Rp1 - Rp3)/D)) + 1 / (1 + 10**((Rp2 - Rp3)/D))) / 2
    Ep4 = (1 / (1 + 10**((Rp1 - Rp4)/D)) + 1 / (1 + 10**((Rp2 - Rp4)/D))) / 2

    # Calculate winning probability for each team
    Rt1 = np.mean([Rp1,Rp2])
    Rt2 = np.mean([Rp3,Rp4])
    Et1 = 1 / (1 + 10**((Rt2 - Rt1)/D))
    Et2 = 1 / (1 + 10**((Rt1 - Rt2)/D))

    return (Ep1,Ep2,Ep3,Ep4),(Et1,Et2)

def update_elo_alt(df,games,ids,dp_names,s1,s2):
    # Read position of current players in the full array
    df_update = []
    for (j,jd) in enumerate(ids):
        for (i,id) in enumerate(dp_names):
            if id == jd:
                df_update.append(i)
    # Pre-allocate K and R, set parameters depending on original elo and games count for each player
    K = []
    R_old = []
    for (i,id) in enumerate(ids):
        K.append(40)
        R_old.append(df[df_update[i]])
    P = 1 + abs(s1-s2)/6
    
    # Calculate winning probability for each team
    Eps,Ets = calc_win_prob_alt(R_old)
    
    # Calculate new ELO scores for each player
    # in Version 0 ELO is NOT strictly conserved, in fact, 222.9 ELO is "lost"
    # Winning probabilities of any player are scaled with how many games the played, which results in deviations from convervation (lol)
    # Solution 1: Dont weight the amount of games played (easiest and probably the fairest?!)
    # Solution 2: Use the weighting to FIRST calculate +- for each team (conserved) and then split them for each player depending on their elo
    # Solution 3: Brute force the conservation as a last step by scaling
    for (i,id) in enumerate(ids):
        if id in [ids[0],ids[1]]:
            S = 1 if s1 > s2 else 0
        else:
            S = 1 if s1 < s2 else 0
        df[df_update[i]] += K[i] * P * (S - Eps[i])
        df[df_update[i]] = round(df[df_update[i]],1)
        games[df_update[i]] += 1

    #ui.label(df).classes('text-h4').style('text-align:center;font-size:12px')
    
    return 0

# Function to calculate Winning probability from ELO scores
def calc_win_prob_alt(Rall):
    # Set parameter
    D = 500
    #ui.label(Rall).classes('text-h4').style('text-align:center;font-size:12px')
    # Calculate winning probability for each player
    Rp1,Rp2,Rp3,Rp4 = Rall
    Ep1 = (1 / (1 + 10**((Rp3 - Rp1)/D)) + 1 / (1 + 10**((Rp4 - Rp1)/D))) / 2
    Ep2 = (1 / (1 + 10**((Rp3 - Rp2)/D)) + 1 / (1 + 10**((Rp4 - Rp2)/D))) / 2
    Ep3 = (1 / (1 + 10**((Rp1 - Rp3)/D)) + 1 / (1 + 10**((Rp2 - Rp3)/D))) / 2
    Ep4 = (1 / (1 + 10**((Rp1 - Rp4)/D)) + 1 / (1 + 10**((Rp2 - Rp4)/D))) / 2

    # Calculate winning probability for each team
    Et1 = (Ep1 + Ep2) / 2
    Et2 = (Ep3 + Ep4) / 2

    return (Ep1,Ep2,Ep3,Ep4),(Et1,Et2)

