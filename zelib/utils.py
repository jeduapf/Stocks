import numpy as np 
import torch
import os
from zelib import *


def empirical_dist(difference = "relative", PATH = "C:/Users/jedua/Documents/Pessoal/Stocks/test/"):
    data_path= []
    for x in os.listdir(PATH):
        if x.endswith(".json"):
            data_path.append(os.path.join(PATH, x))

    lista = []
    for path in data_path:
        df = read_json_df(PATH = path , timestamp = True, just_sec = True)

        timeseries_np = np.array([df['time_close'].values, df['price_close'].values], dtype = np.float64).T
        timeseries = torch.tensor(timeseries_np)

        if difference == "relative":
            diff = torch.diff(timeseries[:,1], dim=0)
            relative = diff/timeseries[:-1,1]
        elif difference == "log":
            relative = torch.log(timeseries[1:,1]/timeseries[:-1,1])
        else:
            raise ValueError(f"The requested difference ({difference}), doesn't exist")


        lista.append(torch.stack((timeseries[:-1,0], timeseries[:-1,1], relative),-1))

    try: 
        timeseries = torch.transpose( torch.transpose(torch.stack(lista), 2, 0), 1, 0) 

    # TODO: Handle error of missing data in one of the timeseries
    except:
        pass

    flag = False
    for sym in range(timeseries.shape[2]):
        if torch.abs(torch.sum(timeseries[:,0,0] - timeseries[:,0,sym])) > 60: # If the sum of the differences is bigger than 1 min then its not that precise
            flag = True

    if flag:
        raise ValueError(f"Something went wrong with the data, there is at least one stock which its times don't match another stock")

    return timeseries
    
def relative_growth():
    pass

def VaR(df, per = 1):
    pass