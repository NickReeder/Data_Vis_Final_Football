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

def get_defensive_stats(team, df, verbose = False):
  import numpy as np

  '''
  Inputs: DataFrame, Team, Verbose (optional)
    If verbose = True, prints number of plays to analyze
  Outputs: Dictionary of stats

  Takes a dataframe, subsets it, and devlops defensive stats for the specified team. Stats returned are:
  avg_yards_conceded: average yards conceded per play
  median_yards_conceded: median yards conceded per play
  first_down_efficency: 1 - (first downs allowed / number of plays)
  first_down_on_fourth_effic: 1 - (first downs allowed on fourth down / number of of fourth downs)
  '''


  if team not in df['defense'].unique():
      print('Input defense is not in our data, please check spelling at try again')
      return()

  team_df = df[df['defense'] == team]

  num_plays = len(team_df)
  if verbose == True:
    print('there are', num_plays, 'to analyze')

  avg_yards_conceded = np.mean(team_df['yards_gained'])
  median_yards_conceded = np.median(team_df['yards_gained'])
  try:
    first_down_efficency = team_df['first_down_conv'].value_counts()['Y'] / num_plays
  except KeyError:
    first_down_efficency = 0



  four_d = team_df[team_df['down'] == 4]
  num_four_d = len(four_d)
  try:
    first_down_on_fourth_effic = four_d['first_down_conv'].value_counts()['Y'] / num_four_d
  except KeyError:
    first_down_on_fourth_effic = 0

  stats_dict = {'avg_yards_conceded': round(avg_yards_conceded, 3),
                'median_yards_conceded': median_yards_conceded,
                'first_down_efficency': round(1 - first_down_efficency, 5),
                'first_down_on_fourth_effic': round(1 - first_down_on_fourth_effic, 5)
                }

  return(stats_dict)




  ######################################################################################


def get_offensive_stats(team, df, verbose = False):
  import numpy as np


  '''
  Inputs: DataFrame, Team, Verbose (optional)
    If verbose = True, prints number of plays to analyze
  Outputs: Dictionary of stats

  Takes a dataframe, subsets it, and devlops offensive stats for the specified team. Stats returned are:
  avg_yards: average yards gained per play
  first_down_efficency: first downs / number of plays
  first_down_on_fourth_effic: first downs allowed on fourth down / number of of fourth downs

  '''


  if team not in df['offense'].unique():
      print('Input offense is not in our data, please check spelling at try again')
      return()
  rush_team = df[df['offense'] == team]

  if 'yards_gained' not in rush_team.columns:
      print('No yards gained found, please ensure you are using the correct dataframe')
      return()

  num_plays = len(rush_team)
  if verbose == True:
    print('there are', num_plays, 'to analyze')

  avg_yard = np.mean(rush_team['yards_gained'])

  median_yard = np.median(rush_team['yards_gained'])
  try:
    fd_effic = rush_team['first_down_conv'].value_counts()['Y'] / num_plays
  except KeyError:
    fd_effic = 0
  avg_yard = np.mean(rush_team['yards_gained'])


  four_d = rush_team[rush_team['down'] == 4]
  num_four_d = len(four_d)
  try:
    first_down_on_fourth_effic = four_d['first_down_conv'].value_counts()['Y'] / num_four_d
  except KeyError:
    first_down_on_fourth_effic = 0


  stats_dict = {'avg_yard': np.round(avg_yard, 3),
                'median_yard': median_yard,
                'fd_effic': np.round(fd_effic, 5),
                'first_down_on_fourth_effic': np.round(first_down_on_fourth_effic, 5)
              }
  return(stats_dict)


##################################################

def get_offensive_dict(df):

  '''
  Inputs: a pandas dataframe
  Outputs: a dictionary of offensive stats for each team

  Generates a dictionary of offensive stats for each team in the dataset
  '''
  output = {}

  for team in df['offense'].unique():
    output[team] = get_offensive_stats(team, df)

  return(output)


####################################


def get_defensive_dict(df):
  output = {}

  for team in df['defense'].unique():
    output[team] = get_defensive_stats(team, df)

  return(output)

###################################


def get_off_stats_against(offense, defense, df, verbose = False):
  '''
  Inputs: offense, defense, dataframe
  Outputs: dictionary of offensive stats against that specfic team
  '''

  if offense not in df['offense'].unique():
      print('Input offense is not in our data, please check spelling at try again')
      return()
  if defense not in df['defense'].unique():
      print('Input defense is not in our data, please check spelling at try again')
      return()



  df_off = df[df['offense'] == offense]

  df_combo = df[(df['offense'] == offense) & (df['defense'] == defense)]

  if len(df_combo) == 0:
    if verbose:
      print('No data for', offense, 'against', defense)
    return()
  else:
    stats_dict = get_offensive_stats(offense, df_combo)

  return(stats_dict)


#########################

def get_def_stats_against(offense, defense, df, verbose = False):
  '''
  Inputs: offense, defense, dataframe
  Outputs: dictionary of defensive stats against that specfic team
  '''

  if offense not in df['offense'].unique():
      print('Input offense is not in our data, please check spelling at try again')
      return()
  if defense not in df['defense'].unique():
      print('Input defense is not in our data, please check spelling at try again')
      return()



  df_combo = df[(df['offense'] == offense) & (df['defense'] == defense)]

  if len(df_combo) == 0:
    if verbose:
      print('No data for', offense, 'against', defense)
    return()
  else:
    stats_dict = get_defensive_stats(defense, df_combo)

  return(stats_dict)

#########################################


def get_offensive_dict_against(offense, df):
  '''
  Inputs: offense, dataframe
  Outputs: dictionary of offensive stats against each team
  '''

  if offense not in df['offense'].unique():
      print('Input offense is not in our data, please check spelling at try again')
      return()


  output = {}

  for team in df['defense'].unique():
    output[team] = get_off_stats_against(offense, team, df)

  return(output)


####################################


def get_defensive_dict_against(defense, df):
  '''
  Inputs: defense, dataframe
  Outputs: dictionary of defensive stats against each team
  '''

  if defense not in df['defense'].unique():
      print('Input defense is not in our data, please check spelling at try again')
      return()

  output = {}

  for team in df['offense'].unique():
    output[team] = get_def_stats_against(team, defense, df)

  return(output)

throw = FDB.get_tPass()
game = FDB.get_tGame()

selected = ['ARZ','ATL','BLT','BUF','CAR','CHI','CIN','CLV','DAL','DEN','DET',
 'GB','HST','IND','JAX','KC','LV','LAC','LA','MIA','MIN','NE','NO',
 'NYG','NYJ','PHI','PIT','SF','SEA','TB','TEN','WAS']

def Ridgeline(stat, year):

  if stat == 'Touchdown':
    stat = 0
  elif stat == 'Screen Pass':
    stat = 1
  elif stat == 'Play Action Pass':
    stat = 2

  options = ['touchdown','screen','play_action']

  fig = go.Figure()
  n = 0

  merged_throw = throw.merge(game, left_on='game_id', right_on='game_id')
  throw_year = merged_throw[merged_throw['season'] == int(year)]

  stat_frame = throw_year[throw_year[options[stat]] == 1.0]

  avg_stat = stat_frame.groupby('offense')['yards'].mean()
  sorted_stat_teams = avg_stat.sort_values().index.tolist()


  for i in sorted_stat_teams:

    selected_frame = stat_frame[stat_frame['offense'] == i]

    tx = selected_frame['offense']
    ty = selected_frame['yards']

    colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', 48, colortype='rgb')

    fig.add_trace(go.Violin(x= ty, line_color=colors[n], name = i))


    n += 1


  fig.update_traces(orientation='h', side='positive', width=3, points=False, showlegend = False)

  if stat == 0:
    phrase = 'TD Pass Yards'
  if stat == 1:
    phrase = 'Screen Pass Yards'
  if stat == 2:
    phrase = 'Play Action Pass Yards'

  fig.update_layout(xaxis_title = 'Yards', yaxis_title = 'Teams',title = {'text':'Distribution of ' + phrase + ' For ' + str(year) + ' Season By Team', 'font':{'size':20},'x':0.01},xaxis_showgrid=False, xaxis_zeroline=False, height = 1000, width = 800)
  fig.update_xaxes(range=[-20, 110])


  fig.update_layout(shapes=[
          dict(type='line', x0=-15, y0=-0.5, x1=100, y1=-0.5, line=dict(color='grey'))])
  fig.add_vline(x = 0, line_color = 'gray', line_dash = 'dash',
               opacity = 0.7,  annotation_text = '0 yds', annotation_position="top")
  fig.add_vline(x = 10, line_color = 'gray', line_dash = 'dash',
               opacity = 0.7,  annotation_text = '10 yds', annotation_position="top")
  
  fig.update_layout(height=1000, width=600)

  return fig

stat = st.sidebar.selectbox('Select Statistic', ['Touchdown','Screen Pass','Play Action Pass'])
year = st.sidebar.selectbox('Select Season', ['2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'])

st.plotly_chart(Ridgeline(stat=stat, year=year))