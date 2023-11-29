import os
import sqlite3
import pandas as pd
from src.Pre_Processing import pre_processing as PP
import src.sql_queries as SQ
from IPython.display import clear_output
from glob import glob

# Minimal example code to implement a database (with minimal documentation!)
# No error handling has been implemented, so catastrophic failure is possible.

class FootballDB:

    # File paths are all relative to where the code is run from, not where this module is saved!
    # The idea is that if we're using this code, we'll be importing it into a file that lives in the main project directory
    # Otherwise, you could remove the hardcoded file paths here, and instead supply them as parameters when instantiating the class

    PATH_DB_LOCAL = '../data/NFL_13_22.db'

    PATH_DB_ST = 'data/NFL_13_22.db'
    
    # Files for new games go here
    PATH_UNLOADED = '../data/unloaded/'

    # Files for games already in the DB get moved here
    PATH_LOADED = '../data/loaded/'

    # Usually have a naming convention for data files, 
    # in case other files accidentally make their way into the directory
    FLAG_GAMEFILES = 'DATA_*.csv'

    def __init__(self
                 ):
        '''
        Create the database if it doesn't exist
        '''
        if not (os.path.exists(self.PATH_DB_LOCAL)) or (os.path.exists(self.PATH_DB_ST)):
            #print('Creating the database')
            try:
                conn = sqlite3.connect(self.PATH_DB_LOCAL)
            except:
                conn = sqlite3.connect(self.PATH_DB_ST)
            conn.close()
        return
    
    def connect(self):
        '''
        Establish a connection and cursor
        '''
        try:
            self.conn = sqlite3.connect(self.PATH_DB_LOCAL)
        except:
            self.conn = sqlite3.connect(self.PATH_DB_ST)
        self.curs = self.conn.cursor()
        return
    
    def close(self):
        '''
        Close the connection
        '''
        self.conn.close()
        return
    
    def get_games(self):
        '''
        Return a list of game_id in the database
        '''
        games = self.run_query("SELECT DISTINCT game_id FROM tGame;")['game_id']
        return list(games)
    
    def get_game_data(self, 
                      game_id
                      ) -> pd.DataFrame:
        sql = "SELECT * FROM tGame WHERE game_id = ?;"
        return self.run_query(sql, (game_id,))
    
    def get_tGame(self) -> pd.DataFrame:
        '''
        Returns the tGame table from the provided database as a Pandas dataframe
        '''
        sql = "SELECT * FROM tGame;"
        return self.run_query(sql)
    
    def get_tPass(self) -> pd.DataFrame:
        '''
        Returns the tGame table from the provided database as a Pandas dataframe
        '''
        sql = "SELECT * FROM tPass;"
        return self.run_query(sql)
    
    def get_tRush(self) -> pd.DataFrame:
        '''
        Returns the tGame table from the provided database as a Pandas dataframe
        '''
        sql = "SELECT * FROM tRush;"
        return self.run_query(sql)
    
    def get_tRunConcept(self) -> pd.DataFrame:
        '''
        Returns the tGame table from the provided database as a Pandas dataframe
        '''
        sql = "SELECT * FROM tRunConcept;"
        return self.run_query(sql)
    
    def run_query(self, 
                  sql: str, 
                  params: tuple or dict = None
                  ) -> pd.DataFrame:
        '''
        Run a SELECT query
        '''
        self.connect()
        if params is not None:
            results = pd.read_sql(sql, 
                                  self.conn, 
                                  params=params
                                  )
        else:
            results = pd.read_sql(sql,
                                  self.conn
                                  )
        self.close()
        return results
    
    def build_tables(self, 
                     are_you_sure:bool=False
                     ):
        '''
        Build the tables (with a safety flag to be sure we don't run this by accident!)
        '''
        if not are_you_sure:
            raise Exception("You almost deleted the database by accident!")
        
        # and as a double-double check!!!
        really_sure = input("Are you really sure you want to drop all tables and rebuild? Enter y if so.")
        if really_sure != 'y':
            print("OK - we won't do it then! Quitting.")
            return

        print('Building the tables')
        self.connect()

        self.curs.execute("DROP TABLE IF EXISTS tGame;")
        sql = SQ.SQL_G_BUILD
        self.curs.execute(sql)

        self.curs.execute("DROP TABLE IF EXISTS tPass;")
        sql = SQ.SQL_P_BUILD
        self.curs.execute(sql)

        self.curs.execute("DROP TABLE IF EXISTS tRush;")
        sql = SQ.SQL_R_BUILD
        self.curs.execute(sql)

        self.curs.execute("DROP TABLE IF EXISTS tRunConcept;")
        sql = SQ.SQL_RC_BUILD
        self.curs.execute(sql)

        self.close()
        return
    
    def preprocess(self, df):
        '''
        Removes plays with duplicate play IDs and utilizes Pre_Processing.py to prepare the data for entry into the database.
        '''

        clear_output(wait=True)
        print('Checking for Duplicate Plays...')

        df.drop_duplicates(subset='play_id', keep=False, inplace=True)
        
        clear_output(wait=True)
        print('Any Duplicate Plays Removed!')

        clear_output(wait=True)
        print('Preprocessing Data...')

        df = df[df['yards'].notna()]

        Pre_Proc = PP()
        clean_df = Pre_Proc.pre_processing(data=df)

        clear_output(wait=True)
        print('Data Preprocessed!')

        return clean_df

    def load_new_data(self):
        '''
        Find new data files to load and then move them to the LOADED directory
        '''
        
        # Connect
        self.connect()
        
        # Our INSERT statement
        sql = """
            INSERT INTO tGameData (game_id, play_id, player_id, x, y, m)
            VALUES (:game_id, :play_id, :player_id, :x, :y, :m)
            ;"""

        files_to_load = glob(self.PATH_UNLOADED + self.FLAG_GAMEFILES)

        for file in files_to_load:
            print('Loading a file:', file)
            df = pd.read_csv(file)

            clean_df = self.preprocess(df)

            num_rows = len(clean_df)
            current_row = 0

            for i, row in enumerate(clean_df.to_dict(orient='records')):
                # Check if Game exists
                x = pd.read_sql(SQ.SQL_CHECK_GAME, self.conn, params=row)
                if len(x) == 0:
                    # Insert the record if it did not
                    self.curs.execute(SQ.SQL_INSERT_TGAME, row)

                if 'passing' in file:
                    # Check if Pass exists
                    x = pd.read_sql(SQ.SQL_CHECK_PASS, self.conn, params=row)
                    if len(x) == 0:
                        # Insert the record if it did not
                        self.curs.execute(SQ.SQL_INSERT_TPASS, row)
                    
                    current_row+=1
                    clear_output(wait=True)
                    print('Data Fill - Progress: ' + str("%.1f" % ((current_row/num_rows)*100)) + '%')

                if 'rushing' in file:
                    # Check if Rush exists
                    x = pd.read_sql(SQ.SQL_CHECK_RUSH, self.conn, params=row)
                    if len(x) == 0:
                        # Insert the record if it did not
                        self.curs.execute(SQ.SQL_INSERT_TRUSH, row)

                    # Check if RunConcept exists
                        x = pd.read_sql(SQ.SQL_CHECK_RUNCONCEPT, self.conn, params=row)
                        if len(x) == 0:
                            # Insert the record if it did not
                            self.curs.execute(SQ.SQL_INSERT_TRUNCONCEPT, row)

                    current_row+=1
                    clear_output(wait=True)
                    print('Data Fill - Progress: ' + str("%.1f" % ((current_row/num_rows)*100)) + '%')

            # Move the file to the LOADED directory
            os.rename(file, file.replace(self.PATH_UNLOADED, self.PATH_LOADED))
        
        # Commit the changes and close the connection
        self.conn.commit()
        self.close()
        return