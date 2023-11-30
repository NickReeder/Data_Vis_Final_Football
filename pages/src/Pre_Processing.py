import numpy as np
import pandas as pd

class pre_processing:
    ''' 
    This is the class for handling all of the data pre-processing.

    It initilizes a constants object and splits the pre-processing by passing data and rushing data
    '''
    
    def __init__(self):

        return
        
    def get_values(self, data):

        '''
        This function gets the total yards gained per play, the play type, and reformats the field position variable

        Returns:
            yards_gained, play_type
        '''

        import pandas as pd
        
        

        yards_gained = []
        play_type = []
        for row in data.itertuples():
            try:
                if 'yards_after_catch' in data.columns: #this check can happen at the beginning if needed
                    yards_gained.append(row.yards + row.yards_after_catch) 
                    play_type.append('P')
                elif 'yards_after_contact' in data.columns:
                    yards_gained.append(row.yards + row.yards_after_contact) 
                    play_type.append('R')
            except:
                print('Error at index', row.Index)
                print('Game ID', row.gsis_game_id)
                print('Play ID', row.gsis_play_id)
        return(yards_gained, play_type)
    
    def parse_fieldpos(self, data):
        '''
        This function reformats the field position variable to make it easier to use for analysis.
        '''
        import pandas as pd
        
        fieldpos_list = [pos.split(' ') for pos in data['fieldpos']]
        for i, pos in enumerate(fieldpos_list):
            if pos[0] == data['offense'].iloc[i]:
                pos[1] = int('-' + pos[1])
                data['fieldpos'].iloc[i] = pos[1]
            else:
                data['fieldpos'].iloc[i] = int(pos[1])
                
        return data
    
    def parse_game_clock(self, data):
        '''
        This function reformats the game clock variable to make it easier to use for analysis.
        '''
        import pandas as pd
        data['clock_min'] = ''
        data['clock_sec'] = ''
        game_clock_list = [clock.split(':') for clock in data['game_clock']]
        for i, clock in enumerate(game_clock_list):
            data['clock_min'].iloc[i] = int(clock[0])
            data['clock_sec'].iloc[i] = int(clock[1])

        return data
    
    def stitch(self, yards, play_type, data):

        '''
        This function stitches the new dataframe together

        Returns:
            dataframe
        '''
        data['yards_gained'] = yards
        data['yards_gained'].replace(np.nan,0)
        data['play_type'] = play_type
        return(data)
    

    def pre_processing(self, data):
        '''
        PASSING DATA ONLY
        This function calls the get_values_pass and stitch functions to make a single pre-processing call

        Returns:
            clean_data, padas dataframe (data frame of cleaned and processed data)
        '''
        yards_gained, play_type= self.get_values(data)
        data = self.parse_fieldpos(data)
        data = self.parse_game_clock(data)
        clean_data = self.stitch(yards_gained, play_type, data)
        return(clean_data)
    

