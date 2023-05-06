from nicegui import app, ui
import pandas as pd
from os.path import isfile

# General settings
app.add_static_files('/media', 'media')

df = pd.read_csv('data/data-kicker-app.txt',sep='\t')
df['Quote'] = [str(a) + ' %' for a  in round(df['Wins'] / df['Games']*100,1)]
df['image'] = ['media/image_' + a + '.png' for a in df['Name']]
for i,row in df.iterrows():
    if not isfile(row['image']):
        df.at[i,'image'] = 'media/dummy_player.png'

dat = df.to_dict('records')
columns = [
    {'name': 'name', 'label': 'Name', 'field': 'Name', 'sortable': True, 'align': 'left'},
    {'name': 'image', 'label': 'Bild', 'field': 'image', 'sortable': False, 'align': 'center'},
    {'name': 'games', 'label': 'Spiele', 'field': 'Games', 'sortable': True, 'align': 'center'},
    # Add other columns here
]

table = ui.table(columns=columns, rows=dat)
table.add_slot('body',
               r'''
               <q-tr :props="props">
                   <q-td
                       v-for="col in props.cols"
                       :key="col.name"
                       :props="props"
                   >
                       <span v-if="col.name != 'image'">{{ col.value }}</span>
                       <q-avatar v-if="col.name === 'image'" size="80px" class="shadow-10">
                           <img :src="col.value">
                       </q-avatar>
                   </q-td>
               </q-tr>
               ''')

# app.add(table)
ui.run()