# GlassNode API Downloader

This project provides a set of Python classes to facilitate querying, collecting, and processing cryptocurrency data from GlassNode.

## Classes Overview

### 1. DataQuerier

The DataQuerier class fetches the coin symbol and the individual metric URLs from GlassNode.
```
from data_querier import DataQuerier

# Initialize 
querier = DataQuerier(endpoints_file='path/to/your/endpoints.txt')

# Check the available coin for a given metric URL
coin_symbol = querier.get_symbol('/path/to/metric')

# Get metric URLs for a specific tier and coin symbol
t1_btc_path_list = querier.get_metrics(1, 'BTC')
t2_btc_path_list = querier.get_metrics(2, 'BTC')
t3_btc_path_list = querier.get_metrics(3, 'BTC')
btc_path_list = t1_btc_path_list + t2_btc_path_list + t3_btc_path_list
```

### 2. DataCollector

The DataCollector class fetches and process data from the GlassNode API.
```
from data_collector import DataCollector

# Initialize
collector = CryptoDataCollector(api_key='your_api_key')

# Downloads Individual Metrics
collector.process_data(btc_path_list, 'BTC')
```

### 3. FileCombiner

The FileCombiner class combines multiple CSVs into a single DataFrame.
```
from file_combiner import FileCombiner

# Initialize
combiner = FileCombiner()

# Combine the CSV
combiner.join_csv('ETH-metrics')
```

## Setting Up

### Obtain API Key

You can get your API from your [Glassnode account](https://studio.glassnode.com/settings/api).

### Install Packages
Download external libraries: simplejson, requests, pandas
```
pip install -r requirements.txt
```