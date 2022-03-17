from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# load in data 
df = pd.read_csv('data.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

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
    fig = px.bar_polar(df_graph, r="remodel", theta="quad", color="depth",
                        title = 'Cortical Remodelling',
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    return fig

@app.callback(
    Output('cort-resorp','figure'),
    Input('position', 'value'),
    Input('load', 'value'))
def resorp_cort(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Cortical') ]
    fig = px.bar_polar(df_graph, r="resorp", theta="quad", color="depth",
                        title = 'Cortical Resorption',
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    return fig

@app.callback(
    Output('trab-remodel','figure'),
    Input('position', 'value'),
    Input('load', 'value'))
def remodel_trab(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Trabecular') ]
    fig = px.bar_polar(df_graph, r="remodel", theta="quad", color="depth",
                        title = 'Trabecular Remodelling',
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    return fig

@app.callback(
    Output('trab-resorp','figure'),
    Input('position', 'value'),
    Input('load', 'value'))
def resorp_trab(position,load_dir):
    df_graph = df[(df['posi'] == position) & (df['load'] == int(load_dir)) & (df['bone_type'] == 'Trabecular') ]
    fig = px.bar_polar(df_graph, r="resorp", theta="quad", color="depth",
                        title = 'Trabecular Resorption',
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Plasma_r)
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)