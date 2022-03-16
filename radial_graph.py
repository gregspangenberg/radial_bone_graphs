import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pathlib 

def chunks(l,n):
    """ split l into n sized chunks"""
    return [l[i:i + n] for i in range(0, len(l), n)] 

# find all files and group by specimen
files = [x for x in pathlib.Path('data').glob('**/*')] # list all in data folder
files = chunks((sorted(files)),3) # sort by specimen and group into 3s

# combine all files into one wide dataframe
df = pd.DataFrame()
for files_sub in files:
    df_sub = pd.concat([pd.read_csv(f).assign(name=f.stem.rsplit('-',1)[0].split('_')[0]) for f in files_sub], axis= 1)
    df = pd.concat([df,df_sub], axis=0)
df = df.set_index('name')

# index is 3-tuple for some reason instead of string, fix this
indx = [i[0] for i in df.index]
df.index = indx

# add in depth for all 8 specimens 
df.insert(0,'depth',(['0-5','5-10','10-15','15-20','20-25','25-30','30-35','35-40']*8))

# reduce all specimens into just average
df = df.groupby('depth',sort=False).mean()

# concatenate into 3-tuple of all specimens
i = 0
df_comb = pd.DataFrame()
for x in range(3,len(df.columns)+3, 3):
    col_name = str(df.iloc[:,i:x].columns[0])
    sub = df.iloc[:,i:x].apply(tuple,axis=1).rename(col_name)
    df_comb = pd.concat([df_comb,sub.reset_index(drop=True)], axis=1)
    i=x
df_comb.columns = df_comb.columns.str.rstrip('Above Threshold')
df_comb['depth'] = ['0-5','5-10','10-15','15-20','20-25','25-30','30-35','35-40']
df_comb = df_comb.set_index('depth')

# stack and explode the 3-tuple into individual columns
df = df_comb.stack()
df = df.reset_index()
df = df.rename(columns={'level_1':'id', 0:'val'})
df[['remodel','unchanged','resorb']] = pd.DataFrame(df['val'].to_list(), index=df.index)
df = df.drop('val', axis=1)

# label quadrants
conditions = [
    (df['id'].str.contains('Lateral')),
    (df['id'].str.contains('Medial')),
    (df['id'].str.contains('Anterior')),
    (df['id'].str.contains('Posterior'))]
choices = ['Lateral','Medial','Anterior','Posterior']
df['quad'] = np.select(conditions, choices)

# label bone types
conditions = [
    (df['id'].str.contains('Cortical')),
    (df['id'].str.contains('Trabecular'))]
choices = ['Cortical','Trabecular']
df['bone_type'] = np.select(conditions, choices)

# label load angle
conditions = [
    (df['id'].str.contains('45')),
    (df['id'].str.contains('75'))   
]
choices = ['45','75']
df['load'] = np.select(conditions, choices)

# label implant angle
conditions = [
    (df['id'].str.contains('STD')),
    (df['id'].str.contains('INF')),
    (df['id'].str.contains('SUP'))   
]
choices = ['STD','INF','SUP']
df['posi'] = np.select(conditions, choices)

# df.to_csv('data.csv')
# print(df)

# build graphs
df_graph = df[(df['posi'] == 'STD') & (df['bone_type'] == 'Cortical') & (df['load'] == '45')]
fig = px.bar_polar(df_graph, r="resorb", theta="quad",
                   color="depth", template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Plasma_r)
fig.show()
