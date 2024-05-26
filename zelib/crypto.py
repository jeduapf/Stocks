import requests
import json
from datetime import datetime
from time import time 
import os
import pandas as pd
  
  
def timer(func): 
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 

# @timer
def real_time_crypto_data(symbols):
    api_url = "https://api.coincap.io/v2/assets"
    response = requests.get(api_url)

    dict_ = response.json()
    date_time = datetime.fromtimestamp( float( str(int(dict_['timestamp']/1000)) +  '.' + str(int(dict_['timestamp']%1000)) ) )

    crypto_dict = {}
    for ele in dict_['data']:
        if ele['symbol'] in symbols:
            crypto_dict[ele['symbol']] = {  'name': ele['name'],
                                            'id': ele['id'],
                                            'rank': ele['rank'],
                                            'supply': ele['supply'],
                                            'maxSupply': ele['maxSupply'], 
                                            'marketCapUsd': ele['marketCapUsd'],
                                            'volumeUsd24Hr': ele['volumeUsd24Hr'],
                                            'priceUsd': ele['priceUsd'],
                                            'changePercent24Hr': ele['changePercent24Hr'],
                                            'vwap24Hr': ele['vwap24Hr']                      }

    # print(crypto_dict)
    return date_time, crypto_dict

def get_periods(KEY = 'EA0298A6-2076-4DE3-9FBC-471662E86CBD'):
    url = "https://rest.coinapi.io/v1/ohlcv/periods"

    headers = {
      'Accept': 'text/plain',
      'X-CoinAPI-Key': KEY
    }
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        SAVE_DIR = os.path.join(os.getcwd(),"periods.json")
        print(f"\nSuccessfully ordered and saving in \n\t\t{SAVE_DIR}\n")
        with open(SAVE_DIR, "w") as f:
            f.write(json.dumps(response.text, indent=4))

    else:
        response.raise_for_status()
        raise ValueError(f"\nSomething went wrong... Sorry")

def coinapi(payload, symbol_id, FILE, KEY = 'EA0298A6-2076-4DE3-9FBC-471662E86CBD'):
    
    url = f"https://rest.coinapi.io/v1/ohlcv/{symbol_id}/history?"

    headers = {
      'Accept': 'text/plain',
      'X-CoinAPI-Key': KEY
    }

    for k in payload.keys():
        url += k + '=' + str(payload[k]) + '&'
    url = url[:-1]

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        SAVE_DIR = os.path.join(os.getcwd(),f"{FILE}.json")
        print(f"\nSuccessfully ordered and saving in \n\t\t{SAVE_DIR}\n")
        with open(SAVE_DIR, "w") as f:
            f.write(json.dumps(response.text, indent=4))
    else:
        response.raise_for_status()
        raise ValueError(f"\nSomething went wrong... Sorry")

def coinapi_symbols(KEY = 'EA0298A6-2076-4DE3-9FBC-471662E86CBD'):
    url = "https://rest.coinapi.io/v1/symbols"

    payload={}
    headers = {
      'Accept': 'text/plain',
      'X-CoinAPI-Key': KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        SAVE_DIR = os.path.join(os.getcwd(),"coinapi_symbols.json")
        print(f"\nSuccessfully requested symbols and saving in \n\t\t{SAVE_DIR}\n")
        with open(SAVE_DIR, "w") as f:
            f.write(json.dumps(response.text, indent=4))

    else:
        raise ValueError(f"\nSomething went wrong... Sorry")

def read_json_df(PATH, timestamp = False, just_sec = True):
    with open(PATH, 'r') as f:
        data = json.loads(json.load(f))

    if timestamp:
        if just_sec:
            for k in range(len(data)):
                data[k]['time_period_start'] = int(datetime.strptime(data[k]['time_period_start'], "%Y-%m-%dT%H:%M:%S.%f0Z").timestamp())
                data[k]['time_period_end'] = int(datetime.strptime(data[k]['time_period_end'], "%Y-%m-%dT%H:%M:%S.%f0Z").timestamp())
                data[k]['time_open'] = int(datetime.strptime(data[k]['time_open'], "%Y-%m-%dT%H:%M:%S.%f0Z").timestamp())
                data[k]['time_close'] = int(datetime.strptime(data[k]['time_close'], "%Y-%m-%dT%H:%M:%S.%f0Z").timestamp())

        else:
            for k in range(len(data)):
                data[k]['time_period_start'] = datetime.strptime(data[k]['time_period_start'], "%Y-%m-%dT%H:%M:%S.%f0Z").timestamp()
                data[k]['time_period_end'] = datetime.strptime(data[k]['time_period_end'], "%Y-%m-%dT%H:%M:%S.%f0Z").timestamp()
                data[k]['time_open'] = datetime.strptime(data[k]['time_open'], "%Y-%m-%dT%H:%M:%S.%f0Z").timestamp()
                data[k]['time_close'] = datetime.strptime(data[k]['time_close'], "%Y-%m-%dT%H:%M:%S.%f0Z").timestamp()
    else:
        for k in range(len(data)):
            data[k]['time_period_start'] = datetime.strptime(data[k]['time_period_start'], "%Y-%m-%dT%H:%M:%S.%f0Z").strftime('%d/%m/%Y,%H:%M:%S')#.timestamp()
            data[k]['time_period_end'] = datetime.strptime(data[k]['time_period_end'], "%Y-%m-%dT%H:%M:%S.%f0Z").strftime('%d/%m/%Y,%H:%M:%S')#.timestamp()
            data[k]['time_open'] = datetime.strptime(data[k]['time_open'], "%Y-%m-%dT%H:%M:%S.%f0Z").strftime('%d/%m/%Y,%H:%M:%S')##.timestamp()
            data[k]['time_close'] = datetime.strptime(data[k]['time_close'], "%Y-%m-%dT%H:%M:%S.%f0Z").strftime('%d/%m/%Y,%H:%M:%S')##.timestamp()

    df = pd.DataFrame.from_records(data)
    return df