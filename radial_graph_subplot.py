import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import plotly.io as pio

import pandas as pd


def radial(df, implant_dir, load_dir):
    # create plots, 4 are needed for each orientation
    # cortical remodelling
    df_graph = df[(df['posi'] == implant_dir) & (df['bone_type'] == 'Cortical') & (df['load'] == load_dir)]
    fig1 = px.bar_polar(df_graph, r="remodel", theta="quad", color="depth",
                        title = 'Cortical Remodelling',
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Viridis_r)
    # trabecular remodelling
    df_graph = df[(df['posi'] == implant_dir) & (df['bone_type'] == 'Trabecular') & (df['load'] == load_dir)]
    fig2 = px.bar_polar(df_graph, r="remodel", theta="quad", color="depth",
                        title = 'Trabecular Remodelling',
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Viridis_r)
    # cortical resorption
    df_graph = df[(df['posi'] == implant_dir) & (df['bone_type'] == 'Cortical') & (df['load'] == load_dir)]
    fig3 = px.bar_polar(df_graph, r="resorp", theta="quad", color="depth",
                        title = 'Cortical Resorption',
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Viridis_r)

    # trabecular resorption
    df_graph = df[(df['posi'] == implant_dir) & (df['bone_type'] == 'Trabecular') & (df['load'] == load_dir)]
    fig4 = px.bar_polar(df_graph, r="resorp", theta="quad", color="depth",
                        title = 'Trabecular Resorption',
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Viridis_r)


    # For as many traces that exist per Express figure, get the traces from each plot and store them in an array.
    # This is essentially breaking down the Express fig into it's traces
    fig1_traces = []
    fig2_traces = []
    fig3_traces = []
    fig4_traces = []
    for trace in range(len(fig1["data"])):
        fig1_traces.append(fig1["data"][trace])
    for trace in range(len(fig2["data"])):
        fig2["data"][trace]['showlegend'] = False # removes extra legends
        fig2_traces.append(fig2["data"][trace])
    for trace in range(len(fig3["data"])):
        fig3["data"][trace]['showlegend'] = False # removes extra legends
        fig3_traces.append(fig3["data"][trace])
    for trace in range(len(fig4["data"])):
        fig4["data"][trace]['showlegend'] = False # removes extra legends
        fig4_traces.append(fig4["data"][trace])

    big_fig = sp.make_subplots(rows=2, cols=2, specs=[[{'type': 'polar'}]*2]*2,
        # subplot_titles=['Cortical Remodelling','Cortical Resorption','Trabecular Remodelling','Trabecular Resorption'],
        column_titles=['Remodelling','Resorption'],row_titles=['Cortical','Trabecular'],
        horizontal_spacing=0.18, vertical_spacing=0.05
    ) 

    # Get the Express fig broken down as traces and add the traces to the proper plot within in the subplot
    for traces in fig1_traces:
        big_fig.append_trace(traces, row=1, col=1)
    for traces in fig2_traces:
        big_fig.append_trace(traces, row=2, col=1)
    for traces in fig3_traces:
        big_fig.append_trace(traces, row=1, col=2)
    for traces in fig4_traces:
        big_fig.append_trace(traces, row=2, col=2)

    # reposition titles
    for i in range(4):
        big_fig.layout.annotations[i].update(xanchor = 'center')
        big_fig.layout.annotations[i].update(yanchor = 'middle')
    # # big_fig.layout.annotations[0].update(xanchor='auto')
    # # big_fig.layout.annotations[0].update(y = 0.99)
    # # big_fig.layout.annotations[1].update(y = 0.99)
    big_fig.layout.annotations[2].update(x = 0.5)
    big_fig.layout.annotations[3].update(x= 0.5)


    # update layout
    big_fig.update_layout(
        legend = dict(
            orientation="h",
            yanchor="bottom",
            y=-0.02,
            xanchor="right",
            x=1
        ),
        # Cortical Remodelling
        polar = dict(
            hole = 0.1,
            bargap = 0.15,
            radialaxis_angle = -40,
            radialaxis_range = [0, 2.25]
        ),
        # Cortial Resorption
        polar2 = dict(
            hole = 0.1,
            bargap = 0.15,
            radialaxis_angle = -40,
            radialaxis_range = [0, 5.5]
        ),
        # Trabecular Remodelling
        polar3 = dict(
            hole = 0.1,
            bargap = 0.15,
            radialaxis_angle = -40,
            radialaxis_range = [0, 5.5]
        ),
        # Trabecular Resorption
        polar4 = dict(
            hole = 0.1,
            bargap = 0.15,
            radialaxis_angle = -40,
            radialaxis_range = [0, 3.25]
        ),
    )
    return big_fig

# load in data 
df = pd.read_csv('data.csv')

for posi in ['STD','INF','SUP']:
    for load in [45, 75]:
        fig = radial(df, implant_dir=posi, load_dir=load)
        pio.write_image(fig, f'figs/{posi}-{load}.png', width=1.2*1000, height=1.2*1000, scale=5)


# big_fig.show()
