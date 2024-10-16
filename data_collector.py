import json
import simplejson
import requests
import pandas as pd
import datetime
import time
import os

class DataCollector:
    """ Class fetches and loads the json data. Next, it extracts the important information and saves it into a csv file.

    Attributes:
        api_key: API key from Glassnode.

    Methods:
        fetch_api: Fetches and loads the data as a json file.
        extract_data: Extracts the data from the json file and saves it as a csv file.
        process_data: Loops through the path list and calls the two class methods above.

    """
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_api(self, path_list, coin_type):
        """ Class method fetches and loads the data as a json file. 
        
        Note:
            Only handles a maximum of 120 API requests. If requests exceed, sleep for 60s.

        Args:
            path_list: A list of metric urls corresponding to a specific subscription tier and coin symbol.
            coin_type: Crypto coin symbol.

        Returns:
            Data from the json file.

        """
        data = {}
        for i in range(0, len(path_list), 120):
            batch_paths = path_list[i:i + 120]
            for url in batch_paths:
                res = requests.get(url,
                    params={'a': coin_type, 'api_key': self.api_key}, stream=True)
                endpoint_name = url.split('/')[-1]
                try:
                    json_data = simplejson.loads(res.text)
                    data[endpoint_name] = json_data
                except simplejson.JSONDecodeError:
                    print(f'Error decoding JSON response from {url}')
            if i + 120 < len(path_list):
                time.sleep(60)
        return data

    def extract_data(self, json_data, endpoint_name, coin_type):
        """ Class method extracts the data from the json file and saves it as a csv file. 

        Note:
            Only handles either a nested dictionary within a list or a nested dictionary within a dictionary. 

        Args:
            json_data: Data from the json file.
            endpoint_name: Name of the CSV file.

        Returns:
            A pandas dataframe with 2 or more rows: timestamp and its respective values.

        """
        if isinstance(json_data, dict):
            if any(isinstance(value, dict) for value in json_data.values()):
                df = pd.json_normalize(json_data)
                df = df.rename(columns={**{'t': 'timestamp'},
                                        **{col: f'{coin_type} {endpoint_name} {col.replace(".", " ")}' for col in df.columns[1:]}})
        elif isinstance(json_data, list):
            if any(isinstance(item, dict) for item in json_data):
                df = pd.json_normalize(json_data)
                df = df.rename(columns={**{'t': 'timestamp'},
                                        **{col: f'{coin_type} {endpoint_name} {col.replace(".", " ")}' for col in df.columns[1:]}})
                
        df['timestamp'] = df['timestamp'].apply(lambda x: datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'))
        os.makedirs(f'{coin_type}-metrics', exist_ok=True)
        df.to_csv(f'{coin_type}-metrics/{coin_type}-{endpoint_name}.csv', index=False)
        return df

    def process_data(self, url_list, coin_type):
        """ Class method loops through the path list and calls the two class methods above.

        Args:
            url_list: A list of metric urls corresponding to a specific subscription tier and coin symbol.
            coin_type: Crypto coin symbol.

        """
        data = self.fetch_api(url_list, coin_type)
        for endpoint_name, json_data in data.items():
            self.extract_data(json_data, endpoint_name, coin_type)