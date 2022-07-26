import plotly.express as px
import plotly.subplots as sp
import pandas as pd

def radial_integ(df, implant_dir, load_dir):

    # create 2 plots with cortical and trabecular integrated into one
    # remodelling
    df_graph = df[(df['posi'] == implant_dir)  & (df['load'] == load_dir)]
    fig1 = px.bar_polar(df_graph, r="remodel", theta="rad_loc_off", color="depth",
                        pattern_shape= 'bone_type',
                        barmode='group',
                        title = 'Remodelling',
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Viridis_r)
    # cortical resorption
    df_graph = df[(df['posi'] == implant_dir) & (df['load'] == load_dir)]
    fig2 = px.bar_polar(df_graph, r="resorp", theta="rad_loc_off", color="depth",
                        pattern_shape= 'bone_type',
                        barmode='group',
                        title = 'Resorption',
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Viridis_r)
   
    # For as many traces that exist per Express figure, get the traces from each plot and store them in an array.
    # This is essentially breaking down the Express fig into it's traces
    fig1_traces = []
    fig2_traces = []
    for trace in range(len(fig1["data"])):
        fig1_traces.append(fig1["data"][trace])
    for trace in range(len(fig2["data"])):
        fig2["data"][trace]['showlegend'] = False # removes extra legends
        fig2_traces.append(fig2["data"][trace])
    
    big_fig = sp.make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2],
        # subplot_titles=['Cortical Remodelling','Cortical Resorption','Trabecular Remodelling','Trabecular Resorption'],
        column_titles=['Remodelling','Resorption'],
        horizontal_spacing=0.18
    ) 
    # Get the Express fig broken down as traces and add the traces to the proper plot within in the subplot
    for traces in fig1_traces:
        big_fig.append_trace(traces, row=1, col=1)
    for traces in fig2_traces:
        big_fig.append_trace(traces, row=1, col=2)
    # reposition titles
    for i in range(2):
        big_fig.layout.annotations[i].update(xanchor = 'center')
        big_fig.layout.annotations[i].update(yanchor = 'middle')
    
        # update layout
    big_fig.update_layout(
        height=800,
        width=1200,
        title_text = implant_dir,
        title_x=0.5,

        legend = dict(
            orientation="h",
            yanchor="bottom",
            y=-0.02,
            xanchor="right",
            x=1.05,
            font=dict(size= 8),
        ),
        # Remodelling
        polar = dict(
            hole = 0.1,
            bargap = 0.0,
            radialaxis = dict(
                angle=-45,
                range= [0,5],
                tickformat = '.1%'
            ),
            angularaxis = dict(
                thetaunit = "degrees",
                dtick = 45,
                rotation=0,
                direction = "counterclockwise",
                tickmode="array",
                tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                ticktext=["Anterior", "", "Lateral", "", "Posterior", "", "Medial", ""]
                )
        ),
        # Resorption
        polar2 = dict(
            hole = 0.1,
            bargap = 0.0,
            radialaxis = dict(
                angle=-45,
                range= [0,5],
                tickformat = '.1%'
            ),
            angularaxis = dict(
                thetaunit = "degrees",
                dtick = 45,
                rotation=0,
                direction = "counterclockwise",
                tickmode="array",
                tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                ticktext=["Anterior", "", "Lateral", "", "Posterior", "", "Medial", ""]
                )
        ),
    )

    return big_fig

# load in data 
df = pd.read_csv('data.csv')

# offset rad_loc -45 for cortical and +45 for trabecular
# df['rad_loc_off'] = df.apply(lambda x: x['rad_loc']+22.5 if x['bone_type']=='Cortical' else x['rad_loc']-22.5, axis=1)
df['rad_loc_off'] = df.apply(lambda x: x['rad_loc']+22.5 if x['bone_type']=='Cortical' else x['rad_loc']-20, axis=1)
print(df)


# print(df)
for posi in ['STD','INF','SUP']:
    # for load in [45, 75]:
    for load in [45]:
        fig = radial_integ(df, implant_dir=posi, load_dir=load)
        # pio.write_image(fig, f'figs/{posi}-{load}.png', width=1.2*1000, height=1.2*1000, scale=5)
        fig.show()
