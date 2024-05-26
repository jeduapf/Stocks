from zelib import *
import plotly.graph_objects as go




if __name__ == "__main__":
    # test_trader()

    symbols = ['BTC', 'ETH', 'ADA', 'DOGE', 'BNB', 'XRP']
    # date_time, crypto_dict = real_time_crypto_data(symbols)
    # get_periods(KEY = 'EA0298A6-2076-4DE3-9FBC-471662E86CBD')

    # for symbol in symbols:
        # payload={
        #     'period_id': '10MIN',
        #     'time_start': '2021-05-10T00:00:00',
        #     'limit': 100,
        #     'include_empty_items': False
        # }
        # exchange_id = 'BINANCE' 
        # asset_id_base = symbol
        # asset_id_quote = 'USDT' 
        # symbol_id = f'{exchange_id}_SPOT_{asset_id_base}_{asset_id_quote}'
        # file = symbol_id

        # coinapi(payload,
        #         symbol_id,
        #         FILE = file,
        #         KEY = 'EA0298A6-2076-4DE3-9FBC-471662E86CBD')

    # data = read_json_df(PATH = f"C:/Users/jedua/Documents/Pessoal/Stocks/{symbol_id}.json", timestamp = True, just_sec = True)

    timeseries = empirical_dist(difference = "relative", PATH = r"C:\Users\jedua\Documents\Pessoal\Stocks\test")

    fig = go.Figure()
    t =  [datetime.fromtimestamp(float(i)) for i in timeseries[:,0,0].detach().cpu().numpy()] 
    for coin in range(timeseries.shape[-1]):   
        
        fig.add_trace(go.Scatter(x = t, y = 100*timeseries[:,-1,coin], mode="lines", name =f"{symbols[coin]}" ))

    fig.update_layout(
    title="Price percent change to last measure",
    xaxis_title="Day and time",
    yaxis_title="Percentage ( % )",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
            )
        )
    fig.show()