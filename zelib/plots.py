import plotly.graph_objects as go


def candlestick_plot(data):
    df = data.copy()

    fig = go.Figure(
        data=[go.Candlestick(
                x=df['time_open'],
                open=df['price_open'],
                high=df['price_high'],
                low=df['price_low'],
                close=df['price_close']
                            )]
                    )

    return fig

def add_SMA(fig, data, color = 'rgb(204, 204, 204)', feature = 'price_close', SMA = 20):
    
    df = data.copy()
    df[f'SMA({SMA})'] = df[feature].rolling(SMA).mean()

    fig.add_trace(
                    go.Scatter(
                        x=df['time_open'], 
                        y=df[f'SMA({SMA})'], 
                        mode='lines', 
                        name=f'SMA({SMA})',
                        line=dict(
                                    color=color,
                                    width=2
                                )
                        )
                  )

    return fig

def SMA(data):

    fig = candlestick_plot(data)
    SMA = 5
    fig = add_SMA(fig, data, color = f'rgba(0, {1275/SMA}, 255, 1)', feature = 'price_close', SMA = SMA)
    SMA = 10
    fig = add_SMA(fig, data, color = f'rgba(0, {1275/SMA}, 255, 1)', feature = 'price_close', SMA = SMA)
    SMA = 20
    fig = add_SMA(fig, data, color = f'rgba(0, {1275/SMA}, 255, 1)', feature = 'price_close', SMA = SMA)
    fig.show()
