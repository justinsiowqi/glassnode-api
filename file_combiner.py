import json
import simplejson
import requests
import pandas as pd
import datetime
import time
import os

class FileCombiner:
    """ Class splits combines crypto csv files in a left-join.

    Methods:
        get_csv: Loops through the csv files in several folders and returns a list of dataframes.
        create_timestamp_df: Creates an empty dataframe with timestamp as the index. It ranges from 2008-12-31 till present day.
        join_csv: Calls get_csv on a list of dataframes and performs a left outer-join.

    """
    def get_csv(self, folder):
        """ Class method loops through the csv files in several folders and returns a list of dataframes.

        Note:
            Uses the folder directory that is created in CryptoDataCollector.

        Args:
            folder: Name of the folder containing crypto csv files.

        Returns:
            A list of dataframes.

        """
        df_list = []
        for filename in os.listdir(folder):
            if filename.endswith('.csv'):
                df = pd.read_csv(os.path.join(folder, filename), parse_dates=['timestamp'])
                df = df.set_index('timestamp')
                df_list.append(df)
        return df_list

    def create_timestamp_df(self):
        """ Class method creates an empty dataframe with timestamp as the index. It ranges from 2008-12-31 till present day.

        Returns:
            An empty dataframe with timestamp as the index column.

        """
        start_date = pd.Timestamp('2008-12-31')
        end_date = pd.Timestamp.now()
        timestamp_df = pd.DataFrame({'timestamp': pd.date_range(start_date, end_date)}).set_index('timestamp')
        return timestamp_df

    def join_csv(self, folders, delete_null=False):
        """ Class method calls get_csv on a list of dataframes and performs a left outer-join.

        Note:
            To remove rows that contain only null values, pass delete_null=True as an argument.

        Args:
            folders: List of folders containing crypto csv files.
            delete_null: Removes rows that contains only null values (set to false by default).

        Returns:
            A dataframe with all the dataframes combined column-wise.

        """
        df_list = self.get_csv(folders)
        
        timestamp_df = self.create_timestamp_df()
        join_df = timestamp_df.join(df_list, how='outer')

        if delete_null:
            join_df.dropna(how='all', inplace=True)

        join_df.to_csv(f'{folders[:3]}-metrics-concatenated.csv')
        
        return join_df