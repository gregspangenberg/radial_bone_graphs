from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# load in data 
df = pd.read_csv('data.csv')

# rename legend
df = df.rename(columns={'depth':'Depth [mm]'})

# dash automatically loads in any js, or css in /assets folder
app = Dash(__name__)

app.layout = html.Div([
    # dropdown menus
    html.Div([
        html.Div([
            dcc.Dropdown(
                df['posi'].unique(),
                'STD',
                id='position',
            )],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                df['load'].unique(),
                '45',
                id='load'
            )], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={'padding': '10px 5px'}),

    # graphs
    html.Div([
        dcc.Graph(id='cort-remodel'),
        dcc.Graph(id='trab-remodel'),
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='cort-resorp'),
        dcc.Graph(id='trab-resorp'),
    ], style={'display': 'inline-block', 'width': '49%'})
    ])


@app.callback(
    Output('cort-remodel', 'figure'),
    Input('position', 'value'),
    Input('load', 'value'))
def remodel_cort(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Cortical') ]
    fig = px.bar_polar(df_graph, r="remodel", theta="quad", color="Depth [mm]",
                        range_r = [0, 2.25],
                        title = 'Cortical Remodelling',
                        template="ggplot2",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    return fig

@app.callback(
    Output('cort-resorp','figure'),
    Input('position', 'value'),
    Input('load', 'value'))
def resorp_cort(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Cortical') ]
    fig = px.bar_polar(df_graph, r="resorp", theta="quad", color="Depth [mm]",
                        range_r = [0, 5.5],
                        title = 'Cortical Resorption',
                        template="ggplot2",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    return fig

@app.callback(
    Output('trab-remodel','figure'),
    Input('position', 'value'),
    Input('load', 'value'))
def remodel_trab(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Trabecular') ]
    fig = px.bar_polar(df_graph, r="remodel", theta="quad", color="Depth [mm]",
                        range_r = [0, 5],
                        title = 'Trabecular Remodelling',
                        template="ggplot2",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    return fig

@app.callback(
    Output('trab-resorp','figure'),
    Input('position', 'value'),
    Input('load', 'value'))
def resorp_trab(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Trabecular') ]
    fig = px.bar_polar(df_graph, r="resorp", theta="quad", color="Depth [mm]",
                        range_r = [0, 3.25],
                        title = 'Trabecular Resorption',
                        template="ggplot2",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    return fig




if __name__ == '__main__':
    app.run_server()#debug=True)