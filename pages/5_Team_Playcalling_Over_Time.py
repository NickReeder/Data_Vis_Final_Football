from __future__ import annotations
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
from plotly.colors import n_colors
from plotly.subplots import make_subplots

from src.football_db import FootballDB

FDB = FootballDB()

def build_plots(team):

    rush = FDB.get_tRush()
    rush = rush[rush['offense']==team]
    throw = FDB.get_tPass()
    throw = throw[throw['offense']==team]
    game = FDB.get_tGame()

    merged_throw = throw.merge(game, left_on='game_id', right_on='game_id')
    merged_rush = rush.merge(game, left_on='game_id', right_on='game_id')

    throw_totals = []
    rush_totals = []
    pa_totals = []
    sc_totals = []
    seasons = merged_throw['season'].unique()
    for i in seasons:

    # THROW totals
        throw_idx_szn = merged_throw['season'] == i
        throw_totals.append(len(merged_throw[throw_idx_szn]))

        #pa + sc total
        throw_szn = merged_throw[throw_idx_szn]
        pa_idx = throw_szn['play_action'] == 1
        sc_idx = throw_szn['screen'] == 1
        pa_totals.append(len(throw_szn[pa_idx]))
        sc_totals.append(len(throw_szn[sc_idx]))

        rush_idx_szn = merged_rush['season'] == i
        rush_totals.append(len(merged_rush[rush_idx_szn]))

    df = pd.DataFrame()
    df['Season'] = seasons
    df['Throws'] = throw_totals
    df['Rushes'] = rush_totals
    df['Screens'] = sc_totals
    df['Play_Action'] = pa_totals

    y_data_1 = np.array([
        df['Throws'],
        df['Rushes']
    ])

    y_data_2 = np.array([
        df['Screens'],
        df['Play_Action']
    ])

    colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
    line_size = [2, 2, 4, 2]
    mode_size = [8, 8, 12, 8]
    labels = ['Passes', 'Rushes']
    labels_2 = ['Screen', 'Play Action']

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(x= df['Season'], y= df['Play_Action'], mode='lines',
            name= 'Play Action',
            line=dict(color=colors[1], width=line_size[0]),
            connectgaps=True,
            hovertemplate=
            "Plays: %{y:,}<br>" +
            "<extra></extra>"
        ))

    fig1.add_trace(go.Scatter(
        x=[df['Season'][0], df['Season'][0]],
        y=[df['Play_Action'][0], df['Play_Action'][0]],
        mode='markers',
        marker=dict(color=colors[1], size=mode_size[0]),
        hovertemplate=
            "Plays: %{y:,}<br>" +
            "<extra></extra>"
        ))

    fig1.add_trace(go.Scatter(x= df['Season'], y= df['Screens'], mode='lines',
            name= 'Throws',
            line=dict(color=colors[2], width=line_size[0]),
            connectgaps=True,
            hovertemplate=
            "Plays: %{y:,}<br>" +
            "<extra></extra>"
        ))

    fig1.add_trace(go.Scatter(
        x=[df['Season'][0], df['Season'][0]],
        y=[df['Screens'][0], df['Screens'][0]],
        mode='markers',
        marker=dict(color=colors[2], size=mode_size[0]),
        hovertemplate=
            "Plays: %{y:,}<br>" +
            "<extra></extra>"
        ))

    fig1.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            showticklabels=True,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    for y_trace, label, color in zip(y_data_2, labels_2, colors):

        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.1, y=y_trace[0] + 5,
                                    xanchor='right', yanchor='middle',
                                    text = label,

                                    font=dict(family='Arial',
                                                size=12),
                                    showarrow=False))

    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                xanchor='left', yanchor='bottom',
                                text='Total Play Action and Screen Plays by Season',
                                font=dict(family='Arial',
                                            size=20,
                                            color='rgb(37,37,37)'),
                                showarrow=False))

    fig1.update_layout(annotations=annotations)

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x= df['Season'], y= df['Throws'], mode='lines',
            name= 'Throws',
            line=dict(color=colors[0], width=line_size[0]),
            connectgaps=True,
        ))

    fig2.add_trace(go.Scatter(
        x=[df['Season'][0], df['Season'][0]],
        y=[df['Throws'][0], df['Throws'][0]],
        mode='markers',
        marker=dict(color=colors[0], size=mode_size[0])
        ))


    fig2.add_trace(go.Scatter(x= df['Season'], y= df['Rushes'], mode='lines',
            name= 'Rushes',
            line=dict(color=colors[3], width=line_size[0]),
            connectgaps=True,
        ))

    fig2.add_trace(go.Scatter(
        x=[df['Season'][0], df['Season'][0]],
        y=[df['Rushes'][0], df['Rushes'][0]],
        mode='markers',
        marker=dict(color=colors[3], size=mode_size[0])
        ))

    fig2.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            showticklabels=True,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    for y_trace, label, color in zip(y_data_1, labels, colors):

        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.1, y=y_trace[0] + 10,
                                    xanchor='right', yanchor='middle',
                                    text = label,

                                    font=dict(family='Arial',
                                                size=12),
                                    showarrow=False))


    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                xanchor='left', yanchor='bottom',
                                text='Total Plays by Season',
                                font=dict(family='Arial',
                                            size=20,
                                            color='rgb(37,37,37)'),
                                showarrow=False))

    fig2.update_layout(annotations=annotations)

    return fig1, fig2


team_list = ['ARZ','ATL','BLT','BUF','CAR','CHI','CIN','CLV','DAL','DEN','DET',
 'GB','HST','IND','JAX','KC','LV','LAC','LA','MIA','MIN','NE','NO',
 'NYG','NYJ','PHI','PIT','SF','SEA','TB','TEN','WAS']

team = st.sidebar.selectbox('Select Team',team_list)
fig1, fig2 = build_plots(team = team)

st.plotly_chart(fig1)
st.plotly_chart(fig2)

