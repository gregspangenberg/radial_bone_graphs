from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

import pandas as pd
import numpy as np

# load in data 
df = pd.read_csv('data.csv')

# create plots, 4 are needed for each orientation
load_dir = 45
implant_dir = 'STD'
# cortical remodelling
df_graph = df[(df['posi'] == implant_dir) & (df['bone_type'] == 'Cortical') & (df['load'] == load_dir)]
fig1 = px.bar_polar(df_graph, r="remodel", theta="quad",
                   color="depth", template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Plasma_r)
# trabecular remodelling
df_graph = df[(df['posi'] == implant_dir) & (df['bone_type'] == 'Trabecular') & (df['load'] == load_dir)]
fig2 = px.bar_polar(df_graph, r="remodel", theta="quad",
                   color="depth", template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Plasma_r)
# cortical resorption
df_graph = df[(df['posi'] == implant_dir) & (df['bone_type'] == 'Cortical') & (df['load'] == load_dir)]
fig3 = px.bar_polar(df_graph, r="resorp", theta="quad",
                   color="depth", template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Plasma_r)
# trabecular resorption
df_graph = df[(df['posi'] == implant_dir) & (df['bone_type'] == 'Trabecular') & (df['load'] == load_dir)]
fig4 = px.bar_polar(df_graph, r="resorp", theta="quad",
                   color="depth", template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Plasma_r)

# For as many traces that exist per Express figure, get the traces from each plot and store them in an array.
# This is essentially breaking down the Express fig into it's traces
fig1_traces = []
fig2_traces = []
fig3_traces = []
fig4_traces = []
for trace in range(len(fig1["data"])):
    fig1_traces.append(fig1["data"][trace])
for trace in range(len(fig2["data"])):
    fig2_traces.append(fig2["data"][trace])
for trace in range(len(fig3["data"])):
    fig3_traces.append(fig3["data"][trace])
for trace in range(len(fig4["data"])):
    fig4_traces.append(fig4["data"][trace])

big_fig = sp.make_subplots(rows=2, cols=2, specs=[[{'type': 'polar'}]*2]*2) 

# Get the Express fig broken down as traces and add the traces to the proper plot within in the subplot
for traces in fig1_traces:
    big_fig.append_trace(traces, row=1, col=1)
for traces in fig2_traces:
    big_fig.append_trace(traces, row=2, col=1)
for traces in fig3_traces:
    big_fig.append_trace(traces, row=1, col=2)
for traces in fig4_traces:
    big_fig.append_trace(traces, row=2, col=2)

big_fig.show()