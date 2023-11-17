import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

class pre_processing:
    ''' 
    This is the class for handling all of the data pre-processing.

    It initilizes a constants object and splits the pre-processing by passing data and rushing data
    '''


    def __init__(self):

        ''' 
        Contants used in pre-processing. Last update: 10/9/23 by Nick Reeder

        Constants: FCS Teams
        '''
        self.fcs_teams = ['LANW','ILSO','TNMR','ILST','OHYO','MOSW','NDST',
                            'OHDA','PADU','CASU','NYMR','INBU','DEUN','RIUN',
                            'NYST','NCEL','MAMK','VAJM','KYMO','AZNO','INST',
                            'IANO','ORPS','UTSO','IDUN','MTUN','CADA','ALNO',
                            'NJMO','IDST','WAEA','UTWB','LASE','NDUN','ILWE',
                            'SDVE','LANI','SCWO','SCST','FLAM','MDMO','NCAT',
                            'DCHO','PASF','PAVI','MDTO','NHUN','VARI','MSVA',
                            'TNAI','ARPB','KYMU','TNAP','MOSE','ILEA','NYCW',
                            'IADR','SDST','NJPR','NYCL','PALF','MAHA','CTYA',
                            'CASL','MTST','CASA','TNTC','VANO','CTSH','MEUN',
                            'VAWM','MAHC','NYCN','NYFO','PAUN','RIBT','NYWA',
                            'NYAB','ALJA','PABU','PALE','DCGT','ARCE','KYEA',
                            'TXAC','LAMC','TXSF','NCCE','FLBC','DEST','RIBR',
                            'NHDA','MSAL','TXPV','LASO','ALAM','TXHT','GAME',
                            'NCWE','ALSM','NCDA','PARM','TXIW','SCFU','SCCI',
                            'TXLA','MSJA','SCPR','TXSO','VAMI','TNCH','SCCH',
                            'INVA','NYCG','TNEA','FLSS','ALST','GAKS','NCGW',
                            'VAHI','NCCM','CONO','CTCE','LAGR']
        
    def get_values(self, data):

        '''
        This function gets the index of all games just between FCS teams and the total yards gained per play

        Returns:
            both_fcs_idx: list (index of FCS v FCS games),
            yards_gained,
            play_type
        '''

        import pandas as pd

        both_fcs_idx = []
        yards_gained = []
        play_type = []
        for row in data.itertuples():
            try:
                #If this gets slow we can push them into a if statement to cut out on appends
                both_fcs_idx.append(row.away_team in self.fcs_teams and row.home_team in self.fcs_teams)
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

    
        return(both_fcs_idx, yards_gained, play_type)
    
    def parse_fieldpos(self, data):
        '''
        This function reformats the field position variable to make it easier to use for analysis.
        '''
        
        fieldpos_list = [pos.split(' ') for pos in data['fieldpos']]
        for i, pos in enumerate(fieldpos_list):
            if not pos[1].isnumeric():
                data.drop(i)
            elif pos[0] == data['offense'].iloc[i]:
                pos[1] = int('-' + pos[1])
                data['fieldpos'].iloc[i] = pos[1]
            else:
                data['fieldpos'].iloc[i] = int(pos[1])
        return data
    
    def parse_game_clock(self, data):
        '''
        This function reformats the game clock variable to make it easier to use for analysis.
        '''

        data['clock_min'] = ''
        data['clock_sec'] = ''
        game_clock_list = [clock.split(':') for clock in data['game_clock']]
        for i, clock in enumerate(game_clock_list):
            data['clock_min'].iloc[i] = int(clock[0])
            data['clock_sec'].iloc[i] = int(clock[1])
        return data
    
    def stitch(self, idx, yards, play_type, data):

        '''
        This function stitches the new dataframe together

        Returns:
            data_slim, pandas data frame (data frame of only FCS v FCS games with a yards_gained column)
        '''
        data['yards_gained'] = yards
        data['yards_gained'].replace(np.nan,0)
        data['play_type'] = play_type
        data_slim = data[idx]
        return(data_slim)
    
    def pre_processing(self, data):
        '''
        PASSING DATA ONLY
        This function calls the get_values_pass and stitch functions to make a single pre-processing call

        Returns:
            clean_data, padas dataframe (data frame of cleaned and processed data)
        '''
        index, yards_gained, play_type= self.get_values(data)
        data = self.parse_fieldpos(data)
        data = self.parse_game_clock(data)
        clean_data = self.stitch(index, yards_gained, play_type, data)
        return(clean_data)
    

