import json
import simplejson
import requests
import pandas as pd
import datetime
import time
import os

class DataQuerier:
    """ Class method queries data.

    Attributes:
        endpoints_file: File containing all the crypto endpoints and metrics urls.

    Methods:
        get_symbol: Takes a metric url and returns the symbol of the crypto coin(s) that uses that metric.
        get_metrics: Takes the subscription tier and coin symbol and returns all the metric urls associated with it.

    """
    def __init__(self, endpoints_file='endpoints.txt'):
        with open(endpoints_file, 'r') as f:
            self.endpoints = json.load(f)

    def get_symbol(self, path_name):
        """ Class method takes a metric url and returns the symbol of the crypto coin(s) that uses that metric.

        Args:
            path_name: A list of urls from endpoints.txt.

        Returns:
            Crypto coin symbol.

        """
        for item in self.endpoints:
            if item['path'] == path_name[25:]:
                print(item['assets'][0]['symbol'])

    def get_metrics(self, tier_number, coin_type):
        """ Class method takes the subscription tier and coin symbol and returns all the metric urls associated with it.

        Args:
            tier_number: Subscription tier number(1, 2 and 3)
            coin_type: Crypto coin symbol.

        Returns:
            A list of metric urls.

        """
        path_list = []
        for item in self.endpoints:
            if item['tier'] == tier_number and item['assets'][0]['symbol'] == coin_type:
                path_list.append('https://api.glassnode.com' + item['path'])
        return path_list