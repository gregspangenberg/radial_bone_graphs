from turtle import width
import plotly.express as px
import plotly.io as pio
import pandas as pd

# load in data 
df = pd.read_csv('data.csv')

# rename legend
df = df.rename(columns={'depth':'Depth [mm]'})

def remodel_cort(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Cortical') ]
    fig = px.bar_polar(df_graph, r="remodel", theta="quad", color="Depth [mm]",
                        range_r = [0, 2.25],
                        # title = 'Cortical Remodelling',
                        template="ggplot2",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    fig.update_layout(showlegend=False)
    fig_name = f'remodel_cort-{position}-{str(load_dir)}'
    return fig, fig_name

def resorp_cort(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Cortical') ]
    fig = px.bar_polar(df_graph, r="resorp", theta="quad", color="Depth [mm]",
                        range_r = [0, 5.5],
                        # title = 'Cortical Resorption',
                        template="ggplot2",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    fig.update_layout(showlegend=False)
    fig_name = f'resorp_cort-{position}-{str(load_dir)}'
    return fig, fig_name


def remodel_trab(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Trabecular') ]
    fig = px.bar_polar(df_graph, r="remodel", theta="quad", color="Depth [mm]",
                        range_r = [0, 5.5],
                        # title = 'Trabecular Remodelling',
                        template="ggplot2",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    fig.update_layout(showlegend=False)
    fig_name = f'remodel_trab-{position}-{str(load_dir)}'
    return fig, fig_name

def resorp_trab(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Trabecular') ]
    fig = px.bar_polar(df_graph, r="resorp", theta="quad", color="Depth [mm]",
                        range_r = [0, 3.25],
                        # title = 'Trabecular Resorption',
                        template="ggplot2",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    fig.update_layout(showlegend=False)
    fig_name = f'resorp_trab-{position}-{str(load_dir)}'
    return fig, fig_name
for posi in ['STD','SUP','INF']:
    for load in [45,75]:
        fig,name = remodel_cort(posi, load)
        # fig.write_image(f'figs/{name}.png', scale=10)
        pio.write_image(fig, f'figs/{name}.png', width=1*1000, height=1*1000, scale=5)

        fig,name = resorp_cort(posi, load)
        # fig.write_image(f'figs/{name}.png', scale=10)
        pio.write_image(fig, f'figs/{name}.png', width=1*1000, height=1*1000, scale=5)
        
        
        fig,name = remodel_trab(posi, load)
        # fig.write_image(f'figs/{name}.png', scale=10)
        pio.write_image(fig, f'figs/{name}.png', width=1*1000, height=1*1000, scale=5)
        
        
        fig,name = resorp_trab(posi, load)
        # fig.write_image(f'figs/{name}.png', scale=10)
        pio.write_image(fig, f'figs/{name}.png', width=1*1000, height=1*1000, scale=5)
        