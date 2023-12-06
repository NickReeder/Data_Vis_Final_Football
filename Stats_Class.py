import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import json

path = 'c:\\Users\\Nick\\Dropbox\\PC\\Documents\\GitHub\\DATA_VIS_FINAL_FOOTBALL'

#path = '/content/drive/My Drive/WM_Football_Independent_Study'




from tqdm import tqdm



class Stats:

  def __init__(self):

    print('Building stats objects')
    # ans = None
    # while ans not in ['Y', 'N']:
    #   ans = input('Is Data base built [Y/N]')
    # if ans == 'N':

    #   path = input('Enter path to SRC ')
    #   os.chdir(path)

    #   from src.football_db import FootballDB
    #   import src.dropdown_lists as dropdown


    #   from src.football_viz import FBField
    #   from src.football_db import FootballDB
    #   self.db = FootballDB()
    # else:
    #   print(os.getcwd())
    #   ans_2 = input('Please enter path to db ')
    

    
    from src.football_db import FootballDB
    import src.dropdown_lists as dropdown


    #from src.football_viz import FBField
    from src.football_db import FootballDB
    self.db = FootballDB()
    
    self.set_up = False

    self.rush = self.db.get_tRush()
    self.throw = self.db.get_tPass()

    self.rush_off = self.rush['offense'].unique()
    self.rush_def = self.rush['defense'].unique()
    self.throw_off = self.throw['offense'].unique()
    self.throw_def = self.throw['defense'].unique()
    self.dict_of_teams = None

    #Checking all teams are shared

    #print('Checking rush offense')
    for team in tqdm(self.rush_off, desc = 'Checking rush offense'):
      if team not in self.throw_off:
        print(team, 'not in passing offense')
      if team not in self.throw_def:
        print(team, 'not in passing defense')
      if team not in self.rush_def:
        print(team, 'not in rushing defense')

    #print('Checking rush defense')
    for team in tqdm(self.rush_def, desc = 'Checking rush defense'):
      if team not in self.throw_off:
        print(team, 'not in passing offense')
      if team not in self.throw_def:
        print(team, 'not in passing defense')
      if team not in self.rush_off:
        print(team, 'not in rushing offense')

    #print('Checking passing offense')
    for team in tqdm(self.throw_off, desc = 'Checking passing offense'):
      if team not in self.rush_off:
        print(team, 'not in rushing offense')
      if team not in self.throw_def:
        print(team, 'not in passing defense')
      if team not in self.rush_def:
        print(team, 'not in rushing defense')

    #print('Checking passing offense')
    for team in tqdm(self.throw_def, desc = 'Checking passing defense'):
      if team not in self.rush_off:
        print(team, 'not in rushing offense')
      if team not in self.throw_off:
        print(team, 'not in passing offense')
      if team not in self.rush_def:
        print(team, 'not in rushing defense')







  #####FUNCTIONS#####

  def get_defensive_stats(self, team, df, play_type, verbose = False):
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


    if play_type == 'pass':
      turnover_pct = np.nansum(team_df['turnover_worthy_play'])/num_plays
    else:
      turnover_pct = np.nansum(team_df['fumbles'])/num_plays

    stats_dict = {'avg_yards_conceded': str(round(avg_yards_conceded, 3)),
                  'median_yards_conceded': str(median_yards_conceded),
                  'first_down_efficency': str(round(1 - first_down_efficency, 5)),
                  'first_down_on_fourth_effic': str(round(1 - first_down_on_fourth_effic, 5)),
                  'turnover_pct': str(round(1 - turnover_pct, 5))
                  }

    return(stats_dict)




    ######################################################################################


  def get_offensive_stats(self, team, df, play_type, verbose = False):
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



    if play_type == 'pass':
      #print(rush_team['interception'])
      turnover_pct = np.nansum(rush_team['turnover_worthy_play'])/num_plays
    else:
      turnover_pct = np.nansum(rush_team['fumbles'])/num_plays


    stats_dict = {'avg_yard': str(np.round(avg_yard, 3)),
                  'median_yard': str(median_yard),
                  'fd_effic': str(np.round(fd_effic, 5)),
                  'first_down_on_fourth_effic': str(np.round(first_down_on_fourth_effic, 5)),
                  'turnover_pct': str(np.round(turnover_pct, 5))
                }
    return(stats_dict)


  ##################################################

  def get_offensive_dict(self, df):

    '''
    Inputs: a pandas dataframe
    Outputs: a dictionary of offensive stats for each team

    Generates a dictionary of offensive stats for each team in the dataset
    '''
    output = {}

    for team in df['offense'].unique():
      output[team] = self.get_offensive_stats(team, df)

    return(output)


  ####################################


  def get_defensive_dict(self, df):
    output = {}

    for team in df['defense'].unique():
      output[team] = self.get_defensive_stats(team, df)

    return(output)

  ###################################


  def get_off_stats_against(self, offense, defense, df, play_type, verbose = False):
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
      stats_dict = self.get_offensive_stats(offense, df_combo, play_type)

    return(stats_dict)


  #########################

  def get_def_stats_against(self, offense, defense, df, play_type, verbose = False):
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
      stats_dict = self.get_defensive_stats(defense, df_combo, play_type)

    return(stats_dict)

  #########################################


  def get_offensive_dict_against(self, offense, df, play_type):
    '''
    Inputs: offense, dataframe
    Outputs: dictionary of offensive stats against each team
    '''

    if offense not in df['offense'].unique():
        print('Input offense is not in our data, please check spelling at try again')
        return()


    output = {}

    for team in df['defense'].unique():
      output[team] = self.get_off_stats_against(offense, team, df, play_type)

    return(output)


  ####################################


  def get_defensive_dict_against(self, defense, df, play_type):
    '''
    Inputs: defense, dataframe
    Outputs: dictionary of defensive stats against each team
    '''

    if defense not in df['defense'].unique():
        print('Input defense is not in our data, please check spelling at try again')
        return()

    output = {}

    for team in df['offense'].unique():
      output[team] = self.get_def_stats_against(team, defense, df, play_type)

    return(output)



  def build_json(self):
    dict_of_teams = {}
    for team in tqdm(self.rush_off,
                     desc = 'Building Statistics JSON'):
      #print(team)
      dict_of_teams[team] = {}
      dict_of_teams[team]['rush_off_general'] = self.get_offensive_stats(team, self.rush, play_type= 'rush')
      dict_of_teams[team]['rush_def_general'] = self.get_defensive_stats(team, self.rush, play_type= 'rush')
      dict_of_teams[team]['pass_off_general'] = self.get_offensive_stats(team, self.throw, play_type= 'pass')
      dict_of_teams[team]['pass_def_general'] = self.get_defensive_stats(team, self.throw, play_type= 'pass')

      dict_of_teams[team]['rush_off_by_team'] = self.get_offensive_dict_against(team, self.rush, play_type= 'rush')
      dict_of_teams[team]['rush_def_by_team'] = self.get_defensive_dict_against(team, self.rush, play_type= 'rush')
      dict_of_teams[team]['pass_off_by_team'] = self.get_offensive_dict_against(team, self.throw, play_type= 'pass')
      dict_of_teams[team]['pass_def_by_team'] = self.get_defensive_dict_against(team, self.throw, play_type= 'pass')

    self.dict_of_teams = dict_of_teams

    self.set_up = True





    return(dict_of_teams)




  def get_json(self, path = None, write = True):
    import json
    if self.set_up == False:
      print('running build_json() first')
      self.build_json()

    dict_of_teams = self.dict_of_teams
    #print(dict_of_teams)
    if path != None:
      try:
        os.chdir(path)
      except:
        print('path does not exist')

    if write == True:
      with open('stats.json', 'w') as output:
        json.dump(dict_of_teams, output)

    return(dict_of_teams)


  def get_dict(self):
    return(self.dict_of_teams)
  


stats = Stats()
cwd = os.getcwd()
try:
  stats.get_json(path = cwd+'//data')
except:
  stats.get_json()

